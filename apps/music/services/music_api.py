import os
import requests

class MusicAPIManager:
    BASE_URL = "https://www.jiosaavn.com"
    API_STR = "api.php?_format=json&_marker=0&api_version=4&ctx=web6dot0"
      
    def __init__(self) -> None:
        self.api_url =  f"{MusicAPIManager.BASE_URL}/{MusicAPIManager.API_STR}"
        self.endpoints  = {
          'homeData': '__call=webapi.getLaunchData',
          'topSearches': '__call=content.getTopSearches',
          'fromToken': '__call=webapi.get',
          'featuredRadio': '__call=webradio.createFeaturedStation',
          'artistRadio': '__call=webradio.createArtistStation',
          'entityRadio': '__call=webradio.createEntityStation',
          'radioSongs': '__call=webradio.getSong',
          'songDetails': '__call=song.getDetails',
          'playlistDetails': '__call=playlist.getDetails',
          'albumDetails': '__call=content.getAlbumDetails',
          'getResults': '__call=search.getResults',
          'albumResults': '__call=search.getAlbumResults',
          'artistResults': '__call=search.getArtistResults',
          'playlistResults': '__call=search.getPlaylistResults',
          'getReco': '__call=reco.getreco',
          'getAlbumReco': '__call=reco.getAlbumReco',
          'artistOtherTopSongs':
          '__call=search.artistOtherTopSongs',
        }

    def get_api_url(self):
      url = f"{self.api_url}"
      return url
    
    def get_response(self, params):
        api_url = self.get_api_url()
        url = f"{api_url}&{params}"
       
        response = requests.get(url=url)
        data = response.json()
        return data
      

    def get_home_page_data(self):
        data = self.get_response(self.endpoints["homeData"])
        return data
    
    def get_top_searches(self):
        data = self.get_response(self.endpoints["topSearches"])
        return data
    
    def get_album_details(self, album_id: str):
        params = f"{self.endpoints['albumDetails']}&cc=in&albumid={album_id}"
        data = self.get_response(params=params)
        return data
    
    def get_playlist_details(self, playlist_id: str):
        params = f"{self.endpoints['playlistDetails']}&cc=in&listid={playlist_id}"
        data = self.get_response(params=params)
        return data
        
    def get_song_details(self, song_id: str):
        params = f"{self.endpoints['songDetails']}&pids={song_id}"
        data = self.get_response(params=params)
        return data
    
    # def search_music(self, query: str):
    #     params = f"{self.endpoints['songDetails']}&pids={song_id}"
    #     data = self.get_response(params=params)
    #     return data
        