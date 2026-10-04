from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("home-page/", HomePageAPI.as_view()),
    path("top-searches/", TrendingSearch.as_view()),
    path("album/<str:album_id>/detail/", AlbumDetailAPI.as_view()),
    path("song/<str:song_id>/detail/", SongDetailAPI.as_view()),
    path("search", SearchSongAPI.as_view()),
    path("playlist/<str:playlist_id>/detail/", PlaylistDetailAPI.as_view()),
    path("session/start/", StartListeningSessionAPI.as_view()),
    path("session/<str:session_id>/join/", JoinListeningSessionAPI.as_view()),
    path("session/<str:session_id>/leave/", LeaveListeningSessionAPI.as_view()),
]
