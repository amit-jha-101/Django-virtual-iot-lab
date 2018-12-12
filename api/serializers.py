
from rest_framework import serializers
from .models import Weather_data

class Weather_dataSerializer(serializers.ModelSerializer):
    """
    Serializer to map the model data into JSON format
    """

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Weather_data
        fields = ('id', 'City', 'Temperature', 'time_stamp')
        read_only_fields = ('time_stamp', 'Temperature')