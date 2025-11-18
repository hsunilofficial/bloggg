# blog/urls_admin.py  (CUSTOM ADMIN DASHBOARD)
from django.urls import path
from blog import views

urlpatterns = [

    # Dashboard & Settings
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analytics/', views.analytics, name='analytics'),
    path('settings/', views.settings_page, name='settings'),

    # User Management
    path('users/', views.admin_users, name='admin_users'),
    path('users/manage/', views.manage_users, name='manage_users'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('users/<int:user_id>/view/', views.view_user, name='view_user'),
    path('users/roles/', views.user_roles, name='user_roles'),

    # Post Management
    path('posts/', views.posts, name='posts'),
    path('posts/add/', views.add_post, name='add_post'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/pending/', views.pending_posts, name='pending_posts'),

    # viewer tools
    path('dsa-week-planner/', views.dsa_week_planner, name='dsa_week_planner'),
]
