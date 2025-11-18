# personal_blog/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    # Django's default admin
    path('admin/', admin.site.urls),

    # Public website URLs
    path('', include('blog.urls')),    

    # Custom admin dashboard
    path('admin-dashboard/', include('blog.urls_admin')),
]



