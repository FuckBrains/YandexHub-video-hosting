from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
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
            response = await self.check(text_data)
            if response['status'] == 'ok':
                await self.send(text_data=json.dumps(response))
            else: 
                pass
    
    @sync_to_async
    def check(self, data):
        message = data['message']
        if len(message) > 500 or len(message.replace(" ", "")) == 0:
            return {"status": "err"}
        else:
            return {"data": {"username": data["username"], "avatar": data["avatar"], "user_id": data["user_id"], "message": data["message"]}, "status": "ok"}