from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import *
import json


class AsyncChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        await self.channel_layer.group_send(
            self.room_name, 
            {
                'type': 'chat.data',
                'text': text_data
            }
        )

    async def chat_data(self, event):
        text_data = json.loads(event['text'])

        if 'user_id' in text_data and 'message' in text_data:
            response = await self.get_user(text_data)
            print(response)
            if response['status'] == 'ok':
                await self.send(text_data=json.dumps(response))
            else: 
                pass

    @database_sync_to_async
    def get_user(self, data):
        if len(str(data['message'])) > 1500 or len(str(data['message'])) == 0:
            pass
        else:
            user = CustomUser.objects.filter(user_id=data['user_id'])
            if user.count() > 0:
                return {"data": {"username": user[0].username, "avatar": user[0].avatar.url, "message": data['message']}, "status": "ok"}
            else:
                return {"data": {"username": "Ananimus", "avatar": "/media/Users%20avatars/default/default_avatar.png", "message": data['message']},"status": "ok"}