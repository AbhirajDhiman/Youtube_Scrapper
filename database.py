import os
import logging
from datetime import datetime
from pymongo import MongoClient, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DatabaseService:
    def __init__(self):
        self.client = None
        self.db = None
        self.connected = False

        # Get MongoDB configuration from environment
        self.mongodb_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
        self.database_name = os.environ.get("MONGODB_DATABASE", "youtube_discovery")

        try:
            self.connect()
        except Exception as e:
            logging.warning(f"Database connection failed: {e}. Running without database.")

    def connect(self):
        """Establish MongoDB connection with timeout"""
        try:
            self.client = MongoClient(
                self.mongodb_uri,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )

            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[self.database_name]

            # Create indexes for better performance
            self._create_indexes()

            self.connected = True
            logging.info("MongoDB connection established successfully")

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logging.warning(f"MongoDB connection failed: {e}")
            self.connected = False
        except Exception as e:
            logging.error(f"Unexpected database error: {e}")
            self.connected = False

    def _create_indexes(self):
        """Create database indexes for performance"""
        try:
            # Search history indexes
            self.db.search_history.create_index([("timestamp", DESCENDING)])
            self.db.search_history.create_index([("keyword", ASCENDING)])

            # Channel data indexes
            self.db.channels.create_index([("channel_id", ASCENDING)], unique=True)
            self.db.channels.create_index([("subscriber_count", DESCENDING)])
            self.db.channels.create_index([("last_updated", DESCENDING)])

        except Exception as e:
            logging.warning(f"Error creating database indexes: {e}")

    def is_connected(self):
        """Check if database is connected"""
        return self.connected

    def save_search_history(self, keyword, results_count, filters=None):
        """Save search to history"""
        if not self.connected:
            return False

        try:
            search_record = {
                "keyword": keyword,
                "results_count": results_count,
                "filters": filters or {},
                "timestamp": datetime.now()
            }

            self.db.search_history.insert_one(search_record)
            return True

        except Exception as e:
            logging.error(f"Error saving search history: {e}")
            return False

    def get_search_history(self, limit=50):
        """Get recent search history"""
        if not self.connected:
            return []

        try:
            cursor = self.db.search_history.find().sort("timestamp", DESCENDING).limit(limit)
            history = []

            for record in cursor:
                record['_id'] = str(record['_id'])  # Convert ObjectId to string
                history.append(record)

            return history

        except Exception as e:
            logging.error(f"Error retrieving search history: {e}")
            return []

    def save_channel_data(self, channel_data):
        """Save or update channel data"""
        if not self.connected:
            return False

        try:
            channel_data['last_updated'] = datetime.now()

            # Use upsert to update existing or insert new
            self.db.channels.update_one(
                {"channel_id": channel_data.get("id")},
                {"$set": channel_data},
                upsert=True
            )
            return True

        except Exception as e:
            logging.error(f"Error saving channel data: {e}")
            return False

    def get_database_stats(self):
        """Get database statistics and analytics"""
        if not self.connected:
            return {}

        try:
            stats = {
                "total_searches": self.db.search_history.count_documents({}),
                "total_channels": self.db.channels.count_documents({}),
                "popular_keywords": [],
                "recent_activity": []
            }

            # Get popular keywords
            pipeline = [
                {"$group": {"_id": "$keyword", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]

            popular_keywords = list(self.db.search_history.aggregate(pipeline))
            stats["popular_keywords"] = [
                {"keyword": item["_id"], "searches": item["count"]} 
                for item in popular_keywords
            ]

            # Get recent activity
            recent_searches = list(
                self.db.search_history.find()
                .sort("timestamp", DESCENDING)
                .limit(10)
            )

            stats["recent_activity"] = [
                {
                    "keyword": search["keyword"],
                    "results": search["results_count"],
                    "timestamp": search["timestamp"],
                    "id": str(search["_id"])
                }
                for search in recent_searches
            ]

            return stats

        except Exception as e:
            logging.error(f"Error getting database stats: {e}")
            return {}

    def close_connection(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            self.connected = False
            logging.info("Database connection closed")