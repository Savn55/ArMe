import requests
import math
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer


# Add this new view
def home_view(request):
    return render(request, 'index.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })


class SearchEventsView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        category = request.query_params.get('category', '') #category codes
        
        # if not query and not category: #category codes
        #  not category
        #     return Response([])
        

         # Start with all events #category codes
         
        events = Event.objects.all()
        # Search for events with names containing the query
        # events = Event.objects.filter(name__icontains=query)
        
        if query:#category codes
            
            # Search in multiple fields
            events = Event.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(city__icontains=query)
            )
        #category codes
        
         # Filter by category if provided and not 'ALL'
        if category and category != 'ALL':
            events = events.filter(category=category)
        

        # For events without coordinates, geocode them
        for event in events:
            if event.latitude is None or event.longitude is None:
                self.geocode_event(event)
        
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def geocode_event(self, event):
        address = event.full_address()
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={settings.GOOGLE_MAPS_API_KEY}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if data['status'] == 'OK':
                location = data['results'][0]['geometry']['location']
                event.latitude = location['lat']
                event.longitude = location['lng']
                event.save()
        except Exception as e:
            print(f"Geocoding error: {e}")

class NearbyEventsView(APIView):
    def get(self, request):
        #category codes
        
        try:
            lat = float(request.query_params.get('latitude', 0))
            lng = float(request.query_params.get('longitude', 0))
            radius = float(request.query_params.get('radius', 10))  # Default 10km
            category = request.query_params.get('category', '')
            
            # Start with events that have coordinates
            events_query = Event.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
            
            # Filter by category if provided and not 'ALL'
            if category and category != 'ALL':
                events_query = events_query.filter(category=category)
            
            # Get the filtered events
            events = events_query
            
            # Filter events within radius using Haversine formula
            nearby_events = []
            for event in events:
                distance = self.haversine(lat, lng, event.latitude, event.longitude)
                if distance <= radius:
                    nearby_events.append(event)
            
            serializer = EventSerializer(nearby_events, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        '''
        try:
            lat = float(request.query_params.get('latitude', 0))
            lng = float(request.query_params.get('longitude', 0))
            radius = float(request.query_params.get('radius', 10))  # Default 10km
            
            # Only consider events with coordinates
            events = Event.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
            
            # Filter events within radius using Haversine formula
            nearby_events = []
            for event in events:
                distance = self.haversine(lat, lng, event.latitude, event.longitude)
                if distance <= radius:
                    nearby_events.append(event)
            
            serializer = EventSerializer(nearby_events, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
    '''
    def haversine(self, lat1, lon1, lat2, lon2):
        # Calculate distance between two points on Earth (in kilometers)
        R = 6371  # Earth radius in kilometers
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat/2) * math.sin(dlat/2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon/2) * math.sin(dlon/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance