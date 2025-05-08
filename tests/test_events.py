from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.events.models import Event, Country


class EventTests(TestCase):
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
        self.event_data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'start_datetime': (timezone.now() + timedelta(days=7)).isoformat(),
            'end_datetime': (timezone.now() + timedelta(days=8)).isoformat(),
            'location_id': self.country.id,
            'capacity': 100,
            'price': '50.00'
        }

    def test_create_event_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/events/events/', self.event_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)

    def test_create_event_unauthenticated(self):
        response = self.client.post('/api/events/events/', self.event_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_events(self):
        response = self.client.get('/api/events/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_date_range(self):
        self.client.force_authenticate(user=self.user)
        invalid_data = self.event_data.copy()
        invalid_data['end_datetime'] = invalid_data['start_datetime']
        response = self.client.post('/api/events/events/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
