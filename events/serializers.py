from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    full_address = serializers.CharField(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True) #new item
    

    class Meta: #new item
        model = Event
        fields = ['id', 'name', 'description', 'category', 'category_display', 'street', 'city', 'state', 
                  'zipcode', 'latitude', 'longitude', 'full_address']