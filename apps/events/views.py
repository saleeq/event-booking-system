from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, Country
from .serializers import EventSerializer, CountrySerializer
from .permissions import IsEventCreatorOrReadOnly
from ..bookings.serializers import BookingSerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing countries.
    Only list and retrieve operations are allowed.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsEventCreatorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'is_active', 'start_datetime']
    search_fields = ['title', 'description']
    ordering_fields = ['start_datetime', 'price', 'capacity']
    ordering = ['start_datetime']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Get all bookings for a specific event."""
        event = self.get_object()
        bookings = event.bookings.select_related('attendee')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all events that are not fully booked."""
        available_events = [
            event for event in self.get_queryset()
            if not event.is_fully_booked and event.is_active
        ]
        serializer = self.get_serializer(available_events, many=True)
        return Response(serializer.data)
