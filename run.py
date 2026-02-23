import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file FIRST
# This must happen before importing create_app
load_dotenv()

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from app import create_app

config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=True, port=5000)