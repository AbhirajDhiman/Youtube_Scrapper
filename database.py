import os
import logging
from datetime import datetime
from pymongo import MongoClient, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

class DatabaseService:
    """MongoDB database service for YouTube Channel Discovery app"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.search_history_collection = None
        self.channels_collection = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize MongoDB connection"""
        try:
            # Get MongoDB connection string from environment
            mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
            
            # Connect to MongoDB
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            
            # Test connection
            self.client.admin.command('ping')
            
            # Select database
            db_name = os.environ.get('MONGODB_DATABASE', 'youtube_discovery')
            self.db = self.client[db_name]
            
            # Get collections
            self.search_history_collection = self.db.search_history
            self.channels_collection = self.db.channels
            
            # Create indexes
            self._create_indexes()
            
            logging.info(f"MongoDB connected successfully to database: {db_name}")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logging.warning(f"MongoDB connection failed: {str(e)}")
            logging.warning("Continuing without database. Search history will be session-based only.")
            self.client = None
            self.db = None
        except Exception as e:
            logging.error(f"Unexpected database error: {str(e)}")
            self.client = None
            self.db = None
    
    def _create_indexes(self):
        """Create database indexes for better performance"""
        try:
            # Search history indexes
            self.search_history_collection.create_index([
                ("timestamp", DESCENDING)
            ])
            self.search_history_collection.create_index([
                ("keyword", 1)
            ])
            
            # Channels indexes
            self.channels_collection.create_index([
                ("channel_id", 1)
            ], unique=True)
            self.channels_collection.create_index([
                ("keyword", 1),
                ("last_updated", DESCENDING)
            ])
            self.channels_collection.create_index([
                ("subscriber_count_numeric", DESCENDING)
            ])
            
            logging.info("Database indexes created successfully")
            
        except Exception as e:
            logging.error(f"Error creating indexes: {str(e)}")
    
    def is_connected(self):
        """Check if database is connected"""
        return self.client is not None and self.db is not None
    
    def save_search_history(self, keyword, results_count, user_session_id=None):
        """Save search history to database"""
        if not self.is_connected():
            return False
        
        try:
            search_entry = {
                "keyword": keyword,
                "results_count": results_count,
                "timestamp": datetime.utcnow(),
                "user_session_id": user_session_id
            }
            
            result = self.search_history_collection.insert_one(search_entry)
            logging.info(f"Search history saved with ID: {result.inserted_id}")
            return True
            
        except Exception as e:
            logging.error(f"Error saving search history: {str(e)}")
            return False
    
    def get_search_history(self, user_session_id=None, limit=50):
        """Get search history from database"""
        if not self.is_connected():
            return []
        
        try:
            query = {}
            if user_session_id:
                query["user_session_id"] = user_session_id
            
            cursor = self.search_history_collection.find(query).sort("timestamp", DESCENDING).limit(limit)
            
            history = []
            for entry in cursor:
                history.append({
                    "keyword": entry["keyword"],
                    "results_count": entry["results_count"],
                    "timestamp": entry["timestamp"].strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return history
            
        except Exception as e:
            logging.error(f"Error retrieving search history: {str(e)}")
            return []
    
    def save_channels(self, keyword, channels):
        """Save channel data to database"""
        if not self.is_connected():
            return False
        
        try:
            for channel in channels:
                # Convert subscriber count to numeric for sorting
                subscriber_count_str = channel.get('subscriber_count', '0').replace(',', '')
                try:
                    subscriber_count_numeric = int(subscriber_count_str)
                except ValueError:
                    subscriber_count_numeric = 0
                
                channel_doc = {
                    "channel_id": channel["channel_id"],
                    "title": channel["title"],
                    "description": channel["description"],
                    "subscriber_count": channel["subscriber_count"],
                    "subscriber_count_numeric": subscriber_count_numeric,
                    "video_count": channel["video_count"],
                    "view_count": channel["view_count"],
                    "published_at": channel["published_at"],
                    "thumbnail_url": channel["thumbnail_url"],
                    "custom_url": channel["custom_url"],
                    "country": channel["country"],
                    "email": channel.get("email"),  # Add email field to database
                    "keyword": keyword,
                    "last_updated": datetime.utcnow()
                }
                
                # Upsert channel data
                self.channels_collection.update_one(
                    {"channel_id": channel["channel_id"]},
                    {"$set": channel_doc},
                    upsert=True
                )
            
            logging.info(f"Saved {len(channels)} channels for keyword: {keyword}")
            return True
            
        except Exception as e:
            logging.error(f"Error saving channels: {str(e)}")
            return False
    
    def get_channels(self, keyword, limit=50):
        """Get cached channel data from database"""
        if not self.is_connected():
            return []
        
        try:
            # Get channels for this keyword, updated within last 24 hours
            yesterday = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            
            cursor = self.channels_collection.find({
                "keyword": keyword,
                "last_updated": {"$gte": yesterday}
            }).sort("subscriber_count_numeric", DESCENDING).limit(limit)
            
            channels = []
            for channel in cursor:
                channels.append({
                    "channel_id": channel["channel_id"],
                    "title": channel["title"],
                    "description": channel["description"],
                    "subscriber_count": channel["subscriber_count"],
                    "video_count": channel["video_count"],
                    "view_count": channel["view_count"],
                    "published_at": channel["published_at"],
                    "thumbnail_url": channel["thumbnail_url"],
                    "custom_url": channel["custom_url"],
                    "country": channel["country"]
                })
            
            return channels
            
        except Exception as e:
            logging.error(f"Error retrieving channels: {str(e)}")
            return []
    
    def get_popular_keywords(self, limit=10):
        """Get most popular search keywords"""
        if not self.is_connected():
            return []
        
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$keyword",
                        "search_count": {"$sum": 1},
                        "total_results": {"$sum": "$results_count"},
                        "last_searched": {"$max": "$timestamp"}
                    }
                },
                {
                    "$sort": {"search_count": -1}
                },
                {
                    "$limit": limit
                }
            ]
            
            cursor = self.search_history_collection.aggregate(pipeline)
            
            keywords = []
            for item in cursor:
                keywords.append({
                    "keyword": item["_id"],
                    "search_count": item["search_count"],
                    "total_results": item["total_results"],
                    "last_searched": item["last_searched"].strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return keywords
            
        except Exception as e:
            logging.error(f"Error getting popular keywords: {str(e)}")
            return []
    
    def clear_search_history(self, user_session_id=None):
        """Clear search history"""
        if not self.is_connected():
            return False
        
        try:
            query = {}
            if user_session_id:
                query["user_session_id"] = user_session_id
            
            result = self.search_history_collection.delete_many(query)
            logging.info(f"Cleared {result.deleted_count} search history entries")
            return True
            
        except Exception as e:
            logging.error(f"Error clearing search history: {str(e)}")
            return False
    
    def get_database_stats(self):
        """Get database statistics"""
        if not self.is_connected():
            return {}
        
        try:
            stats = {
                "total_searches": self.search_history_collection.count_documents({}),
                "total_channels": self.channels_collection.count_documents({}),
                "unique_keywords": len(self.search_history_collection.distinct("keyword"))
            }
            return stats
            
        except Exception as e:
            logging.error(f"Error getting database stats: {str(e)}")
            return {}
    
    def close_connection(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logging.info("MongoDB connection closed")