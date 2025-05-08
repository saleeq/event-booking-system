from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Country(models.Model):
    """Model for countries where events can take place."""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)  # ISO country code

    class Meta:
        verbose_name_plural = "countries"
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    """Model for events that can be booked by attendees."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='events')
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='created_events')

    class Meta:
        ordering = ['start_datetime']

    def __str__(self):
        return f"{self.title} - {self.location.name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_datetime and self.end_datetime:
            if self.start_datetime >= self.end_datetime:
                raise ValidationError("Start datetime must be before end datetime")
            if self.start_datetime < timezone.now():
                raise ValidationError("Event cannot start in the past")

    @property
    def remaining_capacity(self):
        booked_count = self.bookings.filter(status='confirmed').count()
        return self.capacity - booked_count

    @property
    def is_fully_booked(self):
        return self.remaining_capacity <= 0
