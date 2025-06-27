# YouTube Channel Discovery Tool

A Flask web application that allows users to search for YouTube channels by keyword and export results to CSV. Features search history, database integration, and analytics.

## Features

- 🔍 **Channel Search**: Search YouTube channels by keyword using YouTube Data API v3
- 📊 **Data Export**: Export search results to CSV format
- 📈 **Analytics**: Track search history and popular keywords
- 🗄️ **Database**: MongoDB integration for persistent storage (optional)
- 🎨 **Responsive UI**: Bootstrap dark theme optimized for development

## Quick Setup

### 1. Install Dependencies

```bash
pip install flask google-api-python-client pymongo python-dotenv gunicorn werkzeug
```

### 2. Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_youtube_api_key_here
SESSION_SECRET=your_secret_key_here
MONGODB_URI=mongodb://localhost:27017  # Optional
MONGODB_DATABASE=youtube_discovery      # Optional
```

### 3. Get YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Copy the API key to your `.env` file

### 4. Run the Application

```bash
python main.py
```

Or with Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

Visit `http://localhost:5000` to access the application.

## Project Structure

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
├── static/              # Static assets
│   ├── css/custom.css   # Custom styling
│   └── js/app.js        # Client-side JavaScript
├── .env                 # Environment variables (create this)
└── requirements.txt     # Python dependencies
```

## Usage

1. **Search Channels**: Enter keywords like "gaming", "cooking", "tech reviews"
2. **View Results**: Browse channels with subscriber count, video count, and descriptions
3. **Export Data**: Download results as CSV for analysis
4. **Track History**: View your search history and popular keywords
5. **Analytics**: Check database statistics (if MongoDB is configured)

## Database Integration

The app works with or without MongoDB:

- **With MongoDB**: Persistent storage, caching, and analytics
- **Without MongoDB**: Session-based storage (data lost on restart)

## Development

The application uses:
- **Flask**: Web framework
- **YouTube Data API v3**: Channel data source
- **MongoDB**: Optional database for persistence
- **Bootstrap 5**: Frontend styling
- **DataTables**: Enhanced table functionality

## Deployment

Ready for deployment on platforms like:
- Replit
- Heroku
- Railway
- DigitalOcean App Platform

## License

Open source - feel free to modify and use for your projects.