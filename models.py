from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from PIL import Image
import os

class AbstractContent(models.Model):
    """Abstract base model for all content types"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('scheduled', 'Scheduled'),
    ]
    
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, max_length=255, db_index=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    featured_image = models.ImageField(
        upload_to='posts/featured/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    publish_date = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-set publish_date for published content
        if self.status == 'published' and not self.publish_date:
            self.publish_date = timezone.now()
        
        super().save(*args, **kwargs)
        
        # Optimize featured image
        if self.featured_image:
            self._optimize_image(self.featured_image.path)
    
    def _optimize_image(self, image_path):
        """Optimize uploaded images"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Resize if too large
                max_size = (1200, 800)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save with optimization
                img.save(image_path, 'JPEG', quality=85, optimize=True)
        except Exception as e:
            print(f"Image optimization failed: {e}")
    
    def __str__(self):
        return self.title

class BlogPost(AbstractContent):
    """Blog post model"""
    category = models.CharField(max_length=100, db_index=True)
    tags = models.CharField(max_length=255, blank=True)
    
    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        indexes = [
            models.Index(fields=['category', 'status']),
            models.Index(fields=['publish_date', 'status']),
        ]

class AcademiaPost(AbstractContent):
    """Academic post model"""
    field_of_study = models.CharField(max_length=150, db_index=True)
    institution = models.CharField(max_length=150, blank=True)
    
    class Meta:
        verbose_name = "Academia Post"
        verbose_name_plural = "Academia Posts"
        indexes = [
            models.Index(fields=['field_of_study', 'status']),
        ]

class TravelPost(AbstractContent):
    """Travel post model"""
    location = models.CharField(max_length=150, db_index=True)
    travel_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Travel Post"
        verbose_name_plural = "Travel Posts"
        indexes = [
            models.Index(fields=['location', 'status']),
            models.Index(fields=['travel_date']),
        ]

class FunStory(AbstractContent):
    """Fun story model"""
    mood = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = "Fun Story"
        verbose_name_plural = "Fun Stories"

class PostImage(models.Model):
    """Multiple images per post using Generic Foreign Key"""
    image = models.ImageField(
        upload_to='posts/gallery/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    alt_text = models.CharField(max_length=150, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Generic foreign key to link to any content type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        verbose_name = "Post Image"
        verbose_name_plural = "Post Images"
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self._optimize_image(self.image.path)
    
    def _optimize_image(self, image_path):
        """Optimize gallery images"""
        try:
            with Image.open(image_path) as img:
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Smaller size for gallery images
                max_size = (800, 600)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                img.save(image_path, 'JPEG', quality=80, optimize=True)
        except Exception as e:
            print(f"Gallery image optimization failed: {e}")
    
    def __str__(self):
        return f"Image for {self.content_object}"

class ServiceRequest(models.Model):
    """Service request model"""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    service_type = models.CharField(max_length=150, db_index=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        verbose_name = "Service Request"
        verbose_name_plural = "Service Requests"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['service_type', 'status']),
        ]
    
    def __str__(self):
        return f"{self.full_name} - {self.service_type}"

class NewsletterSubscriber(models.Model):
    """Newsletter subscriber model with Mailchimp sync"""
    
    STATUS_CHOICES = [
        ('subscribed', 'Subscribed'),
        ('unsubscribed', 'Unsubscribed'),
    ]
    
    email = models.EmailField(unique=True, db_index=True)
    mailchimp_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='subscribed', db_index=True)
    subscribed_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        ordering = ['-subscribed_at']
        indexes = [
            models.Index(fields=['status', 'subscribed_at']),
        ]
    
    def __str__(self):
        return self.email