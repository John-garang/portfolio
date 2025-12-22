from django.urls import path
from django.contrib import admin
from portfolio_app import (
    admin_dashboard, add_blog_post, add_academic_work, 
    add_travel_story, submit_service_request, subscribe_newsletter
)
# from blog_views import (
#     blogs_view, academia_view, travels_view,
#     blog_detail, academic_detail, travel_detail
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('', admin_dashboard, name='home'),
    path('admin-panel/', admin_dashboard, name='admin_panel'),
    # path('blogs/', blogs_view, name='blogs'),
    # path('academia/', academia_view, name='academia'),
    # path('travels/', travels_view, name='travels'),
    # path('blog/<int:blog_id>/', blog_detail, name='blog_detail'),
    # path('academic/<int:work_id>/', academic_detail, name='academic_detail'),
    # path('travel/<int:story_id>/', travel_detail, name='travel_detail'),
    path('add-blog/', add_blog_post, name='add_blog'),
    path('add-academic/', add_academic_work, name='add_academic'),
    path('add-travel/', add_travel_story, name='add_travel'),
    path('submit-request/', submit_service_request, name='submit_request'),
    path('subscribe/', subscribe_newsletter, name='subscribe'),
]