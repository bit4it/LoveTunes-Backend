import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from authentication.firebase import *
from channels.exceptions import StopConsumer

class ChatConsumer(WebsocketConsumer):

    def _get_sender(self, auth_token):
          user = self.firebase_auth.get_user_from_auth_token(auth_token=auth_token)
          return user
    
    def connect(self):
        self.firebase_auth = FirebaseAuthentication()
        request_data = self.scope['url_route']['kwargs']

        try:
            auth_token = request_data['auth_token']
            self.session_id = request_data['session_id']
            # self.sender = self._get_sender(auth_token)

        except Exception as e:
            print("Exception ", e)
            raise StopConsumer({"error": str(e)})
               
        self.room_group_name = f"session_{self.session_id}"
        print(self.room_group_name)
        # Join room groupg
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "timestamp.message", "message": message}
        ) 


    # Receive message from room group
    def timestamp_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))