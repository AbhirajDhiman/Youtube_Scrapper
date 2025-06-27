
import os
import logging
import re
import requests
import time
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import urljoin, urlparse
import whois
from bs4 import BeautifulSoup

class YouTubeService:
    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        self.youtube = None
        self.quota_exceeded = False
        self.daily_quota_used = 0
        self.max_daily_quota = 10000  # YouTube API v3 default quota

        if self.api_key:
            try:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
                logging.info("YouTube API service initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize YouTube API: {str(e)}")
        else:
            logging.warning("No YouTube API key found in environment variables")

    def check_quota_status(self):
        """Check if quota is exceeded and log status"""
        if self.quota_exceeded:
            logging.warning("YouTube API quota exceeded. Please wait or use backup API key.")
            return False

        if self.daily_quota_used >= self.max_daily_quota:
            self.quota_exceeded = True
            logging.error(f"Daily quota limit reached: {self.daily_quota_used}/{self.max_daily_quota}")
            return False

        return True

    def extract_emails_from_text(self, text):
        """Extract email addresses from text using regex"""
        if not text:
            return []

        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))  # Remove duplicates

    def scrape_website_for_contacts(self, url, timeout=10):
        """Scrape website for contact information"""
        contacts = {
            'emails': [],
            'social_media': {},
            'contact_pages': []
        }

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                text_content = soup.get_text()

                # Extract emails from page content
                contacts['emails'].extend(self.extract_emails_from_text(text_content))

                # Look for contact pages
                contact_links = soup.find_all('a', href=True)
                for link in contact_links:
                    href = link.get('href', '').lower()
                    if any(keyword in href for keyword in ['contact', 'about', 'privacy', 'terms']):
                        full_url = urljoin(url, link['href'])
                        contacts['contact_pages'].append(full_url)

                # Extract social media links
                social_patterns = {
                    'twitter': r'(?:https?://)?(?:www\.)?twitter\.com/([A-Za-z0-9_]+)',
                    'linkedin': r'(?:https?://)?(?:www\.)?linkedin\.com/(?:in|company)/([A-Za-z0-9_-]+)',
                    'instagram': r'(?:https?://)?(?:www\.)?instagram\.com/([A-Za-z0-9_.]+)',
                    'facebook': r'(?:https?://)?(?:www\.)?facebook\.com/([A-Za-z0-9_.]+)'
                }

                for platform, pattern in social_patterns.items():
                    matches = re.findall(pattern, text_content)
                    if matches:
                        contacts['social_media'][platform] = matches[0]

                # Scrape additional contact pages
                for contact_url in contacts['contact_pages'][:3]:  # Limit to 3 pages
                    try:
                        contact_response = requests.get(contact_url, headers=headers, timeout=5)
                        if contact_response.status_code == 200:
                            contact_soup = BeautifulSoup(contact_response.content, 'html.parser')
                            contact_text = contact_soup.get_text()
                            contacts['emails'].extend(self.extract_emails_from_text(contact_text))
                    except:
                        continue

        except Exception as e:
            logging.warning(f"Error scraping website {url}: {str(e)}")

        # Remove duplicates
        contacts['emails'] = list(set(contacts['emails']))
        return contacts

    def get_whois_info(self, domain):
        """Get WHOIS information for a domain"""
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
                    whois_info['emails'] = w.emails
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
        """Get detailed channel quality metrics"""
        if not self.check_quota_status():
            return None

        try:
            # Get recent videos (last 10)
            search_request = self.youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=10,
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
                upload_date = datetime.strptime(snippet['publishedAt'][:10], '%Y-%m-%d')
                upload_dates.append(upload_date)

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
            return None

    def search_channels(self, keyword, max_results=50, filters=None):
        """Enhanced channel search with contact enrichment and quality metrics"""
        if not self.youtube:
            return {'error': 'YouTube API not initialized. Please check your API key.'}

        if not self.check_quota_status():
            return {'error': 'YouTube API quota exceeded. Please wait or use backup API key.'}

        try:
            all_results = []
            next_page_token = None
            results_per_page = min(max_results, 50)

            while len(all_results) < max_results:
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

                channel_ids = [item['id']['channelId'] for item in search_response['items']]

                if not channel_ids:
                    break

                # Get detailed channel information
                channels_request = self.youtube.channels().list(
                    part='snippet,statistics,brandingSettings',
                    id=','.join(channel_ids)
                )

                channels_response = channels_request.execute()
                self.daily_quota_used += 1

                for channel in channels_response['items']:
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
                                continue
                            if filters.get('max_subscribers') and subscriber_count > filters['max_subscribers']:
                                continue
                            if filters.get('min_videos') and video_count < filters['min_videos']:
                                continue
                            if filters.get('max_videos') and video_count > filters['max_videos']:
                                continue

                        # Get quality metrics
                        quality_metrics = self.get_channel_quality_metrics(channel['id'])

                        # Filter by activity if specified
                        if filters and quality_metrics:
                            if filters.get('min_upload_frequency') and quality_metrics['upload_frequency'] < filters['min_upload_frequency']:
                                continue
                            if filters.get('max_days_since_upload'):
                                if quality_metrics['last_upload_date']:
                                    days_since = (datetime.now() - quality_metrics['last_upload_date']).days
                                    if days_since > filters['max_days_since_upload']:
                                        continue

                        # Enhanced contact information
                        contact_info = {
                            'emails': [],
                            'social_media': {},
                            'website_contacts': {},
                            'whois_info': {}
                        }

                        # Extract emails from description
                        description = snippet.get('description', '')
                        contact_info['emails'].extend(self.extract_emails_from_text(description))

                        # Get website from branding settings
                        website_url = None
                        if 'channel' in branding and 'unsubscribedTrailer' in branding['channel']:
                            # Try to extract website from channel art or links
                            pass

                        # Check for custom URL or website in description
                        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
                        urls = re.findall(url_pattern, description)

                        for url in urls:
                            if 'youtube.com' not in url and 'youtu.be' not in url:
                                website_url = url
                                break

                        # Scrape website for additional contacts
                        if website_url:
                            try:
                                domain = urlparse(website_url).netloc
                                website_contacts = self.scrape_website_for_contacts(website_url)
                                contact_info['website_contacts'] = website_contacts

                                # Get WHOIS info
                                whois_info = self.get_whois_info(domain)
                                contact_info['whois_info'] = whois_info
                                contact_info['emails'].extend(whois_info.get('emails', []))

                            except Exception as e:
                                logging.warning(f"Error processing website {website_url}: {str(e)}")

                        # Remove duplicate emails
                        contact_info['emails'] = list(set(contact_info['emails']))

                        result = {
                            'id': channel['id'],
                            'title': snippet.get('title', 'N/A'),
                            'description': description,
                            'subscriber_count': subscriber_count,
                            'video_count': video_count,
                            'view_count': int(statistics.get('viewCount', 0)),
                            'thumbnail': snippet.get('thumbnails', {}).get('default', {}).get('url', ''),
                            'url': f"https://www.youtube.com/channel/{channel['id']}",
                            'website_url': website_url,
                            'contact_info': contact_info,
                            'quality_metrics': quality_metrics or {},
                            'created_at': snippet.get('publishedAt', ''),
                            'country': snippet.get('country', 'Unknown'),
                            'custom_url': snippet.get('customUrl', '')
                        }

                        all_results.append(result)

                        if len(all_results) >= max_results:
                            break

                    except Exception as e:
                        logging.error(f"Error processing channel: {str(e)}")
                        continue

                # Check for next page
                next_page_token = search_response.get('nextPageToken')
                if not next_page_token or len(all_results) >= max_results:
                    break

                if not self.check_quota_status():
                    break

            return {
                'channels': all_results[:max_results],
                'total_found': len(all_results),
                'quota_used': self.daily_quota_used,
                'quota_remaining': self.max_daily_quota - self.daily_quota_used
            }

        except HttpError as e:
            if e.resp.status == 403:
                self.quota_exceeded = True
                error_msg = "YouTube API quota exceeded. Please wait 24 hours or use a backup API key."
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

    def get_quota_status(self):
        """Get current quota usage information with safe fallbacks"""
        quota_used = getattr(self, 'daily_quota_used', 0)
        quota_limit = getattr(self, 'max_daily_quota', 10000)

        return {
            'quota_used': quota_used,
            'quota_limit': quota_limit,
            'quota_remaining': max(0, quota_limit - quota_used),
            'quota_percentage': (quota_used / quota_limit) * 100 if quota_limit > 0 else 0,
            'status': 'healthy' if quota_used < quota_limit * 0.8 else 'warning' if quota_used < quota_limit * 0.95 else 'critical'
        }
