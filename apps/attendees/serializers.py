from rest_framework import serializers
from .models import Attendee
from datetime import date


class AttendeeSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Attendee
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'full_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Date of birth cannot be in the future"
            )
        return value
