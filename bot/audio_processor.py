"""
Audio Processing Module
Handles audio search and download functionality via yt-dlp.
"""

import os
import logging
import asyncio
import subprocess
import json
from typing import Dict, Optional
import tempfile
import hashlib
import re

logger = logging.getLogger(__name__)

class AudioProcessor:
    """Handles audio search and download operations via yt-dlp."""
    
    def __init__(self):
        """Initialize audio processor."""
        self.download_dir = tempfile.mkdtemp(prefix="music_bot_")
        
        # yt-dlp configuration
        self.ytdlp_path = "yt-dlp"
        
        logger.info(f"Audio processor initialized with download directory: {self.download_dir}")
        logger.info("Using yt-dlp for reliable YouTube audio downloads")
    
    async def download_track(self, track_info: Dict, quality: str) -> Optional[str]:
        """
        Download track audio file using yt-dlp.
        
        Args:
            track_info: Track information dictionary
            quality: Quality preference (128, 192, 320)
            
        Returns:
            Path to downloaded file or None if failed
        """
        search_query = f"{track_info['name']} {track_info['artist']}"
        logger.info(f"Starting download for: {search_query}")
        
        try:
            # Download directly from YouTube search query using yt-dlp
            file_path = await self._download_with_ytdlp_search(search_query, track_info, quality)
            if file_path and os.path.exists(file_path):
                logger.info(f"Successfully downloaded: {file_path}")
                return file_path
            else:
                logger.error(f"Download failed for: {search_query}")
                return None
                
        except Exception as e:
            logger.error(f"Download error for {search_query}: {e}")
            return None
    
    async def _download_with_ytdlp_search(self, search_query: str, track_info: Dict, quality: str) -> Optional[str]:
        """
        Download audio directly from YouTube search using yt-dlp.
        
        Args:
            search_query: Search query string
            track_info: Track information dictionary
            quality: Quality preference (128, 192, 320)
            
        Returns:
            Path to downloaded file or None
        """
        try:
            # Generate filename
            file_hash = hashlib.md5(search_query.encode()).hexdigest()[:8]
            safe_filename = re.sub(r'[^\w\s-]', '', search_query).strip()
            safe_filename = re.sub(r'[-\s]+', '-', safe_filename)
            output_template = os.path.join(self.download_dir, f"{safe_filename}-{file_hash}.%(ext)s")
            
            # Map quality to yt-dlp format
            audio_quality = self._map_quality_to_ytdlp(quality)
            
            # Build yt-dlp command with search directly
            cmd = [
                self.ytdlp_path,
                f"ytsearch1:{search_query}",  # Search for first result directly
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", audio_quality,
                "--output", output_template,
                "--no-warnings",
                "--no-playlist",
                "--prefer-free-formats"
            ]
            
            logger.info(f"Running yt-dlp with search: {search_query}")
            
            # Execute download
            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                # Find the downloaded file
                expected_path = output_template.replace("%(ext)s", "mp3")
                if os.path.exists(expected_path):
                    logger.info(f"Successfully downloaded: {expected_path}")
                    return expected_path
                else:
                    # Check for any mp3 file with our hash
                    for file in os.listdir(self.download_dir):
                        if file_hash in file and file.endswith('.mp3'):
                            file_path = os.path.join(self.download_dir, file)
                            logger.info(f"Found downloaded file: {file_path}")
                            return file_path
            else:
                stderr_text = stderr.decode() if stderr else 'Unknown error'
                logger.error(f"yt-dlp failed: {stderr_text}")
                return None
                
        except Exception as e:
            logger.error(f"yt-dlp download error: {e}")
            return None
    

    
    def _map_quality_to_ytdlp(self, quality: str) -> str:
        """
        Map quality setting to yt-dlp audio quality format.
        
        Args:
            quality: Requested quality (128, 192, 320)
            
        Returns:
            yt-dlp audio quality string
        """
        quality_map = {
            "128": "128K",
            "192": "192K", 
            "320": "320K"
        }
        return quality_map.get(quality, "192K")
    


    def cleanup_file(self, file_path: str):
        """
        Clean up downloaded file.
        
        Args:
            file_path: Path to file to be cleaned up
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup file {file_path}: {e}")
    
    def cleanup_all(self):
        """Clean up all downloaded files."""
        try:
            for file in os.listdir(self.download_dir):
                file_path = os.path.join(self.download_dir, file)
                self.cleanup_file(file_path)
            os.rmdir(self.download_dir)
            logger.info("All files cleaned up successfully")
        except Exception as e:
            logger.warning(f"Failed to cleanup all files: {e}")
    

