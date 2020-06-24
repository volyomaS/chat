import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Connecting to websocket and
        joining to channel group
        """
        self.user_id = self.scope["session"]["_auth_user_id"]
        self.group_name = f'{self.user_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Leaving channel group
        """
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receiving message from websocket and
        sending it to channel group
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'receive_group_message',
                'message': message
            }
        )

    async def receive_group_message(self, event):
        """
        Receiving message from channel group and
        sending it to websocket
        """
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
