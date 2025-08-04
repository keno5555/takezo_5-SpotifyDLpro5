"""
Utility Functions
Contains helper functions for the Telegram music bot.
"""

import re
import logging
from typing import List, Tuple, Optional
from telegram import InlineKeyboardButton
from config import QUALITY_OPTIONS

logger = logging.getLogger(__name__)

def extract_spotify_id(url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract Spotify ID and content type from a Spotify URL.
    
    Args:
        url: Spotify URL
        
    Returns:
        Tuple of (spotify_id, content_type) or (None, None) if invalid
    """
    try:
        # Regular expression patterns for different Spotify URL formats
        patterns = {
            'track': r'spotify\.com/track/([a-zA-Z0-9]+)',
            'playlist': r'spotify\.com/playlist/([a-zA-Z0-9]+)',
            'album': r'spotify\.com/album/([a-zA-Z0-9]+)',
        }
        
        # Also handle spotify: URI format
        uri_patterns = {
            'track': r'spotify:track:([a-zA-Z0-9]+)',
            'playlist': r'spotify:playlist:([a-zA-Z0-9]+)',
            'album': r'spotify:album:([a-zA-Z0-9]+)',
        }
        
        # Try web URL patterns first
        for content_type, pattern in patterns.items():
            match = re.search(pattern, url)
            if match:
                spotify_id = match.group(1)
                logger.info(f"Extracted {content_type} ID: {spotify_id}")
                return spotify_id, content_type
        
        # Try URI patterns
        for content_type, pattern in uri_patterns.items():
            match = re.search(pattern, url)
            if match:
                spotify_id = match.group(1)
                logger.info(f"Extracted {content_type} ID from URI: {spotify_id}")
                return spotify_id, content_type
        
        logger.warning(f"No valid Spotify ID found in URL: {url}")
        return None, None
        
    except Exception as e:
        logger.error(f"Error extracting Spotify ID from URL {url}: {e}")
        return None, None

def create_quality_keyboard(track_id: str) -> List[List[InlineKeyboardButton]]:
    """
    Create inline keyboard for quality selection in a better grid layout.
    
    Args:
        track_id: Spotify track ID
        
    Returns:
        List of keyboard button rows
    """
    keyboard = []
    
    # Add quality option buttons in rows of 2
    quality_buttons = []
    for quality_text, quality_value in QUALITY_OPTIONS.items():
        button = InlineKeyboardButton(
            quality_text, 
            callback_data=f"quality_{quality_value}"
        )
        quality_buttons.append(button)
    
    # Arrange in rows of 2 buttons
    for i in range(0, len(quality_buttons), 2):
        if i + 1 < len(quality_buttons):
            keyboard.append([quality_buttons[i], quality_buttons[i + 1]])
        else:
            keyboard.append([quality_buttons[i]])
    
    # Add cancel button on its own row
    keyboard.append([InlineKeyboardButton("🚫 Cancel", callback_data="cancel_download")])
    
    return keyboard

def create_main_keyboard() -> List[List[InlineKeyboardButton]]:
    """
    Create main menu inline keyboard with better layout.
    
    Returns:
        List of keyboard button rows
    """
    keyboard = [
        [InlineKeyboardButton("🎪 Try Demo", callback_data="try_demo"), 
         InlineKeyboardButton("💡 Help", callback_data="help")],
        [InlineKeyboardButton("🚀 Share Bot", callback_data="share_bot")]
    ]
    
    return keyboard

def validate_spotify_url(url: str) -> bool:
    """
    Validate if a URL is a valid Spotify URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid Spotify URL, False otherwise
    """
    spotify_patterns = [
        r'https?://open\.spotify\.com/(track|playlist|album)/[a-zA-Z0-9]+',
        r'spotify:(track|playlist|album):[a-zA-Z0-9]+'
    ]
    
    for pattern in spotify_patterns:
        if re.match(pattern, url):
            return True
    
    return False

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    size_index = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and size_index < len(size_names) - 1:
        size /= 1024.0
        size_index += 1
    
    return f"{size:.1f} {size_names[size_index]}"

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters for file systems
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    
    # Limit length
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    
    return sanitized

def create_progress_bar(current: int, total: int, length: int = 10) -> str:
    """
    Create a progress bar string.
    
    Args:
        current: Current progress value
        total: Total value
        length: Length of progress bar
        
    Returns:
        Progress bar string
    """
    if total == 0:
        return "░" * length
    
    progress = min(current / total, 1.0)
    filled_length = int(length * progress)
    
    bar = "█" * filled_length + "░" * (length - filled_length)
    percentage = int(progress * 100)
    
    return f"{bar} {percentage}%"

def is_valid_quality(quality: str) -> bool:
    """
    Check if quality value is valid.
    
    Args:
        quality: Quality string to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_qualities = ["128", "192", "320"]
    return quality in valid_qualities

def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to specified length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def escape_markdown(text: str) -> str:
    """
    Escape markdown special characters.
    
    Args:
        text: Text to escape
        
    Returns:
        Escaped text
    """
    # Characters that need escaping in Telegram markdown
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    
    return text

def create_search_query(track_name: str, artist_name: str) -> str:
    """
    Create optimized search query for audio search.
    
    Args:
        track_name: Name of the track
        artist_name: Name of the artist
        
    Returns:
        Optimized search query
    """
    # Clean track name
    track_clean = re.sub(r'\([^)]*\)', '', track_name)  # Remove parentheses content
    track_clean = re.sub(r'\[[^\]]*\]', '', track_clean)  # Remove brackets content
    track_clean = re.sub(r'\s+', ' ', track_clean).strip()  # Clean whitespace
    
    # Clean artist name
    artist_clean = re.sub(r'\([^)]*\)', '', artist_name)
    artist_clean = re.sub(r'\[[^\]]*\]', '', artist_clean)
    artist_clean = re.sub(r'\s+', ' ', artist_clean).strip()
    
    # Create search query
    search_query = f"{track_clean} {artist_clean}"
    
    logger.info(f"Created search query: {search_query}")
    return search_query
