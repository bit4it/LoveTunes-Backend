from django.contrib import admin
from apps.music.models import *

@admin.register(ListeningSession)
class ListeningSessionAdmin(admin.ModelAdmin):
    list_display = ["session_id", "current_song_id", "is_active"]
    filter_horizontal = ["participants"]
