"""
Flask web application to keep the bot alive on Render.
This runs alongside the Telegram bot to satisfy Render's web service requirements.
"""

from flask import Flask, jsonify, render_template
import threading
import time
import os
import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot.handlers import (
    start_command, help_command, handle_spotify_url, 
    handle_button_callback, handle_message
)

app = Flask(__name__)
bot_status = {"running": False, "last_seen": 0}

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

@app.route('/')
def home():
    """Beautiful status page for the bot."""
    return render_template('status.html')

@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy", 
        "timestamp": time.time(),
        "bot_running": bot_status["running"],
        "service": "keep_alive"
    })

@app.route('/ping')
def ping():
    """Simple ping endpoint for external monitoring."""
    return "pong"

@app.route('/json')
def json_status():
    """JSON status endpoint for monitoring tools."""
    return jsonify({
        "status": "✅ Bot is alive and running!",
        "service": "Telegram Music Bot",
        "message": "Keep-alive server active - bot stays online 24/7",
        "last_seen": bot_status["last_seen"],
        "uptime": time.time() - bot_status.get("start_time", time.time())
    })

@app.route('/api/status')
def api_status():
    """API endpoint for status page to fetch real-time data."""
    return jsonify({
        "bot_running": bot_status["running"],
        "uptime": time.time() - bot_status.get("start_time", time.time()),
        "last_seen": bot_status["last_seen"],
        "service": "MusicFlow Bot"
    })

def keep_alive():
    """Keep alive function to prevent bot from sleeping."""
    print("🚀 Starting keep_alive server on port 8080...")
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

def run_flask():
    """Run Flask app on the specified port."""
    port = int(os.environ.get('PORT', 8080))  # Default to 8080 as requested
    print(f"🌐 Flask keep-alive server starting on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def run_telegram_bot():
    """Run the Telegram bot directly in this process."""
    logger = logging.getLogger(__name__)
    
    while True:
        try:
            print("Starting Telegram bot...")
            bot_status["running"] = True
            bot_status["last_seen"] = time.time()
            bot_status["start_time"] = time.time()
            
            # Get bot token from environment
            bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
            if not bot_token:
                logger.error("TELEGRAM_BOT_TOKEN environment variable is required")
                bot_status["running"] = False  
                time.sleep(30)
                continue
            
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Create application
            application = Application.builder().token(bot_token).build()
            
            # Add handlers
            application.add_handler(CommandHandler("start", start_command))
            application.add_handler(CommandHandler("help", help_command))
            application.add_handler(CallbackQueryHandler(handle_button_callback))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
            
            # Start the bot
            logger.info("Telegram Music Bot starting...")
            
            # Update status periodically
            def update_status():
                while bot_status["running"]:
                    bot_status["last_seen"] = time.time()
                    time.sleep(5)
            
            status_thread = threading.Thread(target=update_status, daemon=True)
            status_thread.start()
            
            # Run bot
            application.run_polling()
            
        except Exception as e:
            logger.error(f"Bot error: {e}")
            bot_status["running"] = False
            print(f"Bot error: {e}")
            print("Restarting bot in 30 seconds...")
            time.sleep(30)

if __name__ == '__main__':
    print("🎵 Starting Telegram Music Bot with Keep-Alive System...")
    
    # Initialize bot status
    bot_status["start_time"] = time.time()
    
    # Start keep_alive Flask server in a separate thread
    flask_thread = threading.Thread(target=keep_alive, daemon=True)
    flask_thread.start()
    
    # Give Flask a moment to start
    time.sleep(2)
    
    # Run the Telegram bot in the main thread (required for asyncio)
    print("🤖 Starting Telegram bot in main thread...")
    run_telegram_bot()