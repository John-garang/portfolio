from django.contrib import admin
from .models import BlogPost, ServiceRequest

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