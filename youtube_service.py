
import os
import logging
import re
import requests
import time
import asyncio
import aiohttp
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import urljoin, urlparse
import whois
from bs4 import BeautifulSoup
from functools import lru_cache
import concurrent.futures
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class YouTubeService:
    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        self.youtube = None
        self.quota_exceeded = False
        self.daily_quota_used = 0
        self.max_daily_quota = 10000  # YouTube API v3 default quota
        self.last_reset = datetime.now().date()
        
        # Reset quota if it's a new day
        if self.last_reset < datetime.now().date():
            self.daily_quota_used = 0
            self.quota_exceeded = False
            self.last_reset = datetime.now().date()

        if self.api_key:
            try:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
                logging.info("YouTube API service initialized successfully")
                # Test the API key with a simple request
                self._test_api_key()
            except Exception as e:
                logging.error(f"Failed to initialize YouTube API: {str(e)}")
                self.youtube = None
        else:
            logging.warning("No YouTube API key found in environment variables")
            
    def _test_api_key(self):
        """Test if the API key is valid with a minimal quota request"""
        try:
            if self.youtube:
                test_request = self.youtube.search().list(
                    part='snippet',
                    q='test',
                    type='channel',
                    maxResults=1
                )
                test_request.execute()
                logging.info("API key validation successful")
                return True
        except HttpError as e:
            if e.resp.status == 403:
                logging.error("API key invalid or quota exceeded")
                self.quota_exceeded = True
            else:
                logging.error(f"API key test failed: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"API key test error: {str(e)}")
            return False

    def check_quota_status(self):
        """Check if quota is exceeded and log status"""
        # Reset daily quota if it's a new day
        if self.last_reset < datetime.now().date():
            self.daily_quota_used = 0
            self.quota_exceeded = False
            self.last_reset = datetime.now().date()
            logging.info("Daily quota reset")
            
        if self.quota_exceeded:
            logging.warning("YouTube API quota exceeded. Please wait or use backup API key.")
            return False

        if self.daily_quota_used >= self.max_daily_quota:
            self.quota_exceeded = True
            logging.error(f"Daily quota limit reached: {self.daily_quota_used}/{self.max_daily_quota}")
            return False

        return True

    @lru_cache(maxsize=128)
    def extract_emails_from_text(self, text):
        """Extract email addresses from text using regex with caching"""
        if not text:
            return tuple()  # Return tuple for hashability

        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return tuple(set(emails))  # Remove duplicates and return tuple

    def scrape_website_for_contacts(self, url, timeout=5):
        """Optimized website scraping with reduced timeout"""
        contacts = {
            'emails': [],
            'social_media': {},
            'contact_pages': []
        }

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                text_content = soup.get_text()

                # Extract emails from page content
                emails = self.extract_emails_from_text(text_content)
                contacts['emails'].extend(emails)

                # Look for contact pages (limit to first 5)
                contact_links = soup.find_all('a', href=True)[:20]  # Limit links to check
                for link in contact_links:
                    href = link.get('href', '').lower()
                    if any(keyword in href for keyword in ['contact', 'about']) and len(contacts['contact_pages']) < 3:
                        full_url = urljoin(url, link['href'])
                        contacts['contact_pages'].append(full_url)

                # Extract social media links (simplified patterns)
                social_patterns = {
                    'twitter': r'(?:https?://)?(?:www\.)?(?:twitter\.com|x\.com)/([A-Za-z0-9_]+)',
                    'linkedin': r'(?:https?://)?(?:www\.)?linkedin\.com/(?:in|company)/([A-Za-z0-9_-]+)',
                    'instagram': r'(?:https?://)?(?:www\.)?instagram\.com/([A-Za-z0-9_.]+)',
                }

                for platform, pattern in social_patterns.items():
                    matches = re.findall(pattern, text_content)
                    if matches:
                        contacts['social_media'][platform] = matches[0]

        except Exception as e:
            logging.warning(f"Error scraping website {url}: {str(e)}")

        # Remove duplicates
        contacts['emails'] = list(set(contacts['emails']))
        return contacts

    def get_whois_info(self, domain):
        """Simplified WHOIS info retrieval with timeout"""
        try:
            w = whois.whois(domain)
            whois_info = {
                'emails': [],
                'registrar': getattr(w, 'registrar', None),
                'creation_date': getattr(w, 'creation_date', None)
            }

            # Extract emails from WHOIS data
            if hasattr(w, 'emails') and w.emails:
                if isinstance(w.emails, list):
                    whois_info['emails'] = w.emails[:3]  # Limit emails
                else:
                    whois_info['emails'] = [w.emails]

            return whois_info
        except Exception as e:
            logging.warning(f"Error getting WHOIS for {domain}: {str(e)}")
            return {'emails': [], 'registrar': None, 'creation_date': None}

    def calculate_engagement_rate(self, video_stats):
        """Calculate engagement rate from video statistics"""
        try:
            likes = int(video_stats.get('likeCount', 0))
            comments = int(video_stats.get('commentCount', 0))
            views = int(video_stats.get('viewCount', 0))

            if views == 0:
                return 0

            engagement_rate = ((likes + comments) / views) * 100
            return round(engagement_rate, 2)
        except:
            return 0

    def get_channel_quality_metrics(self, channel_id):
        """Get detailed channel quality metrics with optimization"""
        if not self.check_quota_status():
            return None

        try:
            # Get recent videos (reduced to 5 for speed)
            search_request = self.youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=5,  # Reduced from 10
                order='date',
                type='video'
            )
            search_response = search_request.execute()
            self.daily_quota_used += 100

            video_ids = [item['id']['videoId'] for item in search_response['items']]

            if not video_ids:
                return {
                    'upload_frequency': 0,
                    'avg_views': 0,
                    'avg_engagement_rate': 0,
                    'last_upload_date': None,
                    'total_recent_videos': 0
                }

            # Get video statistics
            videos_request = self.youtube.videos().list(
                part='statistics,snippet',
                id=','.join(video_ids)
            )
            videos_response = videos_request.execute()
            self.daily_quota_used += 1

            # Calculate metrics
            total_views = 0
            total_engagement = 0
            upload_dates = []

            for video in videos_response['items']:
                stats = video['statistics']
                snippet = video['snippet']

                views = int(stats.get('viewCount', 0))
                total_views += views

                engagement = self.calculate_engagement_rate(stats)
                total_engagement += engagement

                # Parse upload date
                try:
                    upload_date = datetime.strptime(snippet['publishedAt'][:10], '%Y-%m-%d')
                    upload_dates.append(upload_date)
                except:
                    pass

            # Calculate averages and frequency
            video_count = len(videos_response['items'])
            avg_views = total_views // video_count if video_count > 0 else 0
            avg_engagement_rate = total_engagement / video_count if video_count > 0 else 0

            # Calculate upload frequency (videos per week)
            if len(upload_dates) > 1:
                date_range = (max(upload_dates) - min(upload_dates)).days
                upload_frequency = (video_count / max(date_range, 1)) * 7  # per week
            else:
                upload_frequency = 0

            last_upload_date = max(upload_dates) if upload_dates else None

            return {
                'upload_frequency': round(upload_frequency, 2),
                'avg_views': avg_views,
                'avg_engagement_rate': round(avg_engagement_rate, 2),
                'last_upload_date': last_upload_date,
                'total_recent_videos': video_count
            }

        except Exception as e:
            logging.error(f"Error getting quality metrics for channel {channel_id}: {str(e)}")
            return {
                'upload_frequency': 0,
                'avg_views': 0,
                'avg_engagement_rate': 0,
                'last_upload_date': None,
                'total_recent_videos': 0
            }

    def search_channels(self, keyword, max_results=50, filters=None):
        """Enhanced channel search with better error handling and performance"""
        if not self.youtube:
            return {'error': 'YouTube API not initialized. Please check your API key in environment variables.'}

        if not self.api_key:
            return {'error': 'YouTube API key not found. Please set GOOGLE_API_KEY environment variable.'}

        if not self.check_quota_status():
            return {'error': 'YouTube API quota exceeded. Please wait 24 hours or use a backup API key.'}

        try:
            all_results = []
            next_page_token = None
            results_per_page = min(max_results, 50)
            max_pages = 2  # Limit to 2 pages for speed

            for page in range(max_pages):
                if len(all_results) >= max_results:
                    break
                    
                # Search for channels
                search_request = self.youtube.search().list(
                    part='snippet',
                    q=keyword,
                    type='channel',
                    maxResults=results_per_page,
                    pageToken=next_page_token
                )

                search_response = search_request.execute()
                self.daily_quota_used += 100

                # Extract channel IDs with enhanced error handling
                channel_ids = []
                for item in search_response.get('items', []):
                    try:
                        # Handle different response structures
                        channel_id = None
                        
                        if 'id' in item:
                            if isinstance(item['id'], dict):
                                # Standard search response format
                                if 'channelId' in item['id']:
                                    channel_id = item['id']['channelId']
                                elif 'kind' in item['id'] and item['id']['kind'] == 'youtube#channel':
                                    # Sometimes channelId is in a different field
                                    channel_id = item['id'].get('channelId')
                            elif isinstance(item['id'], str):
                                # Sometimes ID is a direct string
                                channel_id = item['id']
                        
                        # Fallback: check snippet for channel ID
                        if not channel_id and 'snippet' in item:
                            snippet = item['snippet']
                            if 'channelId' in snippet:
                                channel_id = snippet['channelId']
                        
                        if channel_id and channel_id not in channel_ids:
                            channel_ids.append(channel_id)
                            logging.info(f"Found channel ID: {channel_id}")
                        else:
                            logging.warning(f"Could not extract channelId from item: {item.get('id', 'No ID field')}")
                            
                    except (KeyError, TypeError, AttributeError) as e:
                        logging.warning(f"Error extracting channelId from item: {e}")
                        continue

                if not channel_ids:
                    logging.warning("No valid channel IDs found in search results")
                    break

                # Get detailed channel information
                channels_request = self.youtube.channels().list(
                    part='snippet,statistics,brandingSettings',
                    id=','.join(channel_ids)
                )

                channels_response = channels_request.execute()
                self.daily_quota_used += 1

                # Process channels with parallel contact enrichment
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    futures = []
                    
                    for channel in channels_response['items']:
                        future = executor.submit(self._process_channel, channel, filters)
                        futures.append(future)
                    
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            result = future.result(timeout=10)  # 10 second timeout per channel
                            if result:
                                all_results.append(result)
                                if len(all_results) >= max_results:
                                    break
                        except Exception as e:
                            logging.error(f"Error processing channel: {str(e)}")
                            continue

                # Check for next page
                next_page_token = search_response.get('nextPageToken')
                if not next_page_token:
                    break

                if not self.check_quota_status():
                    break

            return {
                'channels': all_results[:max_results],
                'total_found': len(all_results),
                'quota_used': self.daily_quota_used,
                'quota_limit': self.max_daily_quota,
                'quota_remaining': max(0, self.max_daily_quota - self.daily_quota_used),
                'quota_percentage': (self.daily_quota_used / self.max_daily_quota) * 100,
                'status': 'success'
            }

        except HttpError as e:
            if e.resp.status == 403:
                self.quota_exceeded = True
                error_msg = "YouTube API quota exceeded or invalid API key. Please check your credentials."
                logging.error(error_msg)
                return {'error': error_msg}
            elif e.resp.status == 400:
                error_msg = "Invalid search parameters. Please check your search terms."
                logging.error(error_msg)
                return {'error': error_msg}
            else:
                error_msg = f"YouTube API error: {str(e)}"
                logging.error(error_msg)
                return {'error': error_msg}
        except Exception as e:
            error_msg = f"Error searching channels: {str(e)}"
            logging.error(error_msg)
            return {'error': error_msg}

    def _process_channel(self, channel, filters):
        """Process individual channel with filters and contact enrichment"""
        try:
            # Basic channel info
            snippet = channel['snippet']
            statistics = channel['statistics']
            branding = channel.get('brandingSettings', {})

            # Apply filters if provided
            subscriber_count = int(statistics.get('subscriberCount', 0))
            video_count = int(statistics.get('videoCount', 0))

            if filters:
                if filters.get('min_subscribers') and subscriber_count < filters['min_subscribers']:
                    return None
                if filters.get('max_subscribers') and subscriber_count > filters['max_subscribers']:
                    return None
                if filters.get('min_videos') and video_count < filters['min_videos']:
                    return None
                if filters.get('max_videos') and video_count > filters['max_videos']:
                    return None

            # Get quality metrics (optional for speed)
            quality_metrics = {}
            if subscriber_count > 1000:  # Only get metrics for channels with 1k+ subs
                quality_metrics = self.get_channel_quality_metrics(channel['id']) or {}

            # Filter by activity if specified and metrics available
            if filters and quality_metrics:
                if filters.get('min_upload_frequency') and quality_metrics.get('upload_frequency', 0) < filters['min_upload_frequency']:
                    return None
                if filters.get('max_days_since_upload') and quality_metrics.get('last_upload_date'):
                    days_since = (datetime.now() - quality_metrics['last_upload_date']).days
                    if days_since > filters['max_days_since_upload']:
                        return None

            # Simplified contact information (faster)
            contact_info = {
                'emails': [],
                'social_media': {},
                'website_contacts': {},
                'whois_info': {}
            }

            # Extract emails from description
            description = snippet.get('description', '')
            emails = self.extract_emails_from_text(description)
            contact_info['emails'].extend(emails)

            # Quick URL extraction from description
            website_url = None
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            urls = re.findall(url_pattern, description)

            for url in urls[:3]:  # Limit to first 3 URLs
                if 'youtube.com' not in url and 'youtu.be' not in url:
                    website_url = url
                    break

            # Simplified contact enrichment (only for high-value channels)
            if website_url and subscriber_count > 10000:  # Only scrape for 10k+ channels
                try:
                    domain = urlparse(website_url).netloc
                    website_contacts = self.scrape_website_for_contacts(website_url, timeout=3)
                    contact_info['website_contacts'] = website_contacts
                    contact_info['emails'].extend(website_contacts.get('emails', []))
                except Exception as e:
                    logging.warning(f"Error processing website {website_url}: {str(e)}")

            # Remove duplicate emails
            contact_info['emails'] = list(set(contact_info['emails']))

            result = {
                'id': channel['id'],
                'title': snippet.get('title', 'N/A'),
                'description': description[:500],  # Truncate for speed
                'subscriber_count': subscriber_count,
                'video_count': video_count,
                'view_count': int(statistics.get('viewCount', 0)),
                'thumbnail': snippet.get('thumbnails', {}).get('default', {}).get('url', ''),
                'url': f"https://www.youtube.com/channel/{channel['id']}",
                'website_url': website_url,
                'contact_info': contact_info,
                'quality_metrics': quality_metrics,
                'created_at': snippet.get('publishedAt', ''),
                'country': snippet.get('country', 'Unknown'),
                'custom_url': snippet.get('customUrl', '')
            }

            return result

        except Exception as e:
            logging.error(f"Error processing channel: {str(e)}")
            return None

    def get_quota_status(self):
        """Get current quota usage information with safe fallbacks"""
        # Reset daily quota if it's a new day
        if self.last_reset < datetime.now().date():
            self.daily_quota_used = 0
            self.quota_exceeded = False
            self.last_reset = datetime.now().date()
            
        quota_used = getattr(self, 'daily_quota_used', 0)
        quota_limit = getattr(self, 'max_daily_quota', 10000)

        return {
            'quota_used': quota_used,
            'quota_limit': quota_limit,
            'quota_remaining': max(0, quota_limit - quota_used),
            'quota_percentage': (quota_used / quota_limit) * 100 if quota_limit > 0 else 0,
            'status': 'healthy' if quota_used < quota_limit * 0.8 else 'warning' if quota_used < quota_limit * 0.95 else 'critical',
            'quota_exceeded': self.quota_exceeded
        }
