# Event Booking System API

A lightweight RESTful API for managing events, attendees, and bookings built with Django REST Framework. This system provides a complete solution for event management with features like capacity control, duplicate booking prevention, and comprehensive search capabilities.

## 🚀 Features

### Core Functionality
- **Event Management**: Create, read, update, and delete events with capacity tracking
- **Attendee Registration**: Public registration system with no authentication required
- **Booking System**: Secure booking management with duplicate prevention and overbooking protection
- **Location Management**: Country-based event locations

### Advanced Features
- **JWT Authentication**: Secure API access with token-based authentication
- **Automatic Capacity Management**: Real-time tracking of available spots
- **Search & Filtering**: Advanced search across events and attendees
- **Pagination**: Efficient data retrieval for large datasets
- **API Documentation**: Interactive Swagger/OpenAPI documentation
- **Custom Permissions**: Role-based access control for event creators

### Business Logic
- Prevents duplicate bookings for the same attendee and event
- Automatically manages event capacity to prevent overbooking
- Validates event dates (events cannot start in the past)
- Supports booking status management (pending, confirmed, cancelled)

## 🛠️ Tech Stack

- Django 5.1
- Django REST Framework
- SQLite Database (lightweight deployment)
- Simple JWT for authentication
- drf-yasg for API documentation
- python-decouple for configuration management

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git (for cloning the repository)
- Docker (optional, for containerized deployment)

## 🔧 Installation & Setup

### Option 1: Traditional Setup

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd event-booking-system
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Environment Configuration

Create a `.env` file in the project root with the following content:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### 5. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# The SQLite database will be created automatically
```

#### 6. Load Initial Data (Optional)

If you have fixture files or want to create initial data:

```bash
# Create sample countries
python manage.py shell
>>> from apps.events.models import Country
>>> Country.objects.create(name="United States", code="US")
>>> Country.objects.create(name="United Kingdom", code="UK")
>>> Country.objects.create(name="Canada", code="CA")
>>> exit()
```

#### 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### 8. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

### Option 2: Docker Setup

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd event-booking-system
```

#### 2. Environment Configuration

Create a `.env` file in the project root with the following content:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

#### 3. Build and Run with Docker

```bash
# Build the Docker image
docker build -t event-booking-api .

# Run the container
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key-here \
  -e DEBUG=True \
  -e ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0 \
  event-booking-api

# Or run with volume mount for development
docker run -p 8000:8000 \
  -v $(pwd):/app \
  -e SECRET_KEY=your-secret-key-here \
  -e DEBUG=True \
  -e ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0 \
  event-booking-api
```

#### 4. Run Database Migrations in Docker

```bash
# Run migrations
docker exec -it <container_id> python manage.py migrate

# Create superuser
docker exec -it <container_id> python manage.py createsuperuser

# Or use the existing admin credentials (username: admin, password: admin)
```

#### 5. Docker Compose (Alternative)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=your-secret-key-here
      - DEBUG=True
      - ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
    volumes:
      - .:/app
      - ./db.sqlite3:/app/db.sqlite3
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn core.wsgi:application --bind 0.0.0.0:8000"
```

Then run:

```bash
# Build and start services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop services
docker-compose down
```

## 🔐 Authentication

### Admin Access
- **Username**: `admin`
- **Password**: `admin`
- **Admin Panel**: http://127.0.0.1:8000/admin/

### JWT Authentication

To obtain JWT tokens:

```bash
# Get access token
curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin"}'

# Use the token in requests
curl -X GET http://127.0.0.1:8000/api/events/events/ \
     -H "Authorization: Bearer <your-access-token>"
```

## 📡 API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Events
- `GET /api/events/events/` - List all events
- `POST /api/events/events/` - Create a new event (auth required)
- `GET /api/events/events/{id}/` - Retrieve specific event
- `PUT /api/events/events/{id}/` - Update event (creator only)
- `DELETE /api/events/events/{id}/` - Delete event (creator only)
- `GET /api/events/events/{id}/bookings/` - Get event bookings
- `GET /api/events/events/available/` - Get available events

### Attendees
- `GET /api/attendees/` - List all attendees
- `POST /api/attendees/` - Register new attendee (no auth)
- `GET /api/attendees/{id}/` - Retrieve specific attendee
- `PUT /api/attendees/{id}/` - Update attendee
- `DELETE /api/attendees/{id}/` - Delete attendee
- `GET /api/attendees/{id}/bookings/` - Get attendee bookings

### Bookings
- `GET /api/bookings/` - List all bookings (auth required)
- `POST /api/bookings/` - Create booking (auth required)
- `GET /api/bookings/{id}/` - Retrieve specific booking
- `PUT /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Delete booking
- `POST /api/bookings/{id}/confirm/` - Confirm booking
- `POST /api/bookings/{id}/cancel/` - Cancel booking

### Countries
- `GET /api/events/countries/` - List all countries
- `GET /api/events/countries/{id}/` - Retrieve specific country

### API Documentation
- `GET /swagger/` - Swagger UI documentation
- `GET /redoc/` - ReDoc documentation

## 🔍 Usage Examples

### Create an Event

```bash
curl -X POST http://127.0.0.1:8000/api/events/events/ \
     -H "Authorization: Bearer <your-token>" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Django Conference 2024",
       "description": "Annual Django developers conference",
       "start_datetime": "2024-06-15T09:00:00Z",
       "end_datetime": "2024-06-17T18:00:00Z",
       "location_id": 1,
       "capacity": 500,
       "price": "299.99"
     }'
```

### Register an Attendee

```bash
curl -X POST http://127.0.0.1:8000/api/attendees/ \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "John",
       "last_name": "Doe",
       "email": "john.doe@example.com",
       "phone": "+1234567890",
       "date_of_birth": "1990-01-01"
     }'
```

### Create a Booking

```bash
curl -X POST http://127.0.0.1:8000/api/bookings/ \
     -H "Authorization: Bearer <your-token>" \
     -H "Content-Type: application/json" \
     -d '{
       "event": 1,
       "attendee": 1,
       "status": "pending"
     }'
```

### Search Events

```bash
# Search by title or description
curl "http://127.0.0.1:8000/api/events/events/?search=django"

# Filter by location
curl "http://127.0.0.1:8000/api/events/events/?location=1"

# Filter by active status
curl "http://127.0.0.1:8000/api/events/events/?is_active=true"
```

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.events
python manage.py test apps.attendees
python manage.py test apps.bookings

# Run tests in Docker
docker exec -it <container_id> python manage.py test
```

## 📁 Project Structure

```
event-booking-system/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── db.sqlite3
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── __init__.py
│   ├── events/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   ├── attendees/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   └── bookings/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── tests.py
├── static/
└── media/
```

## 🐳 Docker Configuration

### Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Building and Running

```bash
# Build the image
docker build -t event-booking-api .

# Run the container
docker run -p 8000:8000 event-booking-api

# Run with environment variables
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=yourdomain.com \
  event-booking-api

# Run with persistent SQLite database
docker run -p 8000:8000 \
  -v $(pwd)/db.sqlite3:/app/db.sqlite3 \
  event-booking-api
```

### Docker Commands Reference

```bash
# View logs
docker logs <container_id>

# Execute commands in container
docker exec -it <container_id> python manage.py shell

# Stop container
docker stop <container_id>

# Remove container
docker rm <container_id>

# Remove image
docker rmi event-booking-api
```

## 🔒 Security Considerations

- JWT tokens expire after 60 minutes
- Refresh tokens expire after 1 day
- All event management operations require authentication
- Event updates/deletions restricted to creators
- Input validation at model and serializer levels
- SQL injection protection through Django ORM

## 🚦 API Response Examples

### Successful Event Creation
```json
{
    "id": 1,
    "title": "Django Conference 2024",
    "description": "Annual Django developers conference",
    "start_datetime": "2024-06-15T09:00:00Z",
    "end_datetime": "2024-06-17T18:00:00Z",
    "location": {
        "id": 1,
        "name": "United States",
        "code": "US"
    },
    "capacity": 500,
    "price": "299.99",
    "is_active": true,
    "remaining_capacity": 500,
    "is_fully_booked": false,
    "created_by": "admin",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
}
```

### Error Response (Duplicate Booking)
```json
{
    "non_field_errors": [
        "Attendee has already booked this event"
    ]
}
```

## 🔄 Common Operations

### Check Event Availability
```bash
# Get all available events (not fully booked and active)
curl http://127.0.0.1:8000/api/events/events/available/
```

### Confirm a Booking
```bash
curl -X POST http://127.0.0.1:8000/api/bookings/1/confirm/ \
     -H "Authorization: Bearer <your-token>"
```

### Get Attendee's Bookings
```bash
curl http://127.0.0.1:8000/api/attendees/1/bookings/
```

## 📊 Database Schema

### Events Table
- `id`: Primary key
- `title`: Event name
- `description`: Event details
- `start_datetime`: Event start time
- `end_datetime`: Event end time
- `location_id`: Foreign key to Country
- `capacity`: Maximum attendees
- `price`: Event cost
- `is_active`: Boolean flag
- `created_by`: Foreign key to User
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Attendees Table
- `id`: Primary key
- `first_name`: First name
- `last_name`: Last name
- `email`: Unique email address
- `phone`: Contact number
- `date_of_birth`: Birth date
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Bookings Table
- `id`: Primary key
- `event_id`: Foreign key to Event
- `attendee_id`: Foreign key to Attendee
- `status`: Booking status (pending/confirmed/cancelled)
- `booking_date`: Timestamp
- `updated_at`: Timestamp

## 🚀 Deployment

### Production Considerations

When deploying to production:

1. Set `DEBUG=False` in your environment
2. Use a proper database (PostgreSQL recommended)
3. Set up proper ALLOWED_HOSTS
4. Use environment variables for sensitive data
5. Set up SSL/TLS certificates
6. Use a reverse proxy (Nginx)
7. Set up proper logging
8. Configure CORS if needed

### Example Production Docker Compose

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./static:/static
      - ./media:/media
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
```

## 🔮 Future Enhancements

- Email notifications for bookings
- Payment gateway integration
- Waitlist management
- Event categories and tags
- Advanced reporting and analytics
- Mobile app API endpoints
- WebSocket support for real-time updates
- Redis caching for improved performance
- Celery for background tasks

---

**Note**: This is a development setup with SQLite. For production deployment, consider using PostgreSQL and implementing proper security measures.