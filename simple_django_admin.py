import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='django-insecure-portfolio-admin-key',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'portfolio_admin.db',
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
        ROOT_URLCONF='simple_django_admin',
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
from django.contrib.auth.models import User

# Simple models for content management
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100)
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

# Register models with admin
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'service_type', 'created_at')
    list_filter = ('service_type', 'created_at')
    search_fields = ('full_name', 'email')
    readonly_fields = ('created_at',)

# URL configuration
urlpatterns = [
    path('admin/', admin.site.urls),
]

if __name__ == '__main__':
    # Create tables
    from django.core.management.commands.migrate import Command as MigrateCommand
    from django.db import connection
    
    with connection.schema_editor() as schema_editor:
        try:
            schema_editor.create_model(BlogPost)
            schema_editor.create_model(ServiceRequest)
        except Exception as e:
            print(f"Tables may already exist: {e}")
    
    # Create superuser if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'j.garang@alustudent.com', 'John123')
        print("Superuser 'admin' created with password 'John123'")
    
    # Run server
    import sys
    sys.argv = ['manage.py', 'runserver', '8000']
    execute_from_command_line(sys.argv)