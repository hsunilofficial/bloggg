from django.contrib.auth.models import User
from django.db import models

ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('editor', 'Editor'),
    ('viewer', 'Viewer'),
]

# Required for entire project to work.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')


    def __str__(self):
        return f"{self.user.username} - {self.role}"


# POST MANAGEMENT
class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('pending', 'Pending Review'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.title
