from django.db import models
from django.core.exceptions import ValidationError
from apps.events.models import Event
from apps.attendees.models import Attendee


class Booking(models.Model):
    """Model for event bookings."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['event', 'attendee']  # Prevents duplicate bookings
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.attendee.full_name} - {self.event.title} ({self.status})"

    def clean(self):
        # Check if event has capacity
        if self.status == 'confirmed' and self.event.is_fully_booked:
            # Check if this is an update (not a new booking)
            if not self.pk or self.status != Booking.objects.get(pk=self.pk).status:
                raise ValidationError("Event is fully booked")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
