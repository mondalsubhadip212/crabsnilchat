# import json
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer as layer

# custom import
from .getuser import verify_user


class ChatConsumer(JsonWebsocketConsumer):

    def connect(self):
        try:
            username = verify_user(self.scope['path'])
            async_to_sync(self.channel_layer.group_add)(username,self.channel_name)
            self.accept()

        except:
            print('in except block consumer')
            self.close()

    def receive_json(self, content, **kwargs):
        async_to_sync(self.channel_layer.group_send)(
            content["receiver"],
            {
                "type": "chat.message",
                "sender": content["sender"],
                "sender_name": content["sender_name"],
                "receiver": content["receiver"],
                "message": content["message"],
                "time": content["time"]
            },
        )

    def chat_message(self,event):
        self.send_json(content={
            "sender": event["sender"],
            "sender_name": event['sender_name'],
            "receiver": event["receiver"],
            "message": event["message"],
            "time": event["time"]
        })

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)('general', self.channel_name)
        self.close()