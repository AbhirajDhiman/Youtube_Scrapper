import os
import csv
import io
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash
from werkzeug.middleware.proxy_fix import ProxyFix
from youtube_service import YouTubeService
from database import DatabaseService

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize services
youtube_service = YouTubeService()
db_service = DatabaseService()

def get_intelligent_filters(keyword):
    """Get smart filter recommendations based on keyword"""
    keyword_lower = keyword.lower()
    
    # Gaming content creator tiers
    if any(game in keyword_lower for game in ['fortnite', 'minecraft', 'gaming', 'rdr2', 'gta', 'cod', 'valorant']):
        return {
            'min_subscribers': '10000',  # Gaming creators need decent following
            'min_videos': '50',          # Active content creators
            'sort_by': 'subscribers'     # Most popular first
        }
    
    # Educational/Tutorial content
    if any(term in keyword_lower for term in ['tutorial', 'guide', 'how to', 'learn', 'education']):
        return {
            'min_subscribers': '5000',
            'min_videos': '20',
            'sort_by': 'videos'
        }
    
    # Entertainment/Vlog content
    if any(term in keyword_lower for term in ['vlog', 'daily', 'lifestyle', 'comedy', 'entertainment']):
        return {
            'min_subscribers': '1000',
            'min_videos': '30',
            'sort_by': 'recent'
        }
    
    # Default for other content
    return {
        'min_subscribers': '1000',
        'min_videos': '10',
        'sort_by': 'relevance'
    }

def expand_search_keywords(keyword):
    """Expand keywords to find similar creators"""
    keyword_lower = keyword.lower()
    
    # Gaming expansions
    gaming_expansions = {
        'fortnite': ['fortnite gaming', 'fortnite battle royale', 'fortnite creative'],
        'minecraft': ['minecraft gaming', 'minecraft survival', 'minecraft builds', 'minecraft mods'],
        'rdr2': ['red dead redemption', 'rdr2 gaming', 'western gaming'],
        'hindi gaming': ['indian gaming', 'hindi gameplay', 'indian streamers'],
        'english gaming': ['gaming commentary', 'english gameplay', 'gaming reviews']
    }
    
    for base_term, expansions in gaming_expansions.items():
        if base_term in keyword_lower:
            return expansions
    
    return [keyword]

def apply_enhanced_filters(channels, min_subscribers, max_subscribers, min_videos, sort_by):
    """Apply enhanced filtering and sorting to channel results"""
    filtered_channels = []
    
    for channel in channels:
        # Convert string numbers to integers for comparison
        try:
            subscriber_count = int(channel.get('subscriber_count', '0').replace(',', ''))
            video_count = int(channel.get('video_count', '0').replace(',', ''))
            view_count = int(channel.get('view_count', '0').replace(',', ''))
        except (ValueError, AttributeError):
            subscriber_count = 0
            video_count = 0
            view_count = 0
        
        # Store numeric values for easier processing
        channel['subscriber_count_num'] = subscriber_count
        channel['video_count_num'] = video_count
        channel['view_count_num'] = view_count
        
        # Calculate advanced engagement metrics
        try:
            if subscriber_count > 0:
                views_per_subscriber = view_count / subscriber_count
                videos_per_year = video_count / max(1, ((2024 - int(channel.get('published_at', '2020')[:4])) or 1))
                engagement_score = (views_per_subscriber * 0.7) + (videos_per_year * 0.3)
            else:
                views_per_subscriber = 0
                videos_per_year = 0
                engagement_score = 0
                
            channel['views_per_subscriber'] = views_per_subscriber
            channel['videos_per_year'] = videos_per_year
            channel['engagement_score'] = engagement_score
        except:
            channel['views_per_subscriber'] = 0
            channel['videos_per_year'] = 0
            channel['engagement_score'] = 0
        
        # Apply subscriber filters with better handling
        if min_subscribers:
            try:
                min_sub_value = int(min_subscribers)
                if subscriber_count < min_sub_value:
                    continue
            except ValueError:
                pass
                
        if max_subscribers:
            try:
                max_sub_value = int(max_subscribers)
                if subscriber_count > max_sub_value:
                    continue
            except ValueError:
                pass
            
        # Apply video count filter
        if min_videos:
            try:
                min_video_value = int(min_videos)
                if video_count < min_video_value:
                    continue
            except ValueError:
                pass
        
        # Quality filters - exclude channels with suspicious metrics
        if subscriber_count > 0 and video_count > 0:
            # Skip channels with unusually low engagement (potential inactive channels)
            if views_per_subscriber < 0.1 and subscriber_count > 1000:
                continue
                
        filtered_channels.append(channel)
    
    # Enhanced sorting options
    if sort_by == 'subscribers':
        filtered_channels.sort(key=lambda x: x.get('subscriber_count_num', 0), reverse=True)
    elif sort_by == 'videos':
        filtered_channels.sort(key=lambda x: x.get('video_count_num', 0), reverse=True)
    elif sort_by == 'engagement':
        filtered_channels.sort(key=lambda x: x.get('engagement_score', 0), reverse=True)
    elif sort_by == 'recent':
        filtered_channels.sort(key=lambda x: x.get('published_at', ''), reverse=True)
    elif sort_by == 'email_first':
        # Sort by email availability first, then by subscribers
        filtered_channels.sort(key=lambda x: (
            bool(x.get('email')),
            x.get('subscriber_count_num', 0)
        ), reverse=True)
    else:  # relevance or default
        # Sort by a combination of factors for relevance
        filtered_channels.sort(key=lambda x: (
            bool(x.get('email')) * 1000000,  # Prioritize channels with email
            x.get('engagement_score', 0) * 1000,
            x.get('subscriber_count_num', 0)
        ), reverse=True)
    
    return filtered_channels

# Keep the old function for backward compatibility
def apply_filters(channels, min_subscribers, max_subscribers, min_videos, sort_by):
    """Legacy filter function - redirects to enhanced version"""
    return apply_enhanced_filters(channels, min_subscribers, max_subscribers, min_videos, sort_by)

@app.route('/')
def index():
    """Home page with search form"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle YouTube channel search with enhanced volume and filtering"""
    keyword = request.form.get('keyword', '').strip()
    
    if not keyword:
        flash('Please enter a search keyword.', 'warning')
        return redirect(url_for('index'))
    
    # Get filter parameters
    min_subscribers = request.form.get('min_subscribers', '')
    max_subscribers = request.form.get('max_subscribers', '')
    min_videos = request.form.get('min_videos', '')
    sort_by = request.form.get('sort_by', 'relevance')
    
    # Get target results (default to 50 for high volume)
    target_results = int(request.form.get('target_results', '50'))
    
    try:
        # Always fetch fresh results for better volume and accuracy
        app.logger.info(f"Starting enhanced search for '{keyword}' targeting {target_results} results")
        
        # Use enhanced search with higher target
        channels = youtube_service.search_channels(keyword, max_results=target_results * 2)  # Search for more than needed
        
        app.logger.info(f"Raw search returned {len(channels)} channels")
        
        # Apply filters BEFORE limiting results
        if channels:
            original_count = len(channels)
            
            # Apply filters with enhanced logic
            channels = apply_enhanced_filters(channels, min_subscribers, max_subscribers, min_videos, sort_by)
            
            app.logger.info(f"After filtering: {len(channels)} channels remaining from {original_count}")
            
            # Limit to target results after filtering
            channels = channels[:target_results]
        
        # Store search in history
        if 'search_history' not in session:
            session['search_history'] = []
        
        search_entry = {
            'keyword': keyword,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'results_count': len(channels),
            'filters_applied': {
                'min_subscribers': min_subscribers,
                'max_subscribers': max_subscribers,
                'min_videos': min_videos,
                'sort_by': sort_by
            }
        }
        
        session['search_history'].insert(0, search_entry)
        session['search_history'] = session['search_history'][:50]
        session.modified = True
        
        # Save to database if connected
        if db_service.is_connected():
            session_id = session.get('session_id', str(id(session)))
            db_service.save_search_history(keyword, len(channels), session_id)
        
        if not channels:
            flash(f'No channels found matching your criteria for keyword: {keyword}', 'info')
            return redirect(url_for('index'))
        
        # Add pagination info
        pagination_info = {
            'total_results': len(channels),
            'has_email': len([ch for ch in channels if ch.get('email')]),
            'filters_applied': bool(min_subscribers or max_subscribers or min_videos or sort_by != 'relevance')
        }
        
        return render_template('results.html', 
                             channels=channels, 
                             keyword=keyword, 
                             pagination=pagination_info)
        
    except Exception as e:
        app.logger.error(f"Search error for keyword '{keyword}': {str(e)}")
        flash(f'Error searching for channels: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/history')
def history():
    """Display search history"""
    # Get history from database if available, otherwise use session
    search_history = []
    
    if db_service.is_connected():
        session_id = session.get('session_id', str(id(session)))
        search_history = db_service.get_search_history(session_id)
    
    # Fallback to session history if database not available
    if not search_history:
        search_history = session.get('search_history', [])
    
    return render_template('history.html', search_history=search_history)

@app.route('/clear_history')
def clear_history():
    """Clear search history"""
    # Clear from database if connected
    if db_service.is_connected():
        session_id = session.get('session_id', str(id(session)))
        db_service.clear_search_history(session_id)
    
    # Clear session history
    session.pop('search_history', None)
    flash('Search history cleared successfully.', 'success')
    return redirect(url_for('history'))

@app.route('/stats')
def stats():
    """Display database statistics"""
    if not db_service.is_connected():
        flash('Database not connected. Statistics not available.', 'warning')
        return redirect(url_for('index'))
    
    try:
        db_stats = db_service.get_database_stats()
        popular_keywords = db_service.get_popular_keywords(10)
        
        return render_template('stats.html', 
                             db_stats=db_stats, 
                             popular_keywords=popular_keywords)
    except Exception as e:
        app.logger.error(f"Error getting database statistics: {str(e)}")
        flash('Error retrieving database statistics.', 'danger')
        return redirect(url_for('index'))

@app.route('/export_csv')
def export_csv():
    """Export last search results to CSV"""
    keyword = request.args.get('keyword', '')
    
    if not keyword:
        flash('No search results to export.', 'warning')
        return redirect(url_for('index'))
    
    try:
        # Re-fetch the channels for export
        channels = youtube_service.search_channels(keyword)
        
        if not channels:
            flash('No channels found to export.', 'warning')
            return redirect(url_for('index'))
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header with email field
        writer.writerow(['Channel Name', 'Channel ID', 'Subscriber Count', 'Video Count', 'Email', 'Description', 'Published Date', 'Country'])
        
        # Write channel data including email
        for channel in channels:
            writer.writerow([
                channel['title'],
                channel['channel_id'],
                channel['subscriber_count'],
                channel['video_count'],
                channel.get('email', 'Not found'),
                channel['description'][:100] + '...' if len(channel['description']) > 100 else channel['description'],
                channel['published_at'],
                channel.get('country', 'N/A')
            ])
        
        # Create response
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=youtube_channels_{keyword.replace(" ", "_")}.csv'
        
        return response
        
    except Exception as e:
        app.logger.error(f"Export error for keyword '{keyword}': {str(e)}")
        flash(f'Error exporting data: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f"Internal server error: {str(error)}")
    flash('An internal error occurred. Please try again.', 'danger')
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
