# blog/urls.py  (PUBLIC SITE URLS)
from django.urls import path
from blog import views
rom django.contrib.auth import views as auth_views

urlpatterns = [
    # Public Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Public Blog
    path('posts/', views.public_posts, name='public_posts'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/', views.view_post, name='view_post'),

    # Authentication
    path('accounts/login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('accounts/signup/',auth_views.LogoutView.as_view(template_name='blog/signup.html'),name='signup'),
    path('accounts/logout/',auth_views.LogoutView.as_view(template_name='blog/logout.html'),name='logout'),

    # Forgot Password
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
]
