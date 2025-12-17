import os
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.template import Template, Context
from django.urls import path
from django.core.management import execute_from_command_line
import sys

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='your-secret-key-here',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'portfolio.db',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        USE_TZ=True,
    )

django.setup()

from django.db import models

class ServiceRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    service_type = models.CharField(max_length=100)
    budget = models.CharField(max_length=50)
    timeline = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = '__main__'

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = '__main__'

def admin_view(request):
    with open('admin_dashboard.html', 'r') as f:
        template_content = f.read()
    
    # Simple replacements for template variables
    service_count = 0
    subscriber_count = 0
    
    try:
        service_count = ServiceRequest.objects.count()
        subscriber_count = NewsletterSubscriber.objects.count()
    except:
        pass
    
    template_content = template_content.replace('{{ service_requests.count }}', str(service_count))
    template_content = template_content.replace('{{ blog_posts.count }}', '0')
    template_content = template_content.replace('{{ newsletter_subscribers.count }}', str(subscriber_count))
    template_content = template_content.replace('{% for request in service_requests|slice:":5" %}', '')
    template_content = template_content.replace('{% empty %}', '')
    template_content = template_content.replace('{% endfor %}', '')
    template_content = template_content.replace('{% for subscriber in newsletter_subscribers %}', '')
    template_content = template_content.replace('{% csrf_token %}', '')
    template_content = template_content.replace('{% url \'admin_create_blog\' %}', '#')
    template_content = template_content.replace('{% url \'admin_create_academic\' %}', '#')
    template_content = template_content.replace('{% url \'admin_create_travel\' %}', '#')
    
    return HttpResponse(template_content)

urlpatterns = [
    path('admin/', admin_view),
]

if __name__ == '__main__':
    from django.core.management.commands.runserver import Command as runserver
    from django.core.management import execute_from_command_line
    
    # Create tables
    from django.core.management.commands.migrate import Command as migrate
    from django.db import connection
    
    with connection.schema_editor() as schema_editor:
        try:
            schema_editor.create_model(ServiceRequest)
            schema_editor.create_model(NewsletterSubscriber)
        except:
            pass
    
    # Start server
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__main__')
    execute_from_command_line(['manage.py', 'runserver', '8000'])