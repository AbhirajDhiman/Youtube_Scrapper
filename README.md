# YouTube Channel Discovery Tool

A powerful Flask-based web application for discovering YouTube channels using keyword searches with advanced filtering capabilities. Built for content creators, marketers, and researchers who need to find and analyze YouTube channels efficiently.

## 🌟 Features

- **Keyword-based Channel Search**: Find YouTube channels using any search term
- **Advanced Filtering**: Filter by subscriber count, video count, and channel activity
- **Real-time API Quota Monitoring**: Track YouTube API usage with visual indicators
- **Multiple Export Formats**: Download results as CSV, Excel, or JSON
- **Responsive Design**: Clean, modern interface that works on all devices
- **Search History**: Track your previous searches (with optional MongoDB integration)
- **Channel Analytics**: View detailed metrics including subscriber counts, video counts, and engagement data

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- YouTube Data API v3 key from [Google Cloud Console](https://console.cloud.google.com/)
- (Optional) MongoDB for search history and analytics

### Setup on Replit

1. **Fork this Repl** or import the repository
2. **Set up environment variables** in Replit Secrets:
   - `GOOGLE_API_KEY`: Your YouTube Data API v3 key (required)
   - `SESSION_SECRET`: Flask session secret (optional, defaults to dev key)
   - `MONGODB_URI`: MongoDB connection string (optional)
   - `MONGODB_DATABASE`: MongoDB database name (optional)

3. **Click the Run button** - dependencies will install automatically

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd youtube-channel-discovery
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements_for_vscode.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_youtube_api_key_here
   SESSION_SECRET=your_secret_key_here
   MONGODB_URI=mongodb://localhost:27017/
   MONGODB_DATABASE=youtube_discovery
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Open your browser** to `http://0.0.0.0:5000`

## 🔑 Getting a YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "YouTube Data API v3"
4. Create credentials (API Key)
5. Restrict the key to YouTube Data API v3 for security
6. Copy the key to your environment variables

## 📖 Usage

### Basic Search
1. Enter a keyword in the search box
2. Optionally set filters for subscribers, video count, etc.
3. Click "Search Channels"
4. View results in an organized table

### Advanced Filtering
- **Subscriber Count**: Set minimum/maximum subscriber ranges
- **Video Count**: Filter by number of videos published
- **Upload Frequency**: Filter by channel activity level
- **Days Since Upload**: Find recently active channels

### Exporting Data
- Click any export button (CSV, Excel, JSON) on the results page
- Data includes channel URLs, subscriber counts, contact information, and metrics
- Files are timestamped for easy organization

### API Quota Management
- Monitor your daily quota usage in the top-right corner
- The app tracks API calls and warns when approaching limits
- Daily quota resets at midnight UTC

## 🏗️ Architecture

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
└── requirements_for_vscode.txt  # Python dependencies
```

## 🔧 API Quota Information

The YouTube Data API v3 has the following quota costs:
- **Search**: 100 units per request
- **Channel details**: 1 unit per request
- **Video statistics**: 1 unit per request

Default daily quota: 10,000 units (can be increased via Google Cloud Console)

## 🐛 Troubleshooting

### Common Issues

**"API key not configured"**
- Ensure `GOOGLE_API_KEY` is set in environment variables
- Verify the API key is valid in Google Cloud Console

**"Cannot perform a search"**
- Check API key permissions
- Verify YouTube Data API v3 is enabled
- Check quota limits

**No search results**
- Try broader keywords
- Remove restrictive filters
- Check API quota status

**MongoDB connection errors**
- MongoDB is optional - app works without it
- Verify MongoDB is running if you want to use it
- Check connection string in environment variables

## 🚀 Deployment

### Replit Deployment (Recommended)

This app is optimized for Replit:
1. Import the repository to Replit
2. Set environment variables in Replit Secrets
3. Click "Run" to start the application
4. Use the Deployments tab for production hosting

### Production Considerations

- Set `SESSION_SECRET` to a secure random string
- Enable MongoDB for persistent search history
- Consider rate limiting for public deployments
- Monitor API quota usage regularly

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, DataTables, Font Awesome
- **Database**: MongoDB (optional)
- **APIs**: YouTube Data API v3
- **Deployment**: Replit-optimized

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Abhiraj Dhiman**  
Email: abhirajdhiman@outlook.com

---

For questions, issues, or feature requests, please open an issue on the repository or contact the author directly.