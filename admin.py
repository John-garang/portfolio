from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.forms import Textarea
from .models import (
    BlogPost, AcademiaPost, TravelPost, FunStory,
    PostImage, ServiceRequest, NewsletterSubscriber
)

class PostImageInline(GenericTabularInline):
    """Inline admin for post images"""
    model = PostImage
    extra = 1
    fields = ('image', 'alt_text')
    
class AbstractContentAdmin(admin.ModelAdmin):
    """Base admin class for all content types"""
    
    list_display = ('title', 'status', 'publish_date', 'created_at', 'preview_link')
    list_filter = ('status', 'created_at', 'publish_date')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('status', 'publish_date'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [PostImageInline]
    
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 80})},
    }
    
    actions = ['make_published', 'make_draft', 'schedule_for_later']
    
    def preview_link(self, obj):
        """Generate preview link for content"""
        if obj.pk:
            url = reverse('admin:preview_content', args=[obj._meta.label_lower, obj.pk])
            return format_html('<a href="{}" target="_blank">Preview</a>', url)
        return "Save to preview"
    preview_link.short_description = "Preview"
    
    def make_published(self, request, queryset):
        """Bulk action to publish content"""
        updated = queryset.update(
            status='published',
            publish_date=timezone.now()
        )
        self.message_user(request, f'{updated} items published successfully.')
    make_published.short_description = "Publish selected items"
    
    def make_draft(self, request, queryset):
        """Bulk action to make content draft"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} items moved to draft.')
    make_draft.short_description = "Move to draft"
    
    def schedule_for_later(self, request, queryset):
        """Bulk action to schedule content"""
        updated = queryset.update(status='scheduled')
        self.message_user(request, f'{updated} items scheduled.')
    schedule_for_later.short_description = "Schedule for later"

@admin.register(BlogPost)
class BlogPostAdmin(AbstractContentAdmin):
    """Blog post admin"""
    
    list_display = AbstractContentAdmin.list_display + ('category',)
    list_filter = AbstractContentAdmin.list_filter + ('category',)
    search_fields = AbstractContentAdmin.search_fields + ('tags',)
    
    fieldsets = AbstractContentAdmin.fieldsets[0:1] + (
        ('Blog Details', {
            'fields': ('category', 'tags')
        }),
    ) + AbstractContentAdmin.fieldsets[1:]

@admin.register(AcademiaPost)
class AcademiaPostAdmin(AbstractContentAdmin):
    """Academia post admin"""
    
    list_display = AbstractContentAdmin.list_display + ('field_of_study', 'institution')
    list_filter = AbstractContentAdmin.list_filter + ('field_of_study',)
    
    fieldsets = AbstractContentAdmin.fieldsets[0:1] + (
        ('Academic Details', {
            'fields': ('field_of_study', 'institution')
        }),
    ) + AbstractContentAdmin.fieldsets[1:]

@admin.register(TravelPost)
class TravelPostAdmin(AbstractContentAdmin):
    """Travel post admin"""
    
    list_display = AbstractContentAdmin.list_display + ('location', 'travel_date')
    list_filter = AbstractContentAdmin.list_filter + ('location', 'travel_date')
    
    fieldsets = AbstractContentAdmin.fieldsets[0:1] + (
        ('Travel Details', {
            'fields': ('location', 'travel_date')
        }),
    ) + AbstractContentAdmin.fieldsets[1:]

@admin.register(FunStory)
class FunStoryAdmin(AbstractContentAdmin):
    """Fun story admin"""
    
    list_display = AbstractContentAdmin.list_display + ('mood',)
    list_filter = AbstractContentAdmin.list_filter + ('mood',)
    
    fieldsets = AbstractContentAdmin.fieldsets[0:1] + (
        ('Story Details', {
            'fields': ('mood',)
        }),
    ) + AbstractContentAdmin.fieldsets[1:]

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    """Post image admin"""
    
    list_display = ('image_preview', 'alt_text', 'content_object', 'uploaded_at')
    list_filter = ('uploaded_at', 'content_type')
    search_fields = ('alt_text',)
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        """Show image preview in admin"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Preview"

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    """Service request admin"""
    
    list_display = ('full_name', 'email', 'service_type', 'status', 'created_at')
    list_filter = ('status', 'service_type', 'created_at')
    search_fields = ('full_name', 'email', 'service_type', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Client Information', {
            'fields': ('full_name', 'email')
        }),
        ('Request Details', {
            'fields': ('service_type', 'message')
        }),
        ('Status', {
            'fields': ('status', 'created_at')
        }),
    )
    
    actions = ['mark_in_progress', 'mark_completed']
    
    def mark_in_progress(self, request, queryset):
        """Mark requests as in progress"""
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} requests marked as in progress.')
    mark_in_progress.short_description = "Mark as in progress"
    
    def mark_completed(self, request, queryset):
        """Mark requests as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} requests marked as completed.')
    mark_completed.short_description = "Mark as completed"

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """Newsletter subscriber admin"""
    
    list_display = ('email', 'status', 'mailchimp_sync_status', 'subscribed_at')
    list_filter = ('status', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at', 'mailchimp_sync_status')
    ordering = ('-subscribed_at',)
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'status')
        }),
        ('Mailchimp Integration', {
            'fields': ('mailchimp_id', 'mailchimp_sync_status'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('subscribed_at',)
        }),
    )
    
    actions = ['sync_with_mailchimp', 'unsubscribe_selected']
    
    def mailchimp_sync_status(self, obj):
        """Show Mailchimp sync status"""
        if obj.mailchimp_id:
            return format_html(
                '<span style="color: green;">✓ Synced</span>'
            )
        return format_html(
            '<span style="color: orange;">⚠ Not synced</span>'
        )
    mailchimp_sync_status.short_description = "Mailchimp Status"
    
    def sync_with_mailchimp(self, request, queryset):
        """Sync selected subscribers with Mailchimp"""
        from .utils import sync_subscribers_to_mailchimp
        
        try:
            synced_count = sync_subscribers_to_mailchimp(queryset)
            self.message_user(
                request, 
                f'{synced_count} subscribers synced with Mailchimp successfully.'
            )
        except Exception as e:
            self.message_user(
                request, 
                f'Mailchimp sync failed: {str(e)}',
                level='ERROR'
            )
    sync_with_mailchimp.short_description = "Sync with Mailchimp"
    
    def unsubscribe_selected(self, request, queryset):
        """Unsubscribe selected subscribers"""
        updated = queryset.update(status='unsubscribed')
        self.message_user(request, f'{updated} subscribers unsubscribed.')
    unsubscribe_selected.short_description = "Unsubscribe selected"

# Customize admin site
admin.site.site_header = "John Garang Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Content Management Dashboard"