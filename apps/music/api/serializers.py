from rest_framework import serializers
from apps.music.models import ListeningSession
from apps.accounts.api.serializers import BasicUserSerializer

class ArtistSerializer(serializers.Serializer):
    id = serializers.CharField()
    type = serializers.CharField()
    name = serializers.CharField()
    role = serializers.CharField()
    image = serializers.URLField()


class AlbumSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    subtitle = serializers.CharField()
    header_desc = serializers.CharField()
    type = serializers.CharField()
    image = serializers.URLField()
    language = serializers.CharField()
    year = serializers.CharField()
    play_count = serializers.CharField()
    explicit_content = serializers.CharField()
    list_count = serializers.CharField()
    list_type = serializers.CharField()
    list = serializers.CharField()
    release_date = serializers.DateField()
    song_count = serializers.CharField()
    artists = serializers.DictField(source="artistMap",child=ArtistSerializer())
    modules = serializers.CharField(allow_null=True)


class ListeningSessionSerializer(serializers.ModelSerializer):
    creator = BasicUserSerializer()
    participants = BasicUserSerializer(many=True)
    
    class Meta:
        model = ListeningSession
        fields = ['session_id', 'creator', 'participants', 'current_song_id', 'playback_position']
