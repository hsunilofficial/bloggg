# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden

from .models import Post, Profile
from .forms import PostForm, ProfileUpdateForm, PreferenceForm
from .utils import get_client_ip

User = get_user_model()


# =========================================================
# ROLE HELPERS
# =========================================================
def is_admin(request):
    return request.user.is_authenticated and hasattr(request.user, "profile") and request.user.profile.role == "admin"


def is_editor(request):
    return request.user.is_authenticated and hasattr(request.user, "profile") and request.user.profile.role in ["editor", "admin"]


def is_viewer(request):
    return request.user.is_authenticated and hasattr(request.user, "profile") and request.user.profile.role in ["viewer", "editor", "admin"]


# =========================================================
# AUTH / ACCOUNT
# =========================================================
class ForgotPasswordView(PasswordResetView):
    template_name = "forgot_password.html"
    email_template_name = "password_reset_email.html"
    subject_template_name = "password_reset_subject.txt"
    success_url = "/reset-password-sent/"


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "blog/login.html", {"error": "Invalid credentials"})

    return render(request, "blog/login.html")


def logout_view(request):
    logout(request)
    return render(request, "blog/logout.html")


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role="viewer")
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "blog/signup.html", {"form": form})


# =========================================================
# PUBLIC PAGES
# =========================================================
def home(request):
    return render(request, "blog/index.html")


def about(request):
    return render(request, "blog/about.html")


def contact(request):
    if request.method == "POST":
        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")
    return render(request, "blog/contact.html")


def posts(request):
    all_posts = Post.objects.all().order_by("-created_at")
    return render(request, "blog/posts.html", {"posts": all_posts})


def public_posts(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "blog/public_posts.html", {"posts": posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog/post_detail.html", {"post": post})


def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog/view_post.html", {"post": post})


# =========================================================
# SETTINGS / PROFILE
# =========================================================
@login_required
def settings_page(request):
    user = request.user

    if request.method == "POST":

        # Profile update
        if "profile_submit" in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=user)
            if profile_form.is_valid():
                updated_user = profile_form.save(commit=False)
                password = profile_form.cleaned_data.get("password")
                if password:
                    updated_user.set_password(password)
                    updated_user.save()
                    update_session_auth_hash(request, updated_user)
                else:
                    updated_user.save()
                messages.success(request, "Profile updated successfully!")
                return redirect("settings")

        # Preferences
        elif "pref_submit" in request.POST:
            request.session["notifications"] = "notifications" in request.POST
            request.session["auto_backup"] = "auto_backup" in request.POST
            request.session["dark_mode"] = "dark_mode" in request.POST
            messages.success(request, "Preferences updated!")
            return redirect("settings")

        # Delete account
        elif "delete_account" in request.POST:
            user.delete()
            messages.error(request, "Your account has been deleted.")
            return redirect("home")

    profile_form = ProfileUpdateForm(instance=user)
    pref_form = PreferenceForm(
        initial={
            "notifications": request.session.get("notifications", True),
            "auto_backup": request.session.get("auto_backup", False),
            "dark_mode": request.session.get("dark_mode", False),
        }
    )

    return render(
        request,
        "blog/settings.html",
        {"profile_form": profile_form, "pref_form": pref_form},
    )


# =========================================================
# POST: ADD / EDIT / DELETE / MANAGE
# =========================================================
def add_post(request):
    if not is_viewer(request):
        return redirect("login")

    ip = get_client_ip(request)
    anon_limit = None

    if not request.user.is_authenticated:
        anon_limit = Post.objects.filter(ip_address=ip, author__isnull=True).count()
        if anon_limit >= 3:
            messages.warning(request, "Anonymous post limit reached. Log in to continue.")
            return redirect("login")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.author = request.user
            else:
                post.ip_address = ip
            post.save()
            messages.success(request, "Post added successfully.")
            return redirect("manage_posts")
    else:
        form = PostForm()

    return render(request, "blog/add_post.html", {"form": form, "anon_post_count": anon_limit})


def manage_posts(request):
    if not is_editor(request):
        return redirect("home")

    # Bulk actions
    if request.method == "POST" and "bulk_action" in request.POST:
        action = request.POST.get("bulk_action")
        selected_ids = request.POST.getlist("selected_posts")

        if not selected_ids:
            messages.warning(request, "No posts selected.")
            return redirect("manage_posts")

        posts_to_modify = Post.objects.filter(id__in=selected_ids)

        if action == "delete":
            posts_to_modify.delete()
            messages.success(request, "Selected posts deleted.")
        elif action == "publish":
            posts_to_modify.update(status="published")
            messages.success(request, "Posts Published.")
        elif action == "pending":
            posts_to_modify.update(status="pending")
            messages.success(request, "Posts marked Pending.")
        elif action == "draft":
            posts_to_modify.update(status="draft")
            messages.success(request, "Posts marked Draft.")

        return redirect("manage_posts")

    posts = Post.objects.all()

    search = request.GET.get("search", "")
    if search:
        posts = posts.filter(title__icontains=search)

    status_filter = request.GET.get("status", "")
    if status_filter:
        posts = posts.filter(status=status_filter)

    sort = request.GET.get("sort", "")
    if sort == "oldest":
        posts = posts.order_by("created_at")
    else:
        posts = posts.order_by("-created_at")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/admin/manage_posts.html", {
        "page_obj": page_obj,
        "posts": page_obj.object_list,
        "search": search,
        "status_filter": status_filter,
        "sort": sort,
    })


def edit_post(request, post_id):
    if not is_editor(request):
        return redirect("home")

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated.")
            return redirect("manage_posts")
    else:
        form = PostForm(instance=post)

    return render(request, "blog/edit_post.html", {"form": form, "post": post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        post.delete()
        return redirect("posts")  

    return render(request, "blog/confirm_delete_post.html", {"post": post})



# =========================================================
# ADMIN: DASHBOARD + PENDING POSTS
# =========================================================
def dashboard(request):
    if not is_editor(request):
        return redirect("home")

    posts_count = Post.objects.count()
    published = Post.objects.filter(status='published').count()
    drafts = Post.objects.filter(status='draft').count()
    pending = Post.objects.filter(status='pending').count()

    return render(request, 'blog/admin/dashboard.html', {
        'posts_count': posts_count,
        'published': published,
        'drafts': drafts,
        'pending': pending,
    })


def pending_posts(request):
    if not is_editor(request):
        return redirect("home")

    pending = Post.objects.filter(status="pending").order_by('-created_at')

    return render(request, "blog/admin/dashboard_posts.html", {
        "posts": pending,
        "title": "Pending Posts",
        "pending_page": True,
    })


# =========================================================
# ADMIN: USER MANAGEMENT
# =========================================================
def admin_users(request):
    if not is_admin(request):
        return redirect("home")

    users = User.objects.select_related("profile").all()

    return render(request, "blog/admin/admin_users.html", {
        "users": users
    })

def manage_users(request):
    if not is_admin(request):
        return redirect("home")

    q = request.GET.get("q", "").strip()
    order = request.GET.get("order", "date_joined")
    direction = request.GET.get("direction", "desc")
    try:
        page_size = int(request.GET.get("page_size", 10))
    except ValueError:
        page_size = 10

    users = User.objects.select_related("profile").all()

    if q:
        users = users.filter(
            Q(username__icontains=q)
            | Q(email__icontains=q)
            | Q(first_name__icontains=q)
        )

    if direction == "asc":
        users = users.order_by(order)
    else:
        users = users.order_by(f"-{order}")

    paginator = Paginator(users, page_size)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    total_pages = paginator.num_pages
    start = max(1, current_page - 2)
    end = min(start + 4, total_pages)
    page_range = range(start, end + 1)

    return render(request, "blog/manage_users.html", {
        "page_obj": page_obj,
        "page_size": page_size,
        "q": q,
        "order": order,
        "direction": direction,
        "page_range": page_range,
        "total_pages": total_pages,
    })


def add_user(request):
    if not is_admin(request):
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role", "viewer")

        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' already exists.")
            return redirect("add_user")

        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user, role=role)

        user.is_staff = role in ["editor", "admin"]
        user.is_superuser = role == "admin"
        user.save()

        messages.success(request, f"User '{username}' created successfully!")
        return redirect("manage_users")

    return render(request, "blog/admin/add_user.html")


def edit_user(request, user_id):
    if not is_admin(request):
        return redirect("home")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        role = request.POST.get("role", "viewer")

        user.username = username
        user.email = email
        user.profile.role = role
        user.profile.save()

        user.is_staff = role in ["editor", "admin"]
        user.is_superuser = role == "admin"
        user.save()

        messages.success(request, "User updated successfully.")
        return redirect("manage_users")

    return render(request, "blog/admin/edit_user.html", {"user": user})


def view_user(request, user_id):
    if not is_admin(request):
        return redirect("home")

    user = get_object_or_404(User, id=user_id)
    return render(request, "blog/admin/view_user.html", {"user": user})


def delete_user(request, user_id):
    if not is_admin(request):
        return redirect("home")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        if request.user == user:
            messages.error(request, "You cannot delete your own account.")
            return redirect("manage_users")

        if user.is_superuser:
            messages.error(request, "You cannot delete a superuser.")
            return redirect("manage_users")

        user.delete()
        messages.success(request, "User deleted.")
        return redirect("manage_users")

    return render(request, "blog/admin/confirm_delete_user.html", {"user": user})


# =========================================================
# ROLES
# =========================================================
@login_required
def user_roles(request):
    if not is_admin(request):
        return HttpResponseForbidden("Access Denied: Admins only.")

    users = User.objects.select_related("profile").all()

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        new_role = request.POST.get("role")

        try:
            user_obj = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("user_roles")

        user_obj.profile.role = new_role
        user_obj.profile.save()

        user_obj.is_staff = new_role in ["editor", "admin"]
        user_obj.is_superuser = new_role == "admin"
        user_obj.save()

        messages.success(request, f"Role updated for {user_obj.username}.")
        return redirect("user_roles")

    return render(request, "blog/admin/user_roles.html", {"users": users})


# =========================================================
# ANALYTICS
# =========================================================
def analytics(request):
    if not is_admin(request):
        return redirect("home")

    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(status="published").count()
    draft_posts = Post.objects.filter(status="draft").count()
    pending_posts_count = Post.objects.filter(status="pending").count()

    total_users = User.objects.count()
    admins = User.objects.filter(profile__role="admin").count()
    editors = User.objects.filter(profile__role="editor").count()
    viewers = User.objects.filter(profile__role="viewer").count()

    return render(request, "blog/admin/analytics.html", {
        "total_posts": total_posts,
        "published_posts": published_posts,
        "draft_posts": draft_posts,
        "pending_posts": pending_posts_count,
        "total_users": total_users,
        "admins": admins,
        "editors": editors,
        "viewers": viewers,
    })


# =========================================================
# VIEWER PAGES
# =========================================================
@login_required
def dsa_week_planner(request):
    if request.user.profile.role != "viewer":
        return HttpResponseForbidden("You do not have permission to view this page.")
    return render(request, "blog/dsa_week_planner.html")


# =========================================================
# ERROR HANDLERS
# =========================================================
def custom_403_view(request, exception=None):
    return render(request, "403.html", status=403)
