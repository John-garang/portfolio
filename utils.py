import os
import hashlib
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import NewsletterSubscriber
import logging

logger = logging.getLogger(__name__)

class MailchimpAPI:
    """Mailchimp API integration"""
    
    def __init__(self):
        self.api_key = os.getenv('MAILCHIMP_API_KEY')
        self.list_id = os.getenv('MAILCHIMP_LIST_ID')
        self.server = self.api_key.split('-')[-1] if self.api_key else None
        self.base_url = f"https://{self.server}.api.mailchimp.com/3.0"
        
        if not all([self.api_key, self.list_id, self.server]):
            logger.warning("Mailchimp credentials not configured properly")
    
    def _get_headers(self):
        """Get API headers"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def _get_subscriber_hash(self, email):
        """Generate subscriber hash for Mailchimp"""
        return hashlib.md5(email.lower().encode()).hexdigest()
    
    def add_subscriber(self, email, status='subscribed'):
        """Add subscriber to Mailchimp list"""
        if not self.api_key:
            logger.warning("Mailchimp API key not configured")
            return None
        
        url = f"{self.base_url}/lists/{self.list_id}/members"
        
        data = {
            'email_address': email,
            'status': status,
            'timestamp_signup': timezone.now().isoformat()
        }
        
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            
            if response.status_code in [200, 201]:
                result = response.json()
                logger.info(f"Successfully added {email} to Mailchimp")
                return result.get('id')
            else:
                logger.error(f"Mailchimp API error: {response.text}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Mailchimp request failed: {str(e)}")
            return None
    
    def update_subscriber(self, email, status='subscribed'):
        """Update subscriber status in Mailchimp"""
        if not self.api_key:
            return None
        
        subscriber_hash = self._get_subscriber_hash(email)
        url = f"{self.base_url}/lists/{self.list_id}/members/{subscriber_hash}"
        
        data = {'status': status}
        
        try:
            response = requests.patch(url, json=data, headers=self._get_headers())
            
            if response.status_code == 200:
                logger.info(f"Successfully updated {email} in Mailchimp")
                return True
            else:
                logger.error(f"Mailchimp update error: {response.text}")
                return False
                
        except requests.RequestException as e:
            logger.error(f"Mailchimp update failed: {str(e)}")
            return False
    
    def get_subscriber(self, email):
        """Get subscriber info from Mailchimp"""
        if not self.api_key:
            return None
        
        subscriber_hash = self._get_subscriber_hash(email)
        url = f"{self.base_url}/lists/{self.list_id}/members/{subscriber_hash}"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except requests.RequestException as e:
            logger.error(f"Mailchimp get subscriber failed: {str(e)}")
            return None

def sync_subscribers_to_mailchimp(queryset=None):
    """Sync newsletter subscribers with Mailchimp"""
    mailchimp = MailchimpAPI()
    
    if not mailchimp.api_key:
        raise Exception("Mailchimp API credentials not configured")
    
    if queryset is None:
        queryset = NewsletterSubscriber.objects.filter(status='subscribed')
    
    synced_count = 0
    
    for subscriber in queryset:
        try:
            if not subscriber.mailchimp_id:
                # Add new subscriber
                mailchimp_id = mailchimp.add_subscriber(
                    subscriber.email, 
                    'subscribed' if subscriber.status == 'subscribed' else 'unsubscribed'
                )
                
                if mailchimp_id:
                    subscriber.mailchimp_id = mailchimp_id
                    subscriber.save(update_fields=['mailchimp_id'])
                    synced_count += 1
            else:
                # Update existing subscriber
                success = mailchimp.update_subscriber(
                    subscriber.email,
                    'subscribed' if subscriber.status == 'subscribed' else 'unsubscribed'
                )
                
                if success:
                    synced_count += 1
                    
        except Exception as e:
            logger.error(f"Failed to sync {subscriber.email}: {str(e)}")
            continue
    
    return synced_count

def send_service_request_notification(service_request):
    """Send email notification for new service requests"""
    subject = f"New Service Request: {service_request.service_type}"
    
    message = f"""
    New service request received:
    
    Name: {service_request.full_name}
    Email: {service_request.email}
    Service: {service_request.service_type}
    
    Message:
    {service_request.message}
    
    Submitted: {service_request.created_at}
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        logger.info(f"Service request notification sent for {service_request.full_name}")
    except Exception as e:
        logger.error(f"Failed to send service request notification: {str(e)}")

def optimize_content_queries():
    """Utility functions for optimized content queries"""
    
    def get_published_blogs():
        """Get published blog posts with optimized query"""
        from .models import BlogPost
        return BlogPost.objects.select_related().filter(
            status='published',
            publish_date__lte=timezone.now()
        ).order_by('-publish_date')
    
    def get_published_academia():
        """Get published academia posts with optimized query"""
        from .models import AcademiaPost
        return AcademiaPost.objects.select_related().filter(
            status='published',
            publish_date__lte=timezone.now()
        ).order_by('-publish_date')
    
    def get_published_travel():
        """Get published travel posts with optimized query"""
        from .models import TravelPost
        return TravelPost.objects.select_related().filter(
            status='published',
            publish_date__lte=timezone.now()
        ).order_by('-publish_date')
    
    def get_published_fun():
        """Get published fun stories with optimized query"""
        from .models import FunStory
        return FunStory.objects.select_related().filter(
            status='published',
            publish_date__lte=timezone.now()
        ).order_by('-publish_date')
    
    return {
        'blogs': get_published_blogs,
        'academia': get_published_academia,
        'travel': get_published_travel,
        'fun': get_published_fun,
    }

def get_content_with_images(content_obj):
    """Get content object with prefetched images"""
    from django.contrib.contenttypes.models import ContentType
    from .models import PostImage
    
    content_type = ContentType.objects.get_for_model(content_obj)
    images = PostImage.objects.filter(
        content_type=content_type,
        object_id=content_obj.id
    ).order_by('uploaded_at')
    
    return {
        'content': content_obj,
        'images': images
    }

class ContentManager:
    """Content management utilities"""
    
    @staticmethod
    def publish_scheduled_content():
        """Publish scheduled content that's due"""
        from .models import BlogPost, AcademiaPost, TravelPost, FunStory
        
        now = timezone.now()
        models_to_check = [BlogPost, AcademiaPost, TravelPost, FunStory]
        
        total_published = 0
        
        for model in models_to_check:
            published = model.objects.filter(
                status='scheduled',
                publish_date__lte=now
            ).update(status='published')
            
            total_published += published
            
            if published > 0:
                logger.info(f"Published {published} scheduled {model.__name__} items")
        
        return total_published
    
    @staticmethod
    def get_content_stats():
        """Get content statistics for dashboard"""
        from .models import BlogPost, AcademiaPost, TravelPost, FunStory, ServiceRequest
        
        return {
            'blogs': {
                'total': BlogPost.objects.count(),
                'published': BlogPost.objects.filter(status='published').count(),
                'draft': BlogPost.objects.filter(status='draft').count(),
            },
            'academia': {
                'total': AcademiaPost.objects.count(),
                'published': AcademiaPost.objects.filter(status='published').count(),
                'draft': AcademiaPost.objects.filter(status='draft').count(),
            },
            'travel': {
                'total': TravelPost.objects.count(),
                'published': TravelPost.objects.filter(status='published').count(),
                'draft': TravelPost.objects.filter(status='draft').count(),
            },
            'fun': {
                'total': FunStory.objects.count(),
                'published': FunStory.objects.filter(status='published').count(),
                'draft': FunStory.objects.filter(status='draft').count(),
            },
            'service_requests': {
                'total': ServiceRequest.objects.count(),
                'new': ServiceRequest.objects.filter(status='new').count(),
                'in_progress': ServiceRequest.objects.filter(status='in_progress').count(),
                'completed': ServiceRequest.objects.filter(status='completed').count(),
            }
        }