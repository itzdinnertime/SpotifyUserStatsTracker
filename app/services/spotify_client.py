from datetime import datetime

class SpotifyClient:
    
    def __init__(self, sp):
        self.sp = sp
        
    def get_current_user(self) -> dict:
        
        user = self.sp.current_user()
        return {
            'id': user['id'],
            'display_name': user.get('display_name')
        }
        
    def get_top_tracks(self, time_range, limit):
        
        results = self.sp.current_user_top_tracks(limit=limit, time_range=time_range)
        tracks = []
        
        for item in results['items']:
            track = {
                'id': item['id'],
                'name': item['name'],
                'artist': item['artists'][0]['name'],
                'image_url': item['album']['images'][0]['url'] if item['album']['images'] else None
            }
            tracks.append(track)
            
        return tracks
            
    def get_top_artists(self, time_range: str, limit: int = 50) -> list:
        
        results = self.sp.current_user_top_artists(limit=limit, time_range=time_range)
        artists = []
        
        for item in results['items']:
            artist = {
                    'id': item['id'],
                    'name': item['name'],
                    'genres': ', '.join(item.get('genres', [])),
                    'image_url': item['images'][0]['url'] if item.get('images') else None
                }
            artists.append(artist)
            
        return artists
    
    def get_recently_played(self, limit):
        
        results = self.sp.current_user_recently_played(limit=limit)
        tracks = []
        
        for item in results['items']:
            track = {
                'id': item['track']['id'],
                'name': item['track']['name'],
                'artist': item['track']['artists'][0]['name'],
                'played_at': datetime.fromisoformat(item['played_at'].replace('Z', '+00:00')),
                'image_url': item['track']['album']['images'][0]['url'] if item['track']['album']['images'] else None
            }
            tracks.append(track)
        
        return tracks