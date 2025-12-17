#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Configure Django
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='quick-admin-key',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'quick_admin.db',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
        ],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ],
        ROOT_URLCONF='__main__',
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }],
        STATIC_URL='/static/',
        USE_TZ=True,
    )

django.setup()

from django.contrib import admin
from django.urls import path
from django.db import models
from django.core.management import execute_from_command_line

# Models
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100, default='General')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        app_label = '__main__'

class ServiceRequest(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    service_type = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.service_type}"
    
    class Meta:
        app_label = '__main__'

# Admin
admin.site.register(BlogPost)
admin.site.register(ServiceRequest)

# URLs
urlpatterns = [
    path('admin/', admin.site.urls),
]

if __name__ == '__main__':
    # Setup database
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser
    from django.contrib.auth.models import User
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'j.garang@alustudent.com', 'John123')
            print("✅ Admin user created: admin / John123")
    except:
        pass
    
    print("🚀 Starting admin at http://127.0.0.1:8000/admin/")
    print("📧 Login: admin / John123")
    
    # Start server
    execute_from_command_line(['manage.py', 'runserver', '8000'])