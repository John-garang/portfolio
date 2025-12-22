from django.db import models
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count
from datetime import datetime, timedelta

# Models
class ServiceRequest(models.Model):
    class Meta:
        app_label = 'portfolio_app'
    STATUS_CHOICES = [
        ('new', 'New'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    SERVICE_CHOICES = [
        ('web-development', 'Web Development'),
        ('graphic-design', 'Graphic Design'),
        ('ghost-writing', 'Ghost Writing'),
    ]
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    budget = models.CharField(max_length=20)
    timeline = models.CharField(max_length=20)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.full_name} - {self.service}"

class BlogPost(models.Model):
    class Meta:
        app_label = 'portfolio_app'
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    content = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

class AcademicWork(models.Model):
    class Meta:
        app_label = 'portfolio_app'
    TYPE_CHOICES = [
        ('research', 'Research Paper'),
        ('essay', 'Academic Essay'),
        ('analysis', 'Analysis'),
    ]
    
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    content = models.TextField()
    work_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

class TravelStory(models.Model):
    class Meta:
        app_label = 'portfolio_app'
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    excerpt = models.TextField()
    content = models.TextField()
    travel_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.title} - {self.location}"

class NewsletterSubscriber(models.Model):
    class Meta:
        app_label = 'portfolio_app'
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email

# Views
def admin_dashboard(request):
    from django.http import HttpResponse
    with open('simple_dashboard.html', 'r') as f:
        html_content = f.read()
    return HttpResponse(html_content)

def add_blog_post(request):
    if request.method == 'POST':
        blog_post = BlogPost.objects.create(
            title=request.POST['title'],
            excerpt=request.POST['excerpt'],
            content=request.POST['content'],
            date=request.POST['date']
        )
        messages.success(request, 'Blog post published successfully!')
        return redirect('admin_dashboard')
    
    return redirect('admin_dashboard')

def add_academic_work(request):
    if request.method == 'POST':
        academic_work = AcademicWork.objects.create(
            title=request.POST['title'],
            abstract=request.POST['abstract'],
            content=request.POST['content'],
            work_type=request.POST['work_type']
        )
        messages.success(request, 'Academic work published successfully!')
        return redirect('admin_dashboard')
    
    return redirect('admin_dashboard')

def add_travel_story(request):
    if request.method == 'POST':
        travel_story = TravelStory.objects.create(
            title=request.POST['title'],
            location=request.POST['location'],
            excerpt=request.POST['excerpt'],
            content=request.POST['content'],
            travel_date=request.POST['travel_date']
        )
        messages.success(request, 'Travel story published successfully!')
        return redirect('admin_dashboard')
    
    return redirect('admin_dashboard')

def submit_service_request(request):
    if request.method == 'POST':
        service_request = ServiceRequest.objects.create(
            full_name=request.POST['fullName'],
            email=request.POST['email'],
            phone=request.POST.get('phone', ''),
            company=request.POST.get('company', ''),
            service=request.POST['service'],
            budget=request.POST.get('budget', ''),
            timeline=request.POST.get('timeline', ''),
            description=request.POST['projectDescription']
        )
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            if created:
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'exists'})
    
    return JsonResponse({'status': 'error'})