"""
Main URL configuration for School Management System.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from config.landing import LandingPageView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('login/', RedirectView.as_view(url='users/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls', namespace='users')),
    path('dashboard/', include('apps.users.dashboard_urls', namespace='dashboard')),
    path('students/', include('apps.students.urls', namespace='students')),
    path('teachers/', include('apps.teachers.urls', namespace='teachers')),
    path('academics/', include('apps.academics.urls', namespace='academics')),
    path('attendance/', include('apps.attendance.urls', namespace='attendance')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
