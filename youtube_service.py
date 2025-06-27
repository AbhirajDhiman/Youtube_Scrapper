import os
import logging
import re
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class YouTubeService:
    """Service class for YouTube Data API interactions"""
    
    def __init__(self):
        self.api_key = os.environ.get('GOOGLE_API_KEY')
        if not self.api_key:
            logging.warning("Google API key not found in environment variables. Please set GOOGLE_API_KEY.")
        self.youtube = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize YouTube API service"""
        if self.api_key:
            try:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
                logging.info("YouTube API service initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize YouTube API service: {str(e)}")
                self.youtube = None
    
    def search_channels(self, keyword, max_results=50):
        """
        Search for YouTube channels by keyword with enhanced data extraction
        
        Args:
            keyword (str): Search keyword
            max_results (int): Maximum number of results to return (increased capacity)
            
        Returns:
            list: List of channel data dictionaries with email extraction
        """
        if not self.youtube:
            raise Exception("YouTube API service not available. Please check your API key.")
        
        channels = []
        
        try:
            # Search for channels
            search_response = self.youtube.search().list(
                q=keyword,
                part='snippet',
                type='channel',
                maxResults=max_results,
                order='relevance'
            ).execute()
            
            channel_ids = []
            for search_result in search_response.get('items', []):
                channel_ids.append(search_result['snippet']['channelId'])
            
            if not channel_ids:
                return channels
            
            # Get detailed channel statistics
            channels_response = self.youtube.channels().list(
                part='snippet,statistics',
                id=','.join(channel_ids)
            ).execute()
            
            for channel in channels_response.get('items', []):
                snippet = channel['snippet']
                statistics = channel.get('statistics', {})
                
                # Extract email from channel description
                description = snippet.get('description', 'No description available')
                email = self._extract_email_from_description(description)
                
                # Try to get more detailed about section if no email found in snippet
                if not email:
                    about_section = self._get_channel_about_section(channel['id'])
                    email = self._extract_email_from_description(about_section)
                
                channel_data = {
                    'title': snippet.get('title', 'N/A'),
                    'channel_id': channel['id'],
                    'description': description,
                    'published_at': snippet.get('publishedAt', 'N/A'),
                    'subscriber_count': self._format_count(statistics.get('subscriberCount', '0')),
                    'video_count': self._format_count(statistics.get('videoCount', '0')),
                    'view_count': self._format_count(statistics.get('viewCount', '0')),
                    'thumbnail_url': snippet.get('thumbnails', {}).get('default', {}).get('url', ''),
                    'custom_url': snippet.get('customUrl', ''),
                    'country': snippet.get('country', 'N/A'),
                    'email': email  # New field for extracted email
                }
                
                channels.append(channel_data)
            
            # Sort by subscriber count (descending)
            channels.sort(key=lambda x: int(x['subscriber_count'].replace(',', '') or '0'), reverse=True)
            
            logging.info(f"Found {len(channels)} channels for keyword: {keyword}")
            return channels
            
        except HttpError as e:
            error_message = f"YouTube API error: {e.resp.status} - {e.content.decode()}"
            logging.error(error_message)
            
            if e.resp.status == 403:
                raise Exception("YouTube API quota exceeded or invalid API key. Please check your API key and quota.")
            elif e.resp.status == 400:
                raise Exception("Invalid search parameters. Please try a different keyword.")
            else:
                raise Exception(f"YouTube API error: {e.resp.status}")
                
        except Exception as e:
            logging.error(f"Unexpected error in search_channels: {str(e)}")
            raise Exception(f"Failed to search channels: {str(e)}")
    
    def _extract_email_from_description(self, description):
        """Extract email addresses from channel description"""
        if not description:
            return None
            
        # Enhanced email regex patterns
        email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'\b[A-Za-z0-9._%+-]+\s*\[\s*at\s*\]\s*[A-Za-z0-9.-]+\s*\[\s*dot\s*\]\s*[A-Z|a-z]{2,}\b',
            r'contact\s*:\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'email\s*:\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'business\s*:\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
        ]
        
        for pattern in email_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            if matches:
                # Return first valid email found
                email = matches[0] if isinstance(matches[0], str) else matches[0]
                # Clean up common obfuscations
                email = email.replace('[at]', '@').replace('[dot]', '.').replace(' ', '')
                return email.lower()
        
        return None

    def _get_channel_about_section(self, channel_id):
        """Get detailed channel about section for email extraction"""
        if not self.youtube:
            return ''
            
        try:
            # Get channel details with brandingSettings part
            response = self.youtube.channels().list(
                part='brandingSettings',
                id=channel_id
            ).execute()
            
            if response.get('items'):
                branding = response['items'][0].get('brandingSettings', {})
                channel_info = branding.get('channel', {})
                return channel_info.get('description', '')
        except Exception as e:
            logging.debug(f"Could not fetch about section for channel {channel_id}: {str(e)}")
        
        return ''
    
    def _format_count(self, count_str):
        """Format count numbers with commas"""
        try:
            count = int(count_str or '0')
            return f"{count:,}"
        except (ValueError, TypeError):
            return "N/A"
