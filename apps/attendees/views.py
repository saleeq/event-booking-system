from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Attendee
from .serializers import AttendeeSerializer
from apps.bookings.serializers import BookingSerializer


class AttendeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing attendees.
    No authentication required for registration.
    """
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']

    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Get all bookings for a specific attendee."""
        attendee = self.get_object()
        bookings = attendee.bookings.select_related('event')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
