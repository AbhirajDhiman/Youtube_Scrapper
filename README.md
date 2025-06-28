
# YouTube Channel Discovery Tool

A powerful web application for discovering YouTube channels using the YouTube Data API v3. This tool allows users to search for channels with advanced filtering options, view detailed analytics, and export results in multiple formats.

## 🌟 Features

- **Advanced Search**: Find YouTube channels by keywords with comprehensive filtering
- **Real-time API Monitoring**: Track YouTube API quota usage and status
- **Smart Filtering**: Filter by subscriber count, video count, upload frequency, and more
- **Contact Discovery**: Extract email addresses and social media links from channel descriptions and websites
- **Export Options**: Export results to CSV, Excel, or JSON formats
- **Modern UI**: Responsive design with smooth animations and interactive elements
- **Performance Optimized**: Async operations and efficient API usage

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- YouTube Data API v3 key from Google Cloud Console

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements_for_vscode.txt
   ```

3. **Configure environment variables:**
   
   Create a `.env` file in the root directory:
   ```env
   # Required: YouTube Data API v3 Key
   GOOGLE_API_KEY=your_youtube_api_key_here
   
   # Flask Configuration
   SESSION_SECRET=your_secure_random_string_here
   PORT=5000
   
   # Optional: MongoDB (leave blank for session storage)
   # MONGODB_URI=mongodb://localhost:27017
   # MONGODB_DATABASE=youtube_discovery
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

5. **Access the app:**
   Open your browser and go to `http://localhost:5000`

## 🔧 Configuration

### Getting a YouTube API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create credentials (API key)
5. Copy the API key to your `.env` file

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `GOOGLE_API_KEY` | ✅ | YouTube Data API v3 key | None |
| `SESSION_SECRET` | ✅ | Flask session secret key | Random |
| `PORT` | ❌ | Application port | 5000 |
| `MONGODB_URI` | ❌ | MongoDB connection string | None |
| `MONGODB_DATABASE` | ❌ | MongoDB database name | youtube_discovery |
| `MAX_DAILY_QUOTA` | ❌ | Daily API quota limit | 10000 |

## 📖 Usage

### Basic Search

1. Enter keywords in the search box
2. Optionally set filters (subscriber count, video count, etc.)
3. Click "Search Channels" or press Ctrl+Enter
4. View results in an organized table

### Advanced Filtering

- **Subscriber Range**: Set minimum and maximum subscriber counts
- **Video Count**: Filter by total number of videos
- **Upload Frequency**: Filter by videos uploaded per week
- **Days Since Upload**: Filter by recency of last upload

### Exporting Results

- **CSV**: Spreadsheet-compatible format
- **Excel**: Rich formatting with proper columns
- **JSON**: Structured data for developers

## 🔍 API Features

### Contact Discovery

The tool automatically extracts:
- Email addresses from channel descriptions
- Social media profiles (Twitter, LinkedIn, Instagram)
- Website URLs and contact pages
- WHOIS information for domains

### Quality Metrics

For each channel, the tool calculates:
- Upload frequency (videos per week)
- Average views per video
- Engagement rate (likes + comments / views)
- Days since last upload
- Channel age

## 🛠️ Development

### Project Structure

```
youtube-discovery/
├── app.py              # Main Flask application
├── main.py             # Application entry point
├── youtube_service.py  # YouTube API service layer
├── database.py         # Database operations (MongoDB)
├── static/             # CSS, JavaScript, images
├── templates/          # HTML templates
├── .env               # Environment configuration
└── requirements_for_vscode.txt  # Python dependencies
```

### Adding New Features

1. **Backend**: Add new routes in `app.py`
2. **API Logic**: Extend `youtube_service.py` for new API operations
3. **Database**: Update `database.py` for data persistence
4. **Frontend**: Add templates in `templates/` and JavaScript in `static/js/`

## 📊 API Quota Management

The tool includes built-in quota management:

- **Real-time Monitoring**: Dashboard shows current usage
- **Smart Limiting**: Prevents quota exhaustion
- **Cost Optimization**: Efficient API calls to minimize quota usage

### Quota Costs

- Channel search: 100 units per request
- Channel details: 1 unit per request
- Video statistics: 1 unit per request

## 🔧 Troubleshooting

### Common Issues

**"API key not configured"**
- Ensure `GOOGLE_API_KEY` is set in `.env`
- Verify the API key is valid in Google Cloud Console

**"Cannot perform a search" / "channelId error"**
- Check API key permissions
- Verify YouTube Data API v3 is enabled
- Check quota limits

**"Connection refused" on localhost**
- Ensure Flask app is running
- Check if port 5000 is available
- Try accessing via `0.0.0.0:5000` instead

**Search returns no results**
- Try broader keywords
- Remove restrictive filters
- Check API quota status

**MongoDB connection errors**
- MongoDB is optional - app works without it
- Verify MongoDB is running if you want to use it
- Check connection string in `.env`

### Performance Issues

**Slow searches**
- Reduce `max_results` parameter
- Disable contact enrichment for faster results
- Check internet connection speed

**Memory usage**
- Large exports may use significant memory
- Process results in smaller batches
- Clear browser cache if UI becomes slow

## 🚀 Deployment

### Replit Deployment

This app is optimized for Replit:

1. Import the repository to Replit
2. Set environment variables in Replit Secrets
3. Click "Run" to start the application
4. Use the Deployments tab for production hosting

### Local Production

For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server like Gunicorn
3. Configure reverse proxy (nginx) if needed
4. Set up proper logging and monitoring

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section above
- Review GitHub issues
- Ensure your API key and environment are properly configured

---

**Note**: This tool is for educational and research purposes. Please respect YouTube's terms of service and API usage policies.
