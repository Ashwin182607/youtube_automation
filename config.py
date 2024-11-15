import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
MUSIC_DIR = os.path.join(MEDIA_DIR, 'music')
BACKGROUNDS_DIR = os.path.join(MEDIA_DIR, 'backgrounds')

# Default paths
DEFAULT_BG = 'default_bg.jpg'

# YouTube settings
YOUTUBE_DEFAULTS = {
    'privacy_status': 'private',
    'category_id': '10',
    'tags': ['chill', 'music', 'relaxing'],
    'description_template': '''🎵 Relaxing Music

Sit back and enjoy ✨

#ChillMusic #Relaxing
'''
}