
# 🎯 YouTube Channel Discovery Tool

A powerful Flask web application that enables comprehensive YouTube channel research with advanced filtering, contact enrichment, and data export capabilities. Built for content creators, marketers, and researchers who need detailed channel analytics and contact information.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v3.0.0-green.svg)
![MongoDB](https://img.shields.io/badge/mongodb-supported-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Key Features

### 🔍 **Advanced Channel Search**
- **Smart Keyword Search**: Discover channels using YouTube Data API v3
- **Advanced Filtering**: Filter by subscriber count, video count, upload frequency
- **Activity Monitoring**: Filter channels by recent upload activity
- **Quality Metrics**: Calculate engagement rates, average views, and channel performance
- **Quick Filter Presets**: One-click filters for high-quality, micro-influencer, and active channels

### 📧 **Contact Enrichment**
- **Email Extraction**: Automatically extract contact emails from channel descriptions
- **Website Analysis**: Discover and analyze linked websites for contact information
- **Social Media Discovery**: Find associated social media profiles
- **WHOIS Integration**: Extract domain registration emails
- **Contact Page Detection**: Identify website contact pages and forms

### 📊 **Comprehensive Analytics**
- **Channel Quality Metrics**: Upload frequency, engagement rates, audience retention
- **Performance Analysis**: Average views per video, subscriber growth patterns
- **Activity Tracking**: Days since last upload, posting consistency
- **Historical Data**: Track channel evolution and performance trends

### 📁 **Multi-Format Export**
- **CSV Export**: Detailed spreadsheet with all channel data and contact information
- **Excel Export**: Formatted XLSX files with styling and optimized column widths
- **JSON Export**: Machine-readable format with complete metadata
- **Custom Fields**: Export includes quality metrics, contact data, and analytics

### 🗄️ **Database Integration**
- **MongoDB Support**: Persistent storage with automatic indexing
- **Search History**: Track and analyze your research patterns
- **Channel Caching**: Improve performance with intelligent data caching
- **Analytics Dashboard**: Visualize popular keywords and search trends
- **Graceful Fallback**: Works with or without database connection

### 🎨 **Professional Interface**
- **Responsive Design**: Bootstrap 5 with dark theme optimization
- **Interactive Tables**: DataTables integration for sorting and filtering
- **Real-time Feedback**: Live quota monitoring and search progress
- **Intuitive Navigation**: Clean, professional interface designed for productivity

## 🚀 Quick Setup

### Prerequisites
- Python 3.11+
- YouTube Data API v3 key
- MongoDB (optional, for persistence)

### 1. Install Dependencies

```bash
pip install flask google-api-python-client pymongo python-dotenv gunicorn werkzeug openpyxl
```

### 2. Environment Configuration

Create a `.env` file:

```env
# Required
GOOGLE_API_KEY=your_youtube_api_key_here
SESSION_SECRET=your_secure_session_key_here

# Optional - Database Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=youtube_discovery

# Optional - Advanced Settings
MAX_RESULTS_PER_SEARCH=200
CACHE_DURATION=3600
```

### 3. Get YouTube API Key

1. Visit [Google Cloud Console](https://console.cloud.google.com)
2. Create or select a project
3. Enable **YouTube Data API v3**
4. Generate an API key under **Credentials**
5. Add the key to your `.env` file

### 4. Launch Application

**Development Mode:**
```bash
python main.py
```

**Production Mode:**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

Access your application at `http://localhost:5000`

## 📋 Usage Guide

### Basic Channel Search
1. Enter keywords (e.g., "tech reviews", "cooking tutorials")
2. Set search parameters (max results, filters)
3. Click **Search Channels** to discover channels
4. Review results with quality metrics and contact information

### Advanced Filtering
- **Subscriber Range**: Target channels within specific subscriber counts
- **Video Count**: Filter by content volume
- **Upload Frequency**: Find consistently active channels
- **Recent Activity**: Discover channels with recent uploads

### Quick Filter Presets
- **High Quality**: Channels with good engagement and regular uploads
- **Micro Influencers**: Smaller channels with engaged audiences
- **Active Channels**: Recently active content creators

### Data Export Options
- **CSV**: Complete dataset for spreadsheet analysis
- **Excel**: Formatted reports with professional styling
- **JSON**: Structured data for API integration

### Analytics Dashboard
- View search history and popular keywords
- Analyze channel discovery patterns
- Track database usage statistics
- Monitor API quota consumption

## 🏗️ Project Structure

```
├── main.py                 # Application entry point and server configuration
├── app.py                  # Flask routes, request handling, and export logic
├── youtube_service.py      # YouTube API integration and data processing
├── database.py             # MongoDB operations and analytics
├── templates/              # Jinja2 HTML templates
│   ├── base.html          # Base template with navigation and styling
│   ├── index.html         # Search interface with advanced filters
│   ├── results.html       # Channel results display and export options
│   ├── history.html       # Search history and pattern analysis
│   └── stats.html         # Database analytics and insights
├── static/                 # Frontend assets
│   ├── css/custom.css     # Custom styling and theme overrides
│   └── js/app.js          # Client-side JavaScript and interactions
├── .env                   # Environment variables (create this file)
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 🔧 Technical Stack

### Backend
- **Flask 3.0.0**: Modern Python web framework
- **YouTube Data API v3**: Official Google API for channel data
- **PyMongo 4.6.0**: MongoDB driver for data persistence
- **Gunicorn**: Production WSGI server
- **OpenPyXL**: Excel file generation with formatting

### Frontend
- **Bootstrap 5**: Responsive CSS framework with dark theme
- **DataTables**: Advanced table functionality and search
- **Font Awesome**: Professional icon library
- **jQuery**: JavaScript utilities and AJAX handling

### Database
- **MongoDB**: NoSQL database for flexible data storage
- **Automatic Indexing**: Optimized queries for performance
- **Analytics Collections**: Dedicated collections for insights

## 🌐 Deployment

### Replit Deployment (Recommended)
The application is optimized for Replit with:
- Automatic dependency installation via Nix
- Environment variable management
- Built-in port forwarding
- One-click deployment

### Production Considerations
- Use environment variables for all sensitive data
- Configure MongoDB with authentication
- Set up proper logging and monitoring
- Implement rate limiting for API protection

## 📊 API Quota Management

The application includes intelligent quota management:
- **Real-time Monitoring**: Track API usage in the interface
- **Efficient Caching**: Reduce redundant API calls
- **Batch Processing**: Optimize multiple channel requests
- **Error Handling**: Graceful fallback when limits are reached

## 🔒 Security Features

- **Environment Variables**: Secure storage of API keys and secrets
- **Session Management**: Encrypted user sessions
- **Input Validation**: Protection against malicious input
- **Error Handling**: Secure error messages without data exposure

## 🤝 Contributing

We welcome contributions to improve the YouTube Channel Discovery Tool:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Changelog

### Version 2.0.0 (Current)
- ✅ **Enhanced Contact Enrichment**: Email extraction, website analysis, WHOIS integration
- ✅ **Advanced Quality Metrics**: Upload frequency, engagement rates, performance analytics
- ✅ **Multi-Format Export**: CSV, Excel, and JSON export with complete metadata
- ✅ **MongoDB Integration**: Persistent storage, caching, and analytics dashboard
- ✅ **Advanced Filtering**: Comprehensive filters for subscriber count, activity, and quality
- ✅ **Professional UI**: Bootstrap 5 dark theme with responsive design
- ✅ **Quick Filter Presets**: One-click filters for common use cases
- ✅ **Real-time Analytics**: Live quota monitoring and search insights

### Version 1.0.0
- ✅ **Basic YouTube Search**: Keyword-based channel discovery
- ✅ **Simple Export**: CSV export functionality
- ✅ **Session Storage**: Basic search history tracking
- ✅ **Flask Framework**: Core web application structure

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For support, feature requests, or bug reports:
- Create an issue on the repository
- Check the documentation for common solutions
- Review the changelog for recent updates

---

**Built with ❤️ for content creators, marketers, and researchers**

*Discover, analyze, and connect with YouTube channels like never before.*
