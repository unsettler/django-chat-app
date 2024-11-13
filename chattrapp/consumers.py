import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, CustomUsercreated
from channels.db import database_sync_to_async
from django.core.mail import send_mail
from django.conf import settings



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chatting_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = self.scope['user'].id
        recipient_id = text_data_json['recipient_id']  # Extract recipient_id from the WebSocket message

        # Save message to database
        await self.save_message(sender_id, recipient_id, message)

        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope['user'].username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    @database_sync_to_async
    def save_message(self, sender_id, recipient_id, message):
        sender = CustomUsercreated.objects.get(id=sender_id)
        recipient = CustomUsercreated.objects.get(id=recipient_id)
        Message.objects.create(sender=sender, receiver=recipient, content=message)

        # Send an email notification to the recipient
        self.send_email_notification(recipient.email, sender.username, message)

    def send_email_notification(self, recipient_email, sender_username, message):
        subject = f"New Message from {sender_username}"
        email_message = f"You have received a new message from {sender_username}: \n\n{message}"
        send_mail(
            subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,  # Make sure DEFAULT_FROM_EMAIL is set in settings.py
            [recipient_email],
            fail_silently=False,
        )
