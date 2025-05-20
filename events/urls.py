from django.urls import path
from .views import SearchEventsView, NearbyEventsView

urlpatterns = [
    path('api/search-events/', SearchEventsView.as_view(), name='search-events'),
    path('api/nearby-events/', NearbyEventsView.as_view(), name='nearby-events'),
]