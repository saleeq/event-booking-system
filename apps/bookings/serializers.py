from rest_framework import serializers
from .models import Booking
from apps.events.serializers import EventSerializer
from apps.attendees.serializers import AttendeeSerializer


class BookingSerializer(serializers.ModelSerializer):
    event_details = EventSerializer(source='event', read_only=True)
    attendee_details = AttendeeSerializer(source='attendee', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'event', 'attendee', 'status', 'booking_date',
            'updated_at', 'event_details', 'attendee_details'
        ]
        read_only_fields = ['booking_date', 'updated_at']

    def validate(self, data):
        # Check if event is active
        if 'event' in data and not data['event'].is_active:
            raise serializers.ValidationError(
                "Cannot book an inactive event"
            )

        # Check for duplicate booking (handled by unique_together, but custom message)
        if self.instance is None:  # Only check for new bookings
            if Booking.objects.filter(
                    event=data.get('event'),
                    attendee=data.get('attendee')
            ).exists():
                raise serializers.ValidationError(
                    "Attendee has already booked this event"
                )

        return data
