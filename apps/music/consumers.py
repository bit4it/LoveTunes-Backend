
import json
import time
import uuid
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from authentication.jwt import CustomJwtAuthentication


class ListeningRoomConsumer(AsyncJsonWebsocketConsumer):

    async def handle_user_auth(self):
        try:
            auth = CustomJwtAuthentication()

            self.user = await sync_to_async(
                auth.authentication_ws_request,
                thread_sensitive=True,
            )(self.scope["headers"])

        except Exception as exc:
            print("WebSocket authentication failed:", exc)
            await self.close(code=4401)
            raise Exception("Authentication failed...")

        # import ipdb; ipdb.set_trace()

    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.room_group_name = f"session_{self.session_id}"
        
        await self.handle_user_auth()

        if not self.user or not self.user.is_authenticated:
            await self.close(code=4401)
            return

        # TODO: Check that this user can join this listening room.

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "room.member_joined",
                "payload": {
                    "user_id": str(self.user.pk),
                },
            },
        )

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )

            if getattr(self, "user", None) and self.user.is_authenticated:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "room.member_left",
                        "payload": {
                            "user_id": str(self.user.pk),
                        },
                    },
                )

    async def receive_json(self, content, **kwargs):
        event_type = content.get("type")
        payload = content.get("payload", {})

        if not isinstance(payload, dict):
            await self.send_json({
                "type": "error",
                "payload": {"message": "Payload must be an object"},
            })
            return

        handlers = {
            "chat.message": self.handle_chat_message,
            "chat.emoji": self.handle_emoji,
            "player.play": self.handle_player_play,
            "player.pause": self.handle_player_pause,
            "player.seek": self.handle_player_seek,
            "player.track_changed": self.handle_track_changed,
            "player.sync": self.handle_player_sync,
        }

        handler = handlers.get(event_type)

        if not handler:
            await self.send_json({
                "type": "error",
                "payload": {"message": "Unsupported event type"},
            })
            return

        await handler(payload)

    async def broadcast(self, event_type, payload):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "room.event",
                "event_type": event_type,
                "payload": payload,
            },
        )

    async def room_event(self, event):
        # Called for events broadcast to the room group.
        await self.send_json({
            "type": event["event_type"],
            "payload": event["payload"],
        })

    async def handle_chat_message(self, payload):
        text = payload.get("text")

        if not isinstance(text, str) or not text.strip():
            return

        text = text.strip()

        if len(text) > 2000:
            return

        await self.broadcast("chat.message", {
            "id": str(uuid.uuid4()),
            "user_id": str(self.user.pk),
            "text": text,
            "timestamp": time.time(),
        })

    async def handle_emoji(self, payload):
        emoji = payload.get("emoji")

        if not isinstance(emoji, str) or len(emoji) > 16:
            return

        await self.broadcast("chat.emoji", {
            "user_id": str(self.user.pk),
            "emoji": emoji,
            "message_id": payload.get("message_id"),
            "timestamp": time.time(),
        })

    async def handle_player_play(self, payload):
        await self.broadcast("player.play", {
            "user_id": str(self.user.pk),
            "position": payload.get("position", 0),
            "timestamp": time.time(),
        })

    async def handle_player_pause(self, payload):
        await self.broadcast("player.pause", {
            "user_id": str(self.user.pk),
            "position": payload.get("position", 0),
            "timestamp": time.time(),
        })

    async def handle_player_seek(self, payload):
        position = payload.get("position")

        if (
            isinstance(position, bool)
            or not isinstance(position, (int, float))
            or position < 0
        ):
            return

        await self.broadcast("player.seek", {
            "user_id": str(self.user.pk),
            "position": position,
            "timestamp": time.time(),
        })

    async def handle_track_changed(self, payload):
        # Validate the track ID against your backend's music data.
        track_id = payload.get("track_id")

        if not isinstance(track_id, str) or not track_id:
            return

        await self.broadcast("player.track_changed", {
            "user_id": str(self.user.pk),
            "track_id": track_id,
            "position": 0,
            "timestamp": time.time(),
        })

    async def handle_player_sync(self, payload):
        # Clients can request the latest state from your
        # room-state service here.
        await self.send_json({
            "type": "player.sync",
            "payload": {
                "message": "Connect this handler to your room-state service."
            },
        })

    async def room_member_joined(self, event):
        await self.send_json({
            "type": "room.member_joined",
            "payload": event["payload"],
        })

    async def room_member_left(self, event):
        await self.send_json({
            "type": "room.member_left",
            "payload": event["payload"],
        })
