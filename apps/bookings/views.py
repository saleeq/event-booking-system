from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Booking
from .serializers import BookingSerializer
from .exceptions import BookingException


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings.
    """
    queryset = Booking.objects.select_related('event', 'attendee')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['event', 'attendee', 'status']

    def create(self, request, *args, **kwargs):
        """Custom create method to handle booking validation."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = serializer.validated_data['event']

        # Check if event is fully booked
        if event.is_fully_booked:
            raise BookingException(
                "This event is fully booked",
                code=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking."""
        booking = self.get_object()

        if booking.status == 'confirmed':
            return Response(
                {"detail": "Booking is already confirmed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if booking.event.is_fully_booked:
            return Response(
                {"detail": "Event is fully booked"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'confirmed'
        booking.save()

        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking."""
        booking = self.get_object()

        if booking.status == 'cancelled':
            return Response(
                {"detail": "Booking is already cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'cancelled'
        booking.save()

        serializer = self.get_serializer(booking)
        return Response(serializer.data)
