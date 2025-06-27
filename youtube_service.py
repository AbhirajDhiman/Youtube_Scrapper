
import os
import logging
import re
import requests
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class YouTubeService:
    """Service class for YouTube Data API interactions with enhanced search capabilities"""
    
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
                # Test the API key with a simple call
                self._validate_api_key()
            except Exception as e:
                logging.error(f"Failed to initialize YouTube API service: {str(e)}")
                self.youtube = None
    
    def _validate_api_key(self):
        """Validate API key with a simple test call"""
        try:
            test_response = self.youtube.search().list(
                q="test",
                part='snippet',
                type='channel',
                maxResults=1
            ).execute()
            logging.info("API key validation successful")
            return True
        except HttpError as e:
            logging.error(f"API key validation failed: {e.resp.status} - {e.content.decode()}")
            return False
        except Exception as e:
            logging.error(f"API key validation error: {str(e)}")
            return False
    
    def search_channels(self, keyword, max_results=50):
        """
        Enhanced search for YouTube channels with multiple strategies and pagination
        
        Args:
            keyword (str): Search keyword
            max_results (int): Target number of results (will try to get close to this)
            
        Returns:
            list: List of channel data dictionaries with comprehensive email extraction
        """
        if not self.api_key:
            logging.error("Google API key not found in environment variables")
            raise Exception("Google API key not found. Please set GOOGLE_API_KEY environment variable.")
        
        if not self.youtube:
            logging.error("YouTube API service not initialized")
            raise Exception("YouTube API service not available. Please check your API key.")
        
        logging.info(f"Starting search for keyword: '{keyword}' with max_results: {max_results}")
        
        all_channels = []
        unique_channel_ids = set()
        
        # Multiple search strategies to get more diverse results
        search_strategies = [
            {'order': 'relevance', 'type': 'channel'},
            {'order': 'viewCount', 'type': 'channel'},
            {'order': 'date', 'type': 'channel'},
            {'order': 'rating', 'type': 'channel'}
        ]
        
        # Also search for videos and extract channel info from top video creators
        video_strategies = [
            {'order': 'relevance', 'type': 'video'},
            {'order': 'viewCount', 'type': 'video'},
            {'order': 'date', 'type': 'video'}
        ]
        
        try:
            # Phase 1: Direct channel searches with different ordering
            for i, strategy in enumerate(search_strategies):
                if len(all_channels) >= max_results:
                    break
                
                logging.info(f"Trying search strategy {i+1}/{len(search_strategies)}: {strategy}")
                channels = self._search_with_strategy(keyword, strategy, max_results=50)
                logging.info(f"Strategy {i+1} returned {len(channels)} channels")
                
                for channel in channels:
                    if channel['channel_id'] not in unique_channel_ids:
                        all_channels.append(channel)
                        unique_channel_ids.add(channel['channel_id'])
                
                logging.info(f"Total unique channels so far: {len(all_channels)}")
                
                # Small delay to avoid rate limiting
                time.sleep(0.1)
            
            # Phase 2: Search videos and extract unique channels
            for strategy in video_strategies:
                if len(all_channels) >= max_results:
                    break
                    
                video_channels = self._search_videos_for_channels(keyword, strategy, max_results=50)
                for channel in video_channels:
                    if channel['channel_id'] not in unique_channel_ids:
                        all_channels.append(channel)
                        unique_channel_ids.add(channel['channel_id'])
                
                time.sleep(0.1)
            
            # Phase 3: Related keyword searches
            related_keywords = self._generate_related_keywords(keyword)
            for related_keyword in related_keywords:
                if len(all_channels) >= max_results:
                    break
                    
                channels = self._search_with_strategy(related_keyword, {'order': 'relevance', 'type': 'channel'}, max_results=25)
                for channel in channels:
                    if channel['channel_id'] not in unique_channel_ids:
                        all_channels.append(channel)
                        unique_channel_ids.add(channel['channel_id'])
                
                time.sleep(0.1)
            
            # Enhanced email extraction for all channels
            for i, channel in enumerate(all_channels):
                enhanced_email = self._enhanced_email_extraction(channel['channel_id'], channel.get('description', ''))
                if enhanced_email:
                    all_channels[i]['email'] = enhanced_email
                
                # Add rate limiting for email extraction
                if i % 10 == 0:
                    time.sleep(0.2)
            
            # Sort by subscriber count (descending) as default
            all_channels.sort(key=lambda x: int(x['subscriber_count'].replace(',', '') or '0'), reverse=True)
            
            logging.info(f"Found {len(all_channels)} unique channels for keyword: {keyword}")
            return all_channels[:max_results]  # Return up to max_results
            
        except HttpError as e:
            error_content = e.content.decode() if e.content else "No error details"
            error_message = f"YouTube API error: {e.resp.status} - {error_content}"
            logging.error(error_message)
            
            if e.resp.status == 403:
                if "quotaExceeded" in error_content or "dailyLimitExceeded" in error_content:
                    raise Exception("YouTube API quota exceeded. Please try again tomorrow or check your quota limits.")
                elif "keyInvalid" in error_content:
                    raise Exception("Invalid YouTube API key. Please check your GOOGLE_API_KEY environment variable.")
                else:
                    raise Exception("YouTube API access forbidden. Please check your API key permissions.")
            elif e.resp.status == 400:
                raise Exception(f"Invalid search parameters for keyword '{keyword}'. Error: {error_content}")
            elif e.resp.status == 404:
                raise Exception("YouTube API endpoint not found. Please check your API configuration.")
            else:
                raise Exception(f"YouTube API error {e.resp.status}: {error_content}")
                
        except Exception as e:
            logging.error(f"Unexpected error in search_channels: {str(e)}")
            if "API" not in str(e):
                raise Exception(f"Network or connection error: {str(e)}")
            else:
                raise
    
    def _search_with_strategy(self, keyword, strategy, max_results=50):
        """Search channels with a specific strategy"""
        channels = []
        next_page_token = None
        results_per_page = min(50, max_results)  # API max is 50 per request
        
        try:
            while len(channels) < max_results:
                # Calculate how many more results we need
                remaining_results = min(results_per_page, max_results - len(channels))
                
                logging.debug(f"Making API call with strategy {strategy}, remaining_results: {remaining_results}")
                
                search_response = self.youtube.search().list(
                    q=keyword,
                    part='snippet',
                    type=strategy['type'],
                    maxResults=remaining_results,
                    order=strategy['order'],
                    pageToken=next_page_token
                ).execute()
                
                logging.debug(f"API response: {len(search_response.get('items', []))} items returned")
                
                if strategy['type'] == 'channel':
                    channel_ids = [item['snippet']['channelId'] for item in search_response.get('items', [])]
                else:
                    # For video searches, extract unique channel IDs
                    channel_ids = list(set([item['snippet']['channelId'] for item in search_response.get('items', [])]))
                
                if not channel_ids:
                    break
                
                # Get detailed channel information
                page_channels = self._get_channel_details(channel_ids)
                channels.extend(page_channels)
                
                # Check if there's a next page
                next_page_token = search_response.get('nextPageToken')
                if not next_page_token:
                    break
                    
        except Exception as e:
            logging.warning(f"Error in search strategy {strategy}: {str(e)}")
        
        return channels
    
    def _search_videos_for_channels(self, keyword, strategy, max_results=50):
        """Search videos and extract channel information"""
        channels = []
        channel_ids_seen = set()
        
        try:
            search_response = self.youtube.search().list(
                q=keyword,
                part='snippet',
                type='video',
                maxResults=max_results,
                order=strategy['order']
            ).execute()
            
            # Extract unique channel IDs from video results
            for item in search_response.get('items', []):
                channel_id = item['snippet']['channelId']
                if channel_id not in channel_ids_seen:
                    channel_ids_seen.add(channel_id)
            
            # Get channel details for unique channels
            if channel_ids_seen:
                channels = self._get_channel_details(list(channel_ids_seen))
                
        except Exception as e:
            logging.warning(f"Error in video search strategy: {str(e)}")
        
        return channels
    
    def _get_channel_details(self, channel_ids):
        """Get detailed information for a list of channel IDs"""
        channels = []
        
        # Process in batches of 50 (API limit)
        for i in range(0, len(channel_ids), 50):
            batch_ids = channel_ids[i:i+50]
            
            try:
                channels_response = self.youtube.channels().list(
                    part='snippet,statistics,brandingSettings',
                    id=','.join(batch_ids)
                ).execute()
                
                for channel in channels_response.get('items', []):
                    snippet = channel['snippet']
                    statistics = channel.get('statistics', {})
                    branding = channel.get('brandingSettings', {})
                    
                    # Get comprehensive description from multiple sources
                    description = snippet.get('description', 'No description available')
                    branding_desc = branding.get('channel', {}).get('description', '')
                    
                    # Combine descriptions for better email extraction
                    full_description = f"{description} {branding_desc}".strip()
                    
                    # Basic email extraction (enhanced version will be called later)
                    email = self._extract_email_from_description(full_description)
                    
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
                        'email': email,
                        'full_description': full_description  # Store for enhanced email extraction
                    }
                    
                    channels.append(channel_data)
                    
            except Exception as e:
                logging.warning(f"Error getting channel details for batch: {str(e)}")
                continue
        
        return channels
    
    def _generate_related_keywords(self, keyword):
        """Generate related keywords to expand search scope"""
        keyword_lower = keyword.lower()
        related = []
        
        # Gaming related expansions
        if any(game in keyword_lower for game in ['gaming', 'game', 'fortnite', 'minecraft']):
            related.extend([
                f"{keyword} tutorial",
                f"{keyword} gameplay",
                f"{keyword} review",
                f"{keyword} tips",
                f"{keyword} guide"
            ])
        
        # Educational content expansions
        elif any(term in keyword_lower for term in ['tutorial', 'how to', 'learn']):
            related.extend([
                f"{keyword} beginner",
                f"{keyword} advanced",
                f"{keyword} course",
                f"{keyword} training"
            ])
        
        # General expansions
        else:
            related.extend([
                f"{keyword} channel",
                f"{keyword} creator",
                f"{keyword} youtuber",
                f"best {keyword}"
            ])
        
        return related[:3]  # Limit to avoid too many API calls
    
    def _enhanced_email_extraction(self, channel_id, description):
        """Enhanced email extraction using multiple sources and methods"""
        
        # Try multiple approaches to find email
        emails_found = []
        
        # 1. Enhanced regex patterns on existing description
        email = self._extract_email_from_description(description)
        if email:
            emails_found.append(email)
        
        # 2. Try to get channel's "About" page data
        try:
            about_section = self._get_channel_about_section(channel_id)
            if about_section:
                about_email = self._extract_email_from_description(about_section)
                if about_email and about_email not in emails_found:
                    emails_found.append(about_email)
        except:
            pass
        
        # 3. Check recent video descriptions for contact info
        try:
            recent_videos_email = self._check_recent_videos_for_email(channel_id)
            if recent_videos_email and recent_videos_email not in emails_found:
                emails_found.append(recent_videos_email)
        except:
            pass
        
        # Return the first valid email found
        return emails_found[0] if emails_found else None
    
    def _check_recent_videos_for_email(self, channel_id):
        """Check recent videos for email addresses in descriptions"""
        try:
            # Get recent videos from the channel
            videos_response = self.youtube.search().list(
                part='snippet',
                channelId=channel_id,
                type='video',
                order='date',
                maxResults=5  # Check last 5 videos
            ).execute()
            
            for video in videos_response.get('items', []):
                video_id = video['id']['videoId']
                
                # Get video details with description
                video_details = self.youtube.videos().list(
                    part='snippet',
                    id=video_id
                ).execute()
                
                if video_details.get('items'):
                    video_description = video_details['items'][0]['snippet'].get('description', '')
                    email = self._extract_email_from_description(video_description)
                    if email:
                        return email
                        
        except Exception as e:
            logging.debug(f"Could not check recent videos for channel {channel_id}: {str(e)}")
        
        return None
    
    def _extract_email_from_description(self, description):
        """Extract email addresses from text with enhanced patterns"""
        if not description:
            return None
            
        # Enhanced email regex patterns with more variations
        email_patterns = [
            # Standard email format
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            
            # Email with [at] and [dot] obfuscation
            r'\b[A-Za-z0-9._%+-]+\s*\[\s*at\s*\]\s*[A-Za-z0-9.-]+\s*\[\s*dot\s*\]\s*[A-Z|a-z]{2,}\b',
            
            # Email with (at) and (dot) obfuscation
            r'\b[A-Za-z0-9._%+-]+\s*\(\s*at\s*\)\s*[A-Za-z0-9.-]+\s*\(\s*dot\s*\)\s*[A-Z|a-z]{2,}\b',
            
            # Contact/business email patterns
            r'contact\s*:?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'email\s*:?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'business\s*:?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'inquiries\s*:?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'collaborations?\s*:?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            
            # Gmail/Yahoo/Outlook specific patterns
            r'\b[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook|hotmail)\.com\b',
            
            # Email with spaces around @ symbol
            r'\b[A-Za-z0-9._%+-]+\s+@\s+[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            
            # Email with 'AT' instead of @
            r'\b[A-Za-z0-9._%+-]+\s*AT\s*[A-Za-z0-9.-]+\s*DOT\s*[A-Z|a-z]{2,}\b',
        ]
        
        for pattern in email_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            if matches:
                # Handle tuple results from group captures
                email = matches[0] if isinstance(matches[0], str) else matches[0]
                
                # Clean up common obfuscations
                email = email.replace('[at]', '@').replace('(at)', '@')
                email = email.replace('[dot]', '.').replace('(dot)', '.')
                email = email.replace(' AT ', '@').replace(' DOT ', '.')
                email = email.replace(' @ ', '@').replace(' ', '')
                
                # Validate the email format
                if re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
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
