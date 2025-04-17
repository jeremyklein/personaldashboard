# Personal Dashboard

A simple Django-based personal dashboard application with user authentication and Tailwind CSS styling.

## Features

- User authentication (login, logout, register)
- Protected dashboard page (only accessible to logged-in users)
- Modern UI with Tailwind CSS
- Docker support for easy deployment

## Local Setup Instructions

### Option 1: Using Docker (Recommended)

1. Clone the repository
2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
3. Build and start the containers:
   ```bash
   docker-compose up -d --build
   ```
4. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```
5. Access the application at http://localhost:8000/

### Option 2: Manual Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Install Tailwind CSS:
   ```bash
   cd theme && npm install
   ```
6. Build Tailwind CSS:
   ```bash
   cd theme && npm run build
   ```
7. Run migrations:
   ```bash
   python manage.py migrate
   ```
8. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```
9. Run the development server:
   ```bash
   python manage.py runserver
   ```
10. Access the application at http://127.0.0.1:8000/

## Production Deployment

1. Create a `.env` file with production settings:
   ```bash
   cp .env.example .env
   # Edit .env to set production values
   ```
2. Build and start the production containers:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```
3. Access the application at http://your-server-ip/

## Login Details

- Admin User:
  - Username: admin
  - Password: adminpassword (change this in production!)

## Running Tailwind in Development Mode

For development with hot-reloading of Tailwind styles:

### With Docker:
```bash
docker-compose up tailwind
```

### Without Docker:
```bash
cd theme && npm run watch
```

## Project Structure

- `core/` - Main application with views and templates for authentication and dashboard
- `theme/` - Tailwind CSS configuration and static files
- `dashboard/` - Project settings and main URL configuration
- `nginx/` - Nginx configuration for production
- `Dockerfile` - Docker configuration for the application
- `docker-compose.yml` - Docker Compose configuration for development
- `docker-compose.prod.yml` - Docker Compose configuration for production

## Future Enhancements

- Add more dashboard widgets
- User profile customization
- Data visualization features
- Calendar integration