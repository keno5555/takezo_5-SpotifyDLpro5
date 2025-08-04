"""
Configuration settings for the Telegram Music Bot
"""

import os

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Spotify API Configuration
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Bot Settings
MAX_PLAYLIST_SIZE = 50  # Maximum number of songs to process from a playlist
DOWNLOAD_TIMEOUT = 300  # 5 minutes timeout for downloads
CONCURRENT_DOWNLOADS = 3  # Maximum concurrent downloads

# Quality Options
QUALITY_OPTIONS = {
    "✨ Standard (128kbps)": "128",
    "🚀 High (192kbps)": "192", 
    "💎 Premium (320kbps)": "320"
}

# Bot Messages
BOT_WELCOME = """🎵 *Welcome to MusicFlow Bot!* 🎵

Your personal music companion for seamless downloads! ✨

🌟 *What I can do for you:*
• 🎶 Download individual tracks instantly via multiple sources
• 🎧 Process entire playlists effortlessly  
• 🎯 Multiple quality options available
• ⚡ Lightning-fast processing with smart fallback system
• 🔄 Auto-retry with Y2Mate → OnlyMP3 → MP3Juices
• 🎪 Try demo tracks to test functionality

Simply share any music link and let the magic happen! 🪄

*Ready to get started?* Choose an option below! 👇"""

BOT_HELP = """🎯 *How to use MusicFlow Bot:*

1️⃣ *For Single Tracks:*
   • Share any music platform link
   • Choose your preferred quality
   • Auto-download with smart source selection!

2️⃣ *For Playlists:*
   • Share a playlist link
   • I'll process all tracks for you
   • Sit back and enjoy! ☕

3️⃣ *Quality Options:*
   • ✨ Standard (128kbps) - Good quality, smaller size
   • 🚀 High (192kbps) - Better quality, balanced
   • 💎 Premium (320kbps) - Best quality, larger size

💡 *Pro Tips:*
• Multi-source system: Y2Mate → OnlyMP3 → MP3Juices
• Automatic fallback ensures maximum success rate
• Processing time varies by content length
• Playlists are processed sequentially
• Use /start to return to main menu

Need more help? Just ask! 😊"""

# Demo Songs Configuration
DEMO_ROTATION_SIZE = 10  # Number of demo songs to rotate through
