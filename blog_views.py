from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from portfolio_app import BlogPost, AcademicWork, TravelStory

def blogs_view(request):
    blogs = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blogs_dynamic.html', {'blogs': blogs})

def academia_view(request):
    academic_works = AcademicWork.objects.all().order_by('-created_at')
    return render(request, 'academia_dynamic.html', {'academic_works': academic_works})

def travels_view(request):
    travel_stories = TravelStory.objects.all().order_by('-created_at')
    return render(request, 'travels_dynamic.html', {'travel_stories': travel_stories})

def blog_detail(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

def academic_detail(request, work_id):
    work = get_object_or_404(AcademicWork, id=work_id)
    return render(request, 'academic_detail.html', {'work': work})

def travel_detail(request, story_id):
    story = get_object_or_404(TravelStory, id=story_id)
    return render(request, 'travel_detail.html', {'story': story})