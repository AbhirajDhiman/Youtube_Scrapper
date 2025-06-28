
from app import app
import os

if __name__ == '__main__':
    # Ensure we bind to 0.0.0.0 for Replit accessibility
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
