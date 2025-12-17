from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
import json

from .models import (
    BlogPost, AcademiaPost, TravelPost, FunStory,
    ServiceRequest, NewsletterSubscriber, PostImage
)
from .utils import (
    sync_subscribers_to_mailchimp, 
    send_service_request_notification,
    ContentManager,
    get_content_with_images
)

# Public Views
def blog_list(request):
    """Display published blog posts"""
    blogs = BlogPost.objects.filter(
        status='published',
        publish_date__lte=timezone.now()
    ).select_related().order_by('-publish_date')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Category filter
    category = request.GET.get('category')
    if category:
        blogs = blogs.filter(category=category)
    
    # Pagination
    paginator = Paginator(blogs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filter
    categories = BlogPost.objects.filter(
        status='published'
    ).values_list('category', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category,
    }
    
    return render(request, 'blog/list.html', context)

def blog_detail(request, slug):
    """Display individual blog post"""
    blog = get_object_or_404(
        BlogPost,
        slug=slug,
        status='published',
        publish_date__lte=timezone.now()
    )
    
    # Get related images
    content_data = get_content_with_images(blog)
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        category=blog.category,
        status='published',
        publish_date__lte=timezone.now()
    ).exclude(id=blog.id)[:3]
    
    context = {
        'blog': content_data['content'],
        'images': content_data['images'],
        'related_posts': related_posts,
    }
    
    return render(request, 'blog/detail.html', context)

def academia_list(request):
    """Display published academia posts"""
    posts = AcademiaPost.objects.filter(
        status='published',
        publish_date__lte=timezone.now()
    ).select_related().order_by('-publish_date')
    
    # Field of study filter
    field = request.GET.get('field')
    if field:
        posts = posts.filter(field_of_study=field)
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get fields for filter
    fields = AcademiaPost.objects.filter(
        status='published'
    ).values_list('field_of_study', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'fields': fields,
        'selected_field': field,
    }
    
    return render(request, 'academia/list.html', context)

def academia_detail(request, slug):
    """Display individual academia post"""
    post = get_object_or_404(
        AcademiaPost,
        slug=slug,
        status='published',
        publish_date__lte=timezone.now()
    )
    
    content_data = get_content_with_images(post)
    
    context = {
        'post': content_data['content'],
        'images': content_data['images'],
    }
    
    return render(request, 'academia/detail.html', context)

def travel_list(request):
    """Display published travel posts"""
    posts = TravelPost.objects.filter(
        status='published',
        publish_date__lte=timezone.now()
    ).select_related().order_by('-publish_date')
    
    # Location filter
    location = request.GET.get('location')
    if location:
        posts = posts.filter(location__icontains=location)
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_location': location,
    }
    
    return render(request, 'travel/list.html', context)

def travel_detail(request, slug):
    """Display individual travel post"""
    post = get_object_or_404(
        TravelPost,
        slug=slug,
        status='published',
        publish_date__lte=timezone.now()
    )
    
    content_data = get_content_with_images(post)
    
    context = {
        'post': content_data['content'],
        'images': content_data['images'],
    }
    
    return render(request, 'travel/detail.html', context)

def fun_list(request):
    """Display published fun stories"""
    stories = FunStory.objects.filter(
        status='published',
        publish_date__lte=timezone.now()
    ).select_related().order_by('-publish_date')
    
    # Pagination
    paginator = Paginator(stories, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'fun/list.html', context)

def fun_detail(request, slug):
    """Display individual fun story"""
    story = get_object_or_404(
        FunStory,
        slug=slug,
        status='published',
        publish_date__lte=timezone.now()
    )
    
    content_data = get_content_with_images(story)
    
    context = {
        'story': content_data['content'],
        'images': content_data['images'],
    }
    
    return render(request, 'fun/detail.html', context)

# API Views
@csrf_exempt
@require_http_methods(["POST"])
def submit_service_request(request):
    """Handle service request submissions"""
    try:
        data = json.loads(request.body)
        
        service_request = ServiceRequest.objects.create(
            full_name=data.get('full_name', ''),
            email=data.get('email', ''),
            service_type=data.get('service_type', ''),
            message=data.get('message', '')
        )
        
        # Send notification email
        try:
            send_service_request_notification(service_request)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to send notification: {e}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Service request submitted successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def subscribe_newsletter(request):
    """Handle newsletter subscriptions"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        
        if not email:
            return JsonResponse({
                'status': 'error',
                'message': 'Email is required'
            }, status=400)
        
        # Create or update subscriber
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={'status': 'subscribed'}
        )
        
        if not created and subscriber.status == 'unsubscribed':
            subscriber.status = 'subscribed'
            subscriber.save()
        
        # Sync with Mailchimp asynchronously
        try:
            sync_subscribers_to_mailchimp([subscriber])
        except Exception as e:
            # Log error but don't fail the subscription
            print(f"Mailchimp sync failed: {e}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Successfully subscribed to newsletter'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# Admin Views
@staff_member_required
def admin_dashboard(request):
    """Custom admin dashboard"""
    stats = ContentManager.get_content_stats()
    
    # Recent activity
    recent_blogs = BlogPost.objects.order_by('-created_at')[:5]
    recent_requests = ServiceRequest.objects.order_by('-created_at')[:5]
    recent_subscribers = NewsletterSubscriber.objects.order_by('-subscribed_at')[:5]
    
    context = {
        'stats': stats,
        'recent_blogs': recent_blogs,
        'recent_requests': recent_requests,
        'recent_subscribers': recent_subscribers,
    }
    
    return render(request, 'admin/dashboard.html', context)

@staff_member_required
def preview_content(request, content_type, object_id):
    """Preview content before publishing"""
    try:
        app_label, model_name = content_type.split('.')
        content_type_obj = ContentType.objects.get(
            app_label=app_label,
            model=model_name
        )
        
        content_obj = content_type_obj.get_object_for_this_type(id=object_id)
        content_data = get_content_with_images(content_obj)
        
        context = {
            'content': content_data['content'],
            'images': content_data['images'],
            'is_preview': True,
        }
        
        # Determine template based on content type
        template_map = {
            'blogpost': 'blog/detail.html',
            'academiapost': 'academia/detail.html',
            'travelpost': 'travel/detail.html',
            'funstory': 'fun/detail.html',
        }
        
        template = template_map.get(model_name.lower(), 'admin/preview.html')
        
        return render(request, template, context)
        
    except Exception as e:
        return HttpResponse(f"Preview error: {str(e)}", status=400)

@staff_member_required
def bulk_publish_scheduled(request):
    """Manually trigger publishing of scheduled content"""
    if request.method == 'POST':
        published_count = ContentManager.publish_scheduled_content()
        
        messages.success(
            request, 
            f'Successfully published {published_count} scheduled items.'
        )
    
    return redirect('admin:index')

@staff_member_required
def sync_mailchimp(request):
    """Manually sync subscribers with Mailchimp"""
    if request.method == 'POST':
        try:
            subscribers = NewsletterSubscriber.objects.filter(status='subscribed')
            synced_count = sync_subscribers_to_mailchimp(subscribers)
            
            messages.success(
                request,
                f'Successfully synced {synced_count} subscribers with Mailchimp.'
            )
        except Exception as e:
            messages.error(
                request,
                f'Mailchimp sync failed: {str(e)}'
            )
    
    return redirect('admin:portfolio_newslettersubscriber_changelist')

# Content API for frontend
def api_latest_content(request):
    """API endpoint for latest content across all types"""
    blogs = BlogPost.objects.filter(
        status='published',
        publish_date__lte=timezone.now()
    )[:3]
    
    academia = AcademiaPost.objects.filter(
        status='published',
        publish_date__lte=timezone.now()
    )[:3]
    
    travel = TravelPost.objects.filter(
        status='published',
        publish_date__lte=timezone.now()
    )[:3]
    
    fun = FunStory.objects.filter(
        status='published',
        publish_date__lte=timezone.now()
    )[:3]
    
    def serialize_content(items, content_type):
        return [{
            'id': item.id,
            'title': item.title,
            'slug': item.slug,
            'excerpt': item.excerpt,
            'publish_date': item.publish_date.isoformat() if item.publish_date else None,
            'featured_image': item.featured_image.url if item.featured_image else None,
            'type': content_type,
        } for item in items]
    
    data = {
        'blogs': serialize_content(blogs, 'blog'),
        'academia': serialize_content(academia, 'academia'),
        'travel': serialize_content(travel, 'travel'),
        'fun': serialize_content(fun, 'fun'),
    }
    
    return JsonResponse(data)