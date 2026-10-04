from rest_framework.response import Response
from rest_framework.views import APIView
from apps.music.services.music_api import MusicAPIManager
from rest_framework import serializers
from tools.exceptions import CustomAPIException
from apps.music.models import ListeningSession
from rest_framework import status
from apps.music.services.listening_session import ListeningSessionManager
from apps.music.api.serializers import ListeningSessionSerializer, AlbumSerializer, RadioSerializer, ChartSerializer, PlaylistSerializer, TrendingSerializer
from tools.http import get_request_data

class HomePageAPI(APIView):
    def get(self, request):
        manager = MusicAPIManager()
        data = manager.get_home_page_data()
        trending_albums = data.get("new_trending", [])


        trending = data.get("new_trending", [])
        trending_serializer = TrendingSerializer(trending, many=True)

        new_albums = data.get("new_albums", [])
        album_serilizer = AlbumSerializer(new_albums, many=True)

        top_playlist = data.get("top_playlists", [])
        top_playlist_serializer = PlaylistSerializer(top_playlist, many=True)

        charts = data.get("charts", [])
        charts_serializer = ChartSerializer(charts, many=True)

        radio = data.get("radio", [])
        radio_serilizer = RadioSerializer(radio, many=True)

        response = {
            "trending_albums": trending_serializer.data,
            "new_albums": album_serilizer.data,
            "top_playlists": top_playlist_serializer.data,
            "charts": charts_serializer.data,
            "raido": radio_serilizer.data
        }
        return Response(data=response)
        # return Response(data=trending_albums)

    
class TrendingSearch(APIView):
    def get(self, request):
        manager = MusicAPIManager()
        data = manager.get_home_page_data()
        return Response(data=data)
    

class AlbumDetailAPI(APIView):

    class InputSerializer(serializers.Serializer):
        album_id = serializers.CharField(required=True)

    def get(self, request, **kwargs):
        serializer = self.InputSerializer(data=self.kwargs)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=f"MissingFeild Error {e}")
        
        album_id = serializer.data["album_id"]
        manager = MusicAPIManager()
        data = manager.get_album_details(album_id=album_id)
        return Response(data=data)

class PlaylistDetailAPI(APIView):
    class InputSerializer(serializers.Serializer):
        playlist_id = serializers.CharField(required=True)

    def get(self, request, **kwargs):
        serializer = self.InputSerializer(data=self.kwargs)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=f"MissingFeild Error {e}")
        
        playlist_id = serializer.data["playlist_id"]
        manager = MusicAPIManager()
        data = manager.get_playlist_details(playlist_id=playlist_id)
        return Response(data=data)
    
class SongDetailAPI(APIView):

    class InputSerializer(serializers.Serializer):
        song_id = serializers.CharField(required=True)

    def get(self, request, **kwargs):
        serializer = self.InputSerializer(data=self.kwargs)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=f"MissingFeild Error {e}")
        
        song_id = serializer.data["song_id"]
        manager = MusicAPIManager()
        data = manager.get_song_details(song_id=song_id)
        return Response(data=data)

class SearchAllAPI(APIView):
    def get(self, request):
        manager = MusicAPIManager()
        data = manager.get_home_page_data()
        return Response(data=data)

class StartListeningSessionAPI(APIView):
    def post(self, request):
        user = request.user
        manager = ListeningSessionManager()
        stream = manager.create_session(user)
        serializer = ListeningSessionSerializer(stream)
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

class JoinListeningSessionAPI(APIView):

    class InputSerializer(serializers.Serializer):
        session_id = serializers.CharField(required=True)

    def post(self, request, *args, **kwargs):
        user = request.user
        request_data = get_request_data(request=request, **kwargs)
        serializer = self.InputSerializer(data=request_data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        session_id = serializer.data["session_id"]

        manager = ListeningSessionManager()
        stream = manager.join_session(session_id=session_id, user=user)

        serializer = ListeningSessionSerializer(stream)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class LeaveListeningSessionAPI(APIView):
    class InputSerializer(serializers.Serializer):
        session_id = serializers.CharField(required=True)

  
    def delete(self, request, *args, **kwargs):
        user = request.user
        request_data = get_request_data(request=request, **kwargs)
        serializer = self.InputSerializer(data=request_data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        session_id = serializer.data["session_id"]
        
        manager = ListeningSessionManager()
        stream = manager.leave_session(session_id=session_id, user=user)

        serializer = ListeningSessionSerializer(stream)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

