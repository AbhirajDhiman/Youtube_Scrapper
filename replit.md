# YouTube Channel Discovery Tool

## Overview

This is a Flask-based web application that allows users to search for YouTube channels using keywords and export the results. The application integrates with the YouTube Data API v3 to fetch channel information and provides a clean, responsive interface for discovery and data export.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: MongoDB for persistent data storage and analytics
- **API Integration**: YouTube Data API v3 via Google API Python Client
- **Session Management**: Flask sessions with MongoDB fallback for search history
- **Deployment**: Gunicorn WSGI server with autoscale deployment target

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5 with dark theme
- **JavaScript**: Vanilla JS with Bootstrap components
- **Icons**: Font Awesome
- **Data Tables**: DataTables plugin for enhanced table functionality

### Application Structure
```
├── main.py              # Application entry point
├── app.py               # Main Flask application and routes
├── youtube_service.py   # YouTube API service layer
├── database.py          # MongoDB database service layer
├── templates/           # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Search form page
│   ├── results.html     # Search results display
│   ├── history.html     # Search history page
│   └── stats.html       # Database statistics page
└── static/              # Static assets
    ├── css/custom.css   # Custom styling
    └── js/app.js        # Client-side JavaScript
```

## Key Components

### YouTube Service (`youtube_service.py`)
- Handles all YouTube Data API interactions
- Manages API key authentication
- Provides channel search functionality
- Error handling for API failures

### Database Service (`database.py`)
- MongoDB connection and operations management
- Persistent storage of search history and channel data
- Database indexing for performance optimization
- Analytics and statistics generation
- Graceful fallback when database unavailable

### Flask Application (`app.py`)
- Route handlers for search, results, history, stats, and export
- Hybrid session/database management for search history
- CSV export functionality with database integration
- Flash messaging for user feedback
- Database statistics and analytics routes

### Frontend Components
- Responsive search interface with Bootstrap styling
- DataTables integration for sortable, searchable results
- Database statistics dashboard with analytics
- Dark theme optimized for Replit environment
- Client-side form validation and UX enhancements

## Data Flow

1. **Search Request**: User enters keyword on index page
2. **API Call**: YouTube service searches for channels using keyword
3. **Results Processing**: Channel data is formatted and stored in session
4. **Display**: Results are presented in a sortable table format
5. **Export**: Users can download results as CSV files
6. **History**: Search history is maintained in Flask sessions

## External Dependencies

### Required Environment Variables
- `GOOGLE_API_KEY`: YouTube Data API v3 key (required for functionality)
- `SESSION_SECRET`: Flask session encryption key (defaults to dev key)
- `MONGODB_URI`: MongoDB connection string (optional - defaults to localhost)
- `MONGODB_DATABASE`: MongoDB database name (optional - defaults to youtube_discovery)

### Third-Party Services
- **YouTube Data API v3**: Primary data source for channel information
- **Google API Python Client**: Official Google API library
- **Bootstrap CDN**: Frontend styling framework
- **Font Awesome CDN**: Icon library
- **DataTables CDN**: Table enhancement library

### Python Dependencies
- Flask: Web framework
- Google API Python Client: YouTube API integration
- PyMongo: MongoDB driver and operations
- Python-dotenv: Environment variable management
- Gunicorn: Production WSGI server
- Werkzeug: WSGI utilities and middleware

## Deployment Strategy

- **Environment**: Replit with Nix package management
- **Runtime**: Python 3.11
- **Server**: Gunicorn with autoscale deployment
- **Port**: 5000 (configured for Replit environment)
- **Process Management**: Replit workflows for development and production

The application is configured for immediate deployment on Replit with proper WSGI server configuration and environment variable support.

## Changelog

```
Changelog:
- June 27, 2025. Initial setup with Flask app and YouTube API integration
- June 27, 2025. Added MongoDB database integration with:
  * Persistent search history storage
  * Channel data caching for improved performance
  * Database statistics and analytics dashboard
  * Graceful fallback to session-based storage when database unavailable
  * New /stats route for database analytics
  * Enhanced navigation with database features
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```