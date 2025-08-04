"""
Spotify API Client
Handles all Spotify API interactions for metadata extraction.
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import logging
import asyncio
from typing import Dict, List, Optional
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

logger = logging.getLogger(__name__)

class SpotifyClient:
    """Client for interacting with Spotify Web API."""
    
    def __init__(self):
        """Initialize Spotify client with credentials."""
        try:
            client_credentials_manager = SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET
            )
            self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            logger.info("Spotify client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Spotify client: {e}")
            self.sp = None
    
    async def get_track_info(self, track_id: str) -> Optional[Dict]:
        """
        Get track information from Spotify.
        
        Args:
            track_id: Spotify track ID
            
        Returns:
            Dictionary containing track information or None if failed
        """
        if not self.sp:
            logger.error("Spotify client not initialized")
            return None
            
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            track = await loop.run_in_executor(None, self.sp.track, track_id)
            
            # Extract relevant information
            track_info = {
                'id': track['id'],
                'name': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                'album': track['album']['name'],
                'duration': self._format_duration(track['duration_ms']),
                'duration_ms': track['duration_ms'],
                'popularity': track['popularity'],
                'preview_url': track.get('preview_url'),
                'external_urls': track['external_urls'],
                'release_date': track['album']['release_date'],
                'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
            }
            
            logger.info(f"Successfully retrieved track info for: {track_info['name']}")
            return track_info
            
        except Exception as e:
            logger.error(f"Error retrieving track info for {track_id}: {e}")
            return None
    
    async def get_playlist_info(self, playlist_id: str) -> Optional[Dict]:
        """
        Get playlist information from Spotify.
        
        Args:
            playlist_id: Spotify playlist ID
            
        Returns:
            Dictionary containing playlist information or None if failed
        """
        if not self.sp:
            logger.error("Spotify client not initialized")
            return None
            
        try:
            loop = asyncio.get_event_loop()
            
            # Get playlist basic info
            playlist = await loop.run_in_executor(None, self.sp.playlist, playlist_id)
            
            # Get all tracks (handle pagination)
            tracks = []
            results = playlist['tracks']
            
            while results:
                for item in results['items']:
                    if item['track'] and item['track']['type'] == 'track':
                        track = item['track']
                        track_info = {
                            'id': track['id'],
                            'name': track['name'],
                            'artist': ', '.join([artist['name'] for artist in track['artists']]),
                            'album': track['album']['name'],
                            'duration': self._format_duration(track['duration_ms']),
                            'duration_ms': track['duration_ms'],
                            'popularity': track['popularity']
                        }
                        tracks.append(track_info)
                
                # Get next page if available
                if results['next']:
                    results = await loop.run_in_executor(None, self.sp.next, results)
                else:
                    results = None
            
            playlist_info = {
                'id': playlist['id'],
                'name': playlist['name'],
                'description': playlist.get('description', ''),
                'owner': playlist['owner']['display_name'],
                'tracks': tracks,
                'total_tracks': len(tracks),
                'followers': playlist['followers']['total'],
                'image_url': playlist['images'][0]['url'] if playlist['images'] else None
            }
            
            logger.info(f"Successfully retrieved playlist info: {playlist_info['name']} ({len(tracks)} tracks)")
            return playlist_info
            
        except Exception as e:
            logger.error(f"Error retrieving playlist info for {playlist_id}: {e}")
            return None
    
    async def get_album_info(self, album_id: str) -> Optional[Dict]:
        """
        Get album information from Spotify.
        
        Args:
            album_id: Spotify album ID
            
        Returns:
            Dictionary containing album information or None if failed
        """
        if not self.sp:
            logger.error("Spotify client not initialized")
            return None
            
        try:
            loop = asyncio.get_event_loop()
            
            # Get album info
            album = await loop.run_in_executor(None, self.sp.album, album_id)
            
            # Extract track information
            tracks = []
            for track in album['tracks']['items']:
                track_info = {
                    'id': track['id'],
                    'name': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': album['name'],
                    'duration': self._format_duration(track['duration_ms']),
                    'duration_ms': track['duration_ms'],
                    'track_number': track['track_number']
                }
                tracks.append(track_info)
            
            album_info = {
                'id': album['id'],
                'name': album['name'],
                'artist': ', '.join([artist['name'] for artist in album['artists']]),
                'tracks': tracks,
                'total_tracks': album['total_tracks'],
                'release_date': album['release_date'],
                'genres': album.get('genres', []),
                'popularity': album['popularity'],
                'image_url': album['images'][0]['url'] if album['images'] else None
            }
            
            logger.info(f"Successfully retrieved album info: {album_info['name']} ({len(tracks)} tracks)")
            return album_info
            
        except Exception as e:
            logger.error(f"Error retrieving album info for {album_id}: {e}")
            return None
    
    async def search_track(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for tracks on Spotify.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of track dictionaries
        """
        if not self.sp:
            logger.error("Spotify client not initialized")
            return []
            
        try:
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None, 
                lambda: self.sp.search(q=query, type='track', limit=limit)
            )
            
            tracks = []
            for track in results['tracks']['items']:
                track_info = {
                    'id': track['id'],
                    'name': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'duration': self._format_duration(track['duration_ms']),
                    'duration_ms': track['duration_ms'],
                    'popularity': track['popularity'],
                    'external_urls': track['external_urls']
                }
                tracks.append(track_info)
            
            logger.info(f"Search returned {len(tracks)} results for query: {query}")
            return tracks
            
        except Exception as e:
            logger.error(f"Error searching tracks for query '{query}': {e}")
            return []
    
    def _format_duration(self, duration_ms: int) -> str:
        """
        Format duration from milliseconds to MM:SS format.
        
        Args:
            duration_ms: Duration in milliseconds
            
        Returns:
            Formatted duration string
        """
        seconds = duration_ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"
