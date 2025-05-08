from rest_framework import serializers
from .models import Event, Country
from django.utils import timezone


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code']


class EventSerializer(serializers.ModelSerializer):
    location = CountrySerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source='location', write_only=True
    )
    remaining_capacity = serializers.ReadOnlyField()
    is_fully_booked = serializers.ReadOnlyField()
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'start_datetime', 'end_datetime',
            'location', 'location_id', 'capacity', 'price', 'is_active',
            'remaining_capacity', 'is_fully_booked', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Validate datetime fields
        if 'start_datetime' in data and 'end_datetime' in data:
            if data['start_datetime'] >= data['end_datetime']:
                raise serializers.ValidationError(
                    "Start datetime must be before end datetime"
                )

        # Validate that event doesn't start in the past
        if 'start_datetime' in data and data['start_datetime'] < timezone.now():
            raise serializers.ValidationError(
                "Event cannot start in the past"
            )

        return data
