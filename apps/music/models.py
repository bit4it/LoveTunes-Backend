from django.db import models
from django.contrib.auth import get_user_model
from tools.generate_unique_ids import UniqueIdGenerator

User = get_user_model()

class ListeningSession(models.Model):
    session_id = models.CharField(max_length=132, default=UniqueIdGenerator.generate_listening_session_id)
    creator = models.CharField(max_length=255)
    participants = models.CharField(max_length=255)
    current_song_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    playback_position = models.IntegerField(default=0) # second needs to be update when song is playing.

    class Meta:
        unique_together = ["creator", "is_active"]


    def __str__(self):
        return f"Session by {self.creator.username}"
    
    def end_session(self):
        self.is_active = True
        self.save()
    
