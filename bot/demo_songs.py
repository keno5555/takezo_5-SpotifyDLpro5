"""
Demo Songs Module
Provides rotating demo song URLs for testing bot functionality.
"""

import random
import logging

logger = logging.getLogger(__name__)

class DemoSongs:
    """Manages demo song URLs for testing."""
    
    def __init__(self):
        """Initialize with popular demo songs."""
        self.demo_urls = [
            "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh",  # Never Gonna Give You Up - Rick Astley
            "https://open.spotify.com/track/4VqPOruhp5EdPBeR92t6lQ",  # Gangnam Style - PSY
            "https://open.spotify.com/track/11dFghVXANMlKmJXsNCbNl",  # Rather Be - Clean Bandit
            "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC",  # Never Gonna Give You Up - Rick Astley (alternative)
            "https://open.spotify.com/track/7qiZfU4dY1lWllzX7mPBI3",  # Shape of You - Ed Sheeran
            "https://open.spotify.com/track/1Je1IMUlBXcx1Fz0WE7oPT",  # Somebody That I Used to Know - Gotye
            "https://open.spotify.com/track/5ghIJDpPoe3CfHMGu71E6T",  # Closer - The Chainsmokers
            "https://open.spotify.com/track/3a1lNhkSLSkpJE4MSHpDu9",  # Counting Stars - OneRepublic
            "https://open.spotify.com/track/0tgVpDi06FyKpA1z0VMD4v",  # Perfect - Ed Sheeran
            "https://open.spotify.com/track/6habFhsOp2NvshLv26DqMb",  # Stressed Out - Twenty One Pilots
            "https://open.spotify.com/track/1lDWb6b6ieDQ2xT7ewTC3G",  # Despacito - Luis Fonsi
            "https://open.spotify.com/track/7BKLCZ1jbUBVqRi2FVlTVw",  # Uptown Funk - Mark Ronson ft. Bruno Mars
            "https://open.spotify.com/track/6RUKPb4LETWmmr3iAEQktW",  # Shake It Off - Taylor Swift
            "https://open.spotify.com/track/4VqPOruhp5EdPBeR92t6lQ",  # Gangnam Style - PSY
            "https://open.spotify.com/track/0wwPcA6wtMf6HUMpIRdeP7",  # All of Me - John Legend
            "https://open.spotify.com/track/2Fxmhks0bxGSBdJ92vM42m",  # bad guy - Billie Eilish
            "https://open.spotify.com/track/4Dvkj6JhhA12EX05fT7y2e",  # Thunder - Imagine Dragons
            "https://open.spotify.com/track/5tz69p7tJuGPeMGwNTxYuV",  # Someone Like You - Adele
            "https://open.spotify.com/track/4iJyoBOLtHqaGxP12qzhQI",  # Roar - Katy Perry
        ]
        
        # Shuffle the list initially
        random.shuffle(self.demo_urls)
        logger.info(f"Demo songs initialized with {len(self.demo_urls)} songs")
    
    def get_random_demo_url(self) -> str:
        """
        Get a random demo URL.
        
        Returns:
            Random demo song URL
        """
        demo_url = random.choice(self.demo_urls)
        logger.info(f"Providing demo URL: {demo_url}")
        return demo_url
    
    def get_demo_batch(self, count: int = 5) -> list:
        """
        Get a batch of random demo URLs.
        
        Args:
            count: Number of URLs to return
            
        Returns:
            List of demo URLs
        """
        return random.sample(self.demo_urls, min(count, len(self.demo_urls)))
    
    def refresh_demo_list(self):
        """Shuffle the demo list for variety."""
        random.shuffle(self.demo_urls)
        logger.info("Demo song list refreshed")
    
    def add_demo_song(self, url: str):
        """
        Add a new demo song URL.
        
        Args:
            url: Spotify URL to add
        """
        if url not in self.demo_urls:
            self.demo_urls.append(url)
            logger.info(f"Added new demo song: {url}")
        else:
            logger.info(f"Demo song already exists: {url}")
    
    def remove_demo_song(self, url: str):
        """
        Remove a demo song URL.
        
        Args:
            url: Spotify URL to remove
        """
        if url in self.demo_urls:
            self.demo_urls.remove(url)
            logger.info(f"Removed demo song: {url}")
        else:
            logger.warning(f"Demo song not found: {url}")
    
    def get_demo_count(self) -> int:
        """
        Get the total number of demo songs.
        
        Returns:
            Number of demo songs available
        """
        return len(self.demo_urls)
