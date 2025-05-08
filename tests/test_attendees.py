from datetime import timedelta, date

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.attendees.models import Attendee
from apps.bookings.models import Booking
from apps.events.models import Event, Country


class AttendeeTests(TestCase):
    def setUp(self):
        """Set up test data before each test method."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Create test attendee data
        self.attendee_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '+1234567890',
            'date_of_birth': '1990-01-01'
        }

        # Create a test attendee
        self.attendee = Attendee.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone='+1987654321',
            date_of_birth='1985-05-15'
        )

        # Create test event data for booking tests
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
            capacity=100,
            price=50.00,
            created_by=self.user
        )

    def test_create_attendee_no_auth_required(self):
        """Test that attendees can be created without authentication."""
        response = self.client.post('/api/attendees/', self.attendee_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendee.objects.count(), 2)  # Including the one from setUp

        # Verify the created attendee data
        created_attendee = Attendee.objects.get(email=self.attendee_data['email'])
        self.assertEqual(created_attendee.first_name, self.attendee_data['first_name'])
        self.assertEqual(created_attendee.last_name, self.attendee_data['last_name'])
        self.assertEqual(created_attendee.phone, self.attendee_data['phone'])

    def test_list_attendees(self):
        """Test listing all attendees."""
        response = self.client.get('/api/attendees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Pagination is applied

    def test_retrieve_attendee(self):
        """Test retrieving a specific attendee."""
        response = self.client.get(f'/api/attendees/{self.attendee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.attendee.email)
        self.assertEqual(response.data['full_name'], 'Jane Smith')

    def test_update_attendee(self):
        """Test updating an attendee."""
        update_data = {
            'first_name': 'Jane',
            'last_name': 'Johnson',  # Changed last name
            'email': 'jane.smith@example.com',
            'phone': '+1987654321',
            'date_of_birth': '1985-05-15'
        }
        response = self.client.put(f'/api/attendees/{self.attendee.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the update
        updated_attendee = Attendee.objects.get(id=self.attendee.id)
        self.assertEqual(updated_attendee.last_name, 'Johnson')

    def test_partial_update_attendee(self):
        """Test partial update of an attendee."""
        update_data = {'phone': '+1555555555'}
        response = self.client.patch(f'/api/attendees/{self.attendee.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the update
        updated_attendee = Attendee.objects.get(id=self.attendee.id)
        self.assertEqual(updated_attendee.phone, '+1555555555')

    def test_delete_attendee(self):
        """Test deleting an attendee."""
        response = self.client.delete(f'/api/attendees/{self.attendee.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Attendee.objects.count(), 0)

    def test_create_attendee_duplicate_email(self):
        """Test that duplicate emails are not allowed."""
        duplicate_data = self.attendee_data.copy()
        duplicate_data['email'] = self.attendee.email  # Use existing email

        response = self.client.post('/api/attendees/', duplicate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_create_attendee_invalid_email(self):
        """Test that invalid email formats are rejected."""
        invalid_data = self.attendee_data.copy()
        invalid_data['email'] = 'invalid-email'

        response = self.client.post('/api/attendees/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_create_attendee_future_birth_date(self):
        """Test that future birth dates are rejected."""
        invalid_data = self.attendee_data.copy()
        invalid_data['date_of_birth'] = (date.today() + timedelta(days=1)).isoformat()

        response = self.client.post('/api/attendees/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date_of_birth', response.data)

    def test_attendee_bookings_endpoint(self):
        """Test the attendee bookings endpoint."""
        # Create a booking for the attendee
        booking = Booking.objects.create(
            event=self.event,
            attendee=self.attendee,
            status='confirmed'
        )

        response = self.client.get(f'/api/attendees/{self.attendee.id}/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], booking.id)
        self.assertEqual(response.data[0]['event'], self.event.id)

    def test_search_attendees(self):
        """Test searching attendees by name or email."""
        # Create additional attendees for search testing
        Attendee.objects.create(
            first_name='John',
            last_name='Johnson',
            email='john.johnson@example.com',
            phone='+1234567890',
            date_of_birth='1992-03-20'
        )

        # Search by first name
        response = self.client.get('/api/attendees/?search=John')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # Search by email
        response = self.client.get('/api/attendees/?search=jane.smith')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['email'], 'jane.smith@example.com')

    def test_attendee_full_name_property(self):
        """Test that the full_name property is correctly returned."""
        response = self.client.get(f'/api/attendees/{self.attendee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], f"{self.attendee.first_name} {self.attendee.last_name}")

    def test_attendee_str_representation(self):
        """Test the string representation of an attendee."""
        expected_str = f"{self.attendee.first_name} {self.attendee.last_name} ({self.attendee.email})"
        self.assertEqual(str(self.attendee), expected_str)

    def test_create_attendee_missing_required_fields(self):
        """Test that all required fields must be provided."""
        incomplete_data = {
            'first_name': 'John',
            # Missing last_name, email, phone, date_of_birth
        }

        response = self.client.post('/api/attendees/', incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that all required fields are in the error response
        required_fields = ['last_name', 'email', 'phone', 'date_of_birth']
        for field in required_fields:
            self.assertIn(field, response.data)

    def test_pagination(self):
        """Test that pagination works correctly."""
        # Create multiple attendees to test pagination
        for i in range(25):  # Create 25 more attendees (total 26)
            Attendee.objects.create(
                first_name=f'User{i}',
                last_name=f'Test{i}',
                email=f'user{i}@example.com',
                phone=f'+123456789{i}',
                date_of_birth='1990-01-01'
            )

        response = self.client.get('/api/attendees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 20)  # Default page size
        self.assertIn('next', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 26)

    def test_ordering(self):
        """Test that attendees are ordered by last_name, first_name."""
        # Create attendees with different names
        Attendee.objects.create(
            first_name='Alice',
            last_name='Brown',
            email='alice@example.com',
            phone='+1234567890',
            date_of_birth='1990-01-01'
        )
        Attendee.objects.create(
            first_name='Bob',
            last_name='Brown',
            email='bob@example.com',
            phone='+1234567890',
            date_of_birth='1990-01-01'
        )

        response = self.client.get('/api/attendees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check ordering
        results = response.data['results']
        self.assertEqual(results[0]['last_name'], 'Brown')
        self.assertEqual(results[0]['first_name'], 'Alice')  # Alice comes before Bob
        self.assertEqual(results[1]['last_name'], 'Brown')
        self.assertEqual(results[1]['first_name'], 'Bob')

    def tearDown(self):
        """Clean up after each test."""
        Attendee.objects.all().delete()
        Event.objects.all().delete()
        Country.objects.all().delete()
        User.objects.all().delete()
