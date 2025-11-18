# blog/urls.py  (PUBLIC SITE URLS)
from django.urls import path
from blog import views

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
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Forgot Password
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
]
