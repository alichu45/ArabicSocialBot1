import os

class Config:
    """Base configuration."""
    # Flask settings
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev_secret_key')
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///social_bot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # DeepSeek AI API settings
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
    
    # Social Media API keys
    # Twitter/X
    TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY', '')
    TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET', '')
    TWITTER_CALLBACK_URL = os.environ.get('TWITTER_CALLBACK_URL', 'http://localhost:5000/accounts/twitter/callback')
    
    # Facebook
    FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID', '')
    FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET', '')
    FACEBOOK_CALLBACK_URL = os.environ.get('FACEBOOK_CALLBACK_URL', 'http://localhost:5000/accounts/facebook/callback')
    
    # Instagram
    INSTAGRAM_APP_ID = os.environ.get('INSTAGRAM_APP_ID', '')
    INSTAGRAM_APP_SECRET = os.environ.get('INSTAGRAM_APP_SECRET', '')
    INSTAGRAM_CALLBACK_URL = os.environ.get('INSTAGRAM_CALLBACK_URL', 'http://localhost:5000/accounts/instagram/callback')
    
    # TikTok
    TIKTOK_CLIENT_KEY = os.environ.get('TIKTOK_CLIENT_KEY', '')
    TIKTOK_CLIENT_SECRET = os.environ.get('TIKTOK_CLIENT_SECRET', '')
    TIKTOK_CALLBACK_URL = os.environ.get('TIKTOK_CALLBACK_URL', 'http://localhost:5000/accounts/tiktok/callback')
    
    # Threads (Meta)
    THREADS_APP_ID = os.environ.get('THREADS_APP_ID', '')
    THREADS_APP_SECRET = os.environ.get('THREADS_APP_SECRET', '')
    THREADS_CALLBACK_URL = os.environ.get('THREADS_CALLBACK_URL', 'http://localhost:5000/accounts/threads/callback')
