# ALX Travel App - Backend (0x00)

A comprehensive Django REST API for a travel booking platform that allows users to search, book, and review accommodations worldwide.

## 🚀 Features

- **Accommodation Listings**: Browse and manage property listings
- **Booking System**: Complete booking workflow with validations
- **Review System**: User reviews and ratings for properties
- **REST API**: Full API with Swagger documentation
- **Background Tasks**: Celery integration for async processing
- **Admin Interface**: Django admin for content management

## 🛠️ Technologies Used

- **Backend**: Django 4.2+, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production ready)
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Task Queue**: Celery with Redis
- **Cross-Origin**: django-cors-headers
- **Media Processing**: Pillow for image handling

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)
- Redis (for Celery tasks)
- Git

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/alx_travel_app_0x00.git
cd alx_travel_app_0x00/alx_travel_app
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Seed Database (Optional)
```bash
python manage.py seed
# Or with custom counts
python manage.py seed --listings 20 --bookings 50 --reviews 30
```

### 7. Run Development Server
```bash
python manage.py runserver
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🏗️ Project Structure

```
alx_travel_app_0x00/
├── alx_travel_app               
├── alx_travel_app/
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py            # Celery configuration
├── listings/
│   ├── __init__.py
│   ├── models.py            # Database models (Listing, Booking, Review)
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API views
│   ├── urls.py              # Listings URL patterns
│   ├── admin.py             # Django admin configuration
│   ├── management/
│   │   └── commands/
│   │       └── seed.py      # Database seeding command
│   └── migrations/
├── media/                   # User uploaded files
├── static/                  # Static files
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
├── .gitignore
└── README.md
```

## 🗄️ Database Models

### Listing
- Property details (title, description, location)
- Pricing and capacity information
- Host relationship
- Availability status

### Booking
- Booking details (dates, guests, pricing)
- User and listing relationships
- Status tracking (pending, confirmed, cancelled, completed)

### Review
- User reviews and ratings (1-5 stars)
- Review content and timestamps
- Linked to specific listings

## 🔧 Management Commands

### Database Seeding
```bash
# Seed with default data
python manage.py seed

# Custom data amounts
python manage.py seed --listings 15 --bookings 30 --reviews 25
```

## 🚀 Deployment

### Environment Variables
Set these in production:
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
CELERY_BROKER_URL=redis://redis-server:6379/0
```

### Static Files
```bash
python manage.py collectstatic
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test listings
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 API Endpoints

- `GET /api/v1/listings/` - List all listings
- `POST /api/v1/listings/` - Create a new listing
- `GET /api/v1/listings/{id}/` - Get specific listing
- `PUT /api/v1/listings/{id}/` - Update listing
- `DELETE /api/v1/listings/{id}/` - Delete listing
- `GET /api/v1/bookings/` - List bookings
- `POST /api/v1/bookings/` - Create booking
- `GET /api/v1/reviews/` - List reviews
- `POST /api/v1/reviews/` - Create review

## 🐛 Troubleshooting

### Common Issues

1. **Redis Connection Error**
   - Make sure Redis is running: `redis-server`
   - Check CELERY_BROKER_URL in settings

2. **Migration Issues**
   - Delete migration files and remake: `python manage.py makemigrations`
   - Reset database: `python manage.py flush`

3. **Static Files Not Loading**
   - Run: `python manage.py collectstatic`
   - Check STATIC_URL and STATIC_ROOT settings

## 📄 License

This project is part of the ALX Software Engineering program.

## 👥 Authors

- Your Name - [@your-github-username](https://github.com/your-github-username)

## 🙏 Acknowledgments

- ALX Software Engineering Program
- Django and DRF communities
- Contributors and reviewers