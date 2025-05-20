from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from events.views import home_view 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    # path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('', include('events.urls')),
]