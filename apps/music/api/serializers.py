from rest_framework import serializers
from apps.music.models import ListeningSession
from apps.accounts.api.serializers import UserSerializer
from apps.music.utils import decrypt

class ArtistSerializer(serializers.Serializer):
    id = serializers.CharField()
    type = serializers.CharField()
    name = serializers.CharField()
    role = serializers.CharField()
    image = serializers.URLField()


class AlbumSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    subtitle = serializers.CharField(allow_blank=True)
    type = serializers.CharField()
    perma_url = serializers.URLField()
    image = serializers.URLField()
    language = serializers.CharField()
    explicit_content = serializers.CharField()

    release_date = serializers.CharField(
        source="more_info.release_date",
        required=False,
        allow_null=True,
        default=None
    )

    song_count = serializers.CharField(
        source="more_info.song_count",
        required=False,
        allow_null=True,
        default=None
    )
    artists = ArtistSerializer(
        source="more_info.artistMap.artists",
        many=True,
        required=False,
        allow_null=True,
        default=None
    )




class SongArtistSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()



class SongSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    subtitle = serializers.CharField(allow_blank=True, default="")
    type = serializers.CharField()
    perma_url = serializers.CharField()
    image = serializers.CharField()
    language = serializers.CharField(default="")
    year = serializers.CharField(default="")
    play_count = serializers.CharField(default="0")
    explicit_content = serializers.CharField(default="0")

    music = serializers.CharField(
        source="more_info.music",
        required=False,
        default=""
    )
    album_id = serializers.CharField(
        source="more_info.album_id",
        required=False,
        default=""
    )
    album = serializers.CharField(
        source="more_info.album",
        required=False,
        default=""
    )
    label = serializers.CharField(
        source="more_info.label",
        required=False,
        default=""
    )
    duration = serializers.CharField(
        source="more_info.duration",
        required=False,
        default="0"
    )

    playable_url = serializers.SerializerMethodField()

    def get_playable_url(self, obj):
        encrypted_url = obj.get("more_info", {}).get(
            "encrypted_media_url", ""
        )

        if not encrypted_url:
            return ""

        # TODO: decrypt encrypted_url here
        playable_url = self.decrypt_url(encrypted_url)

        return playable_url

    def decrypt_url(self, encrypted_url):
        return decrypt(encrypted_url)
    

class TrendingSerializer(serializers.Serializer):

    def to_representation(self, instance):
        item_type = instance.get("type")

        serializer_map = {
            "album": AlbumSerializer,
            "song": SongSerializer,
            "playlist": PlaylistSerializer,
            "radio_station": RadioSerializer,
        }

        serializer_class = serializer_map.get(item_type)

        if not serializer_class:
            return instance

        return serializer_class(instance).data


class ChartSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    type = serializers.CharField()
    image = serializers.CharField()

class PlaylistSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    subtitle = serializers.CharField(allow_blank=True, default="")
    type = serializers.CharField()
    image = serializers.CharField()

    song_count = serializers.CharField(
        source="more_info.song_count",
        required=False,
        default=""
    )

    follower_count = serializers.CharField(
        source="more_info.follower_count",
        required=False,
        default=""
    )
    last_updated = serializers.CharField(
        source="more_info.last_updated",
        required=False,
        default=""
    )

from rest_framework import serializers


class RadioSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    subtitle = serializers.CharField(allow_blank=True, default="")
    type = serializers.CharField()
    image = serializers.CharField()

    description = serializers.CharField(
        source="more_info.description",
        required=False,
        default=""
    )
    featured_station_type = serializers.CharField(
        source="more_info.featured_station_type",
        required=False,
        default=""
    )
    query = serializers.CharField(
        source="more_info.query",
        required=False,
        default=""
    )
    color = serializers.CharField(
        source="more_info.color",
        required=False,
        default=""
    )
    language = serializers.CharField(
        source="more_info.language",
        required=False,
        default=""
    )
    station_display_text = serializers.CharField(
        source="more_info.station_display_text",
        required=False,
        default=""
    )


class ListeningSessionSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    participants = UserSerializer(many=True)
    
    class Meta:
        model = ListeningSession
        fields = ['session_id', 'creator', 'participants', 'current_song_id', 'playback_position']
