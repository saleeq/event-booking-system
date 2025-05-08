from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.events.models import Event, Country
from apps.attendees.models import Attendee
from apps.bookings.models import Booking
from datetime import datetime, timedelta
from django.utils import timezone


class BookingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.country = Country.objects.create(
            name='United States',
            code='US'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            start_datetime=timezone.now() + timedelta(days=7),
            end_datetime=timezone.now() + timedelta(days=8),
            location=self.country,
            capacity=2,
            price=50.00,
            created_by=self.user
        )
        self.attendee = Attendee.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            date_of_birth='1990-01-01'
        )

    def test_create_booking(self):
        self.client.force_authenticate(user=self.user)
        booking_data = {
            'event': self.event.id,
            'attendee': self.attendee.id
        }
        response = self.client.post('/api/bookings/', booking_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_booking(self):
        self.client.force_authenticate(user=self.user)
        Booking.objects.create(
            event=self.event,
            attendee=self.attendee
        )
        booking_data = {
            'event': self.event.id,
            'attendee': self.attendee.id
        }
        response = self.client.post('/api/bookings/', booking_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_overbooking(self):
        self.client.force_authenticate(user=self.user)
        # Create attendees and book the event to capacity
        for i in range(self.event.capacity):
            attendee = Attendee.objects.create(
                first_name=f'User{i}',
                last_name=f'Test{i}',
                email=f'user{i}@example.com',
                phone=f'123456789{i}',
                date_of_birth='1990-01-01'
            )
            Booking.objects.create(
                event=self.event,
                attendee=attendee,
                status='confirmed'
            )

        # Try to book one more
        new_attendee = Attendee.objects.create(
            first_name='Extra',
            last_name='User',
            email='extra@example.com',
            phone='9876543210',
            date_of_birth='1990-01-01'
        )
        booking_data = {
            'event': self.event.id,
            'attendee': new_attendee.id
        }
        response = self.client.post('/api/bookings/', booking_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
