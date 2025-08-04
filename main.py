#!/usr/bin/env python3
"""
Telegram Music Bot - Main Entry Point
Provides seamless music downloads with interactive buttons and quality selection.
Runs with Flask web server for Render deployment.
"""

import logging
import os
import threading
import time
import asyncio
from flask import Flask, jsonify, render_template
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot.handlers import (
    start_command, help_command, handle_spotify_url, 
    handle_button_callback, handle_message
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask app for Render web service
app = Flask(__name__)
bot_status = {"running": False, "start_time": time.time(), "last_seen": 0}

@app.route('/')
def home():
    """Simple status page."""
    return "SpotifyPulse bot is running!"

@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy", 
        "timestamp": time.time(),
        "bot_running": bot_status["running"],
        "service": "Telegram Music Bot"
    })

@app.route('/status')
def status_page():
    """Beautiful status page for the bot."""
    try:
        return render_template('status.html')
    except:
        # Fallback if template doesn't exist
        return f"""
        <html>
        <head><title>MusicFlow Bot Status</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🎵 MusicFlow Bot Status</h1>
            <p>Bot is {'✅ Running' if bot_status['running'] else '❌ Stopped'}</p>
            <p>Uptime: {int(time.time() - bot_status['start_time'])} seconds</p>
            <p>Service: Telegram Music Download Bot</p>
        </body>
        </html>
        """

@app.route('/api/status')
def api_status():
    """API endpoint for status page to fetch real-time data."""
    return jsonify({
        "bot_running": bot_status["running"],
        "uptime": time.time() - bot_status.get("start_time", time.time()),
        "last_seen": bot_status["last_seen"],
        "service": "MusicFlow Bot"
    })

async def run_telegram_bot_async():
    """Run the Telegram bot asynchronously."""
    try:
        # Get bot token from environment
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            logger.error("TELEGRAM_BOT_TOKEN environment variable is required")
            return
        
        # Create application
        application = Application.builder().token(bot_token).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CallbackQueryHandler(handle_button_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Update bot status
        bot_status["running"] = True
        bot_status["last_seen"] = time.time()
        
        # Start the bot
        logger.info("Starting Telegram Music Bot...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        # Keep running
        while True:
            bot_status["last_seen"] = time.time()
            await asyncio.sleep(1)
        
    except Exception as e:
        logger.error(f"Error running Telegram bot: {e}")
        bot_status["running"] = False

def run_telegram_bot():
    """Run the Telegram bot in a separate thread with asyncio."""
    try:
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_telegram_bot_async())
    except Exception as e:
        logger.error(f"Error in bot thread: {e}")
        bot_status["running"] = False

def main():
    """Initialize and run both Flask web server and Telegram bot."""
    print("🎵 Starting Telegram Music Bot with Flask Web Server...")
    
    # Get port from environment (Render provides this dynamically)
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Port configuration: {port} (from PORT env var)")
    
    # Start Telegram bot in background thread
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    print("🤖 Telegram bot started in background thread...")
    
    # Add small delay to ensure thread starts
    time.sleep(2)
    
    # Start Flask web server on main thread
    print(f"🚀 Starting Flask web server on port {port}...")
    print(f"🌐 Server will be accessible on all interfaces (0.0.0.0:{port})")
    
    # Run Flask with proper configuration for production
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        use_reloader=False,
        threaded=True
    )

if __name__ == "__main__":
    main()
