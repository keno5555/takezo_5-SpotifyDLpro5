# 🚀 Deploy Your MusicFlow Bot to Render (FREE)

Your bot is **ready for deployment** on Render's free web service! Follow these simple steps:

## ✅ Pre-configured Files
Your bot already includes:
- `main.py` - Flask web server that keeps bot alive 24/7
- `Procfile` - Deployment configuration (`web: python main.py`)
- `requirements-render.txt` - Python 3.13 compatible dependencies
- Port configuration - Uses Render's PORT environment variable

## 🎯 Deployment Steps

### 1. Connect to Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository containing this bot

### 2. Configure Service
**Service Name:** `musicflow-bot` (or any name you prefer)
**Environment:** `Python 3`
**Build Command:** `pip install -r requirements-render.txt`
**Start Command:** `python main.py`

### 3. Add Environment Variables
In Render dashboard, add these environment variables:
- `TELEGRAM_BOT_TOKEN` = Your bot token from @BotFather
- `SPOTIFY_CLIENT_ID` = Your Spotify app client ID  
- `SPOTIFY_CLIENT_SECRET` = Your Spotify app client secret

### 4. Deploy
1. Click "Create Web Service"
2. Wait for deployment (takes 2-3 minutes)
3. Your bot will be live 24/7!

## 🌟 Features After Deployment
- ✅ **24/7 Uptime** - Bot never sleeps
- ✅ **Keep-alive System** - Flask server prevents sleeping
- ✅ **Health Monitoring** - Built-in status endpoints
- ✅ **Auto-restart** - Automatically recovers from errors
- ✅ **Free Tier** - No cost for basic usage

## 📡 Monitoring Endpoints
Once deployed, your bot will have:
- `https://your-app.onrender.com/` - Bot status
- `https://your-app.onrender.com/health` - Health check
- `https://your-app.onrender.com/ping` - Simple ping test

## 🎵 Ready to Deploy!
Your bot is fully configured and ready for deployment. Just follow the steps above and your MusicFlow Bot will be running 24/7 on Render's free tier!