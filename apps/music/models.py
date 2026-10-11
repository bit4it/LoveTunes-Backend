from django.db import models
from django.contrib.auth import get_user_model
from tools.generate_unique_ids import UniqueIdGenerator
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone



User = get_user_model()


class ListeningSession(models.Model):
    session_id = models.CharField(
        max_length=132,
        unique=True,
        default=UniqueIdGenerator.generate_listening_session_id,
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_listening_sessions",
    )

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ListeningParticipant",
        related_name="listening_sessions",
        blank=True,
    )

    current_song_id = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    is_active = models.BooleanField(default=True)
    is_playing = models.BooleanField(default=False)

    # Playback position in seconds
    playback_position = models.PositiveIntegerField(default=0)

    # Last time playback position/state was synchronized
    playback_updated_at = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["creator"],
                condition=Q(is_active=True),
                name="unique_active_session_per_creator",
            ),
        ]

    def __str__(self):
        return f"Session {self.session_id} by {self.creator}"

    def end_session(self):
        if self.is_active:
            self.is_active = False
            self.is_playing = False
            self.ended_at = timezone.now()
            self.save(
                update_fields=[
                    "is_active",
                    "is_playing",
                    "ended_at",
                    "updated_at",
                ]
            )

    def get_current_position(self):
        """Calculate the current position without updating the database."""
        if not self.is_playing:
            return self.playback_position

        elapsed = (
            timezone.now() - self.playback_updated_at
        ).total_seconds()

        return self.playback_position + max(0, int(elapsed))


class ListeningParticipant(models.Model):
    session = models.ForeignKey(
        ListeningSession,
        on_delete=models.CASCADE,
        related_name="participant_records",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listening_participations",
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session", "user"],
                name="unique_user_per_listening_session",
            ),
        ]

    def __str__(self):
        return f"{self.user} in {self.session.session_id}"
