import json

import jwt
from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime
import os

from jwt import ExpiredSignatureError, InvalidTokenError

import Sahand.settings
from Sahand import settings
from chat.models import Message
from security.models import User
from task_manager.models import TaskProject

CHAT_HISTORY_FILE = 'chat_history.json'


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Decode the token to get user information
        token = self.scope['query_string'].decode('utf-8').split('=')[-1]
        try:
            decoded_token = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )
            self.user_id = decoded_token.get("user_id")
            self.user = User.objects.get(id=self.user_id)  # Assign the User object to self.user
            self.username = self.user.username
        except ExpiredSignatureError:
            print("Token has expired")
            self.close()
        except InvalidTokenError:
            print("Invalid token")
            self.close()
        except User.DoesNotExist:
            print("User not found")
            self.close()

        # Add the WebSocket to the group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        print(f"User {self.username} connected!")
        self.accept()
        self.send_previous_messages()

    def receive(self, text_data):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        tsk_id = self.room_group_name[-1]
        text_data_json = json.loads(text_data)
        message = text_data_json['text']

        # Get the current timestamp
        timestamp = datetime.now()

        # Save the message along with the user's info and timestamp
        self.save_message(self.username, message, timestamp, task_id=tsk_id)
        print(self.username, message, timestamp, tsk_id)

        # User details
        user_detail = {
            "id": self.user_id,
            "photo": self.user.photo.id if self.user.photo else None,
            "fullname": self.user.full_name
        }

        # Broadcast the message to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'client': self.username,  # Username
                'user_detail': user_detail,  # Include user details
                'message': message,
                'timestamp': timestamp
            }
        )

    def chat_message(self, event):
        # Receive message from the group and send it to the WebSocket
        self.send(text_data=json.dumps({
            'type': 'chat',
            'client': event['client'],  # Username
            'user_detail': event['user_detail'],  # Include user details here
            'message': event['message'],
            'timestamp': event['timestamp'].isoformat()  # Convert datetime to ISO string
        }))

    def save_message(self, client, message, timestamp, task_id, message_status=1, file=None, status=1, voice=None):
        user_id = None
        token = self.scope['query_string'].decode('utf-8').split('=')[-1]
        try:
            # Decode the token
            decoded_token = jwt.decode(
                token,
                settings.SECRET_KEY,  # Use your Django secret key for decoding
                algorithms=["HS256"]  # Match the algorithm used to sign the token
            )
            user_id = decoded_token.get("user_id")  # Extract the user ID
        except ExpiredSignatureError:
            print("Token has expired")
            self.close()
        except InvalidTokenError:
            print("Invalid token")
            self.close()
        """
        Save the message to the Message model.

        Args:
            client (str): Client information.
            message (str): The message text.
            timestamp (datetime): The timestamp of the message.
            user (User): The user sending/receiving the message.
            task_id (id): The associated task project.
            message_status (int): Status of the message (default is 'Send').
            file (FileManager): Optional file attachment.
            status (int): Status of the message (default is 'Active').
        """
        try:
            # Save the message instance to the database
            tp = TaskProject.objects.get(id=task_id)
            Message.objects.create(
                text=message,
                send_time=timestamp,
                user_id=user_id,
                task_project=tp,
                message_status=message_status,
                file_id=file,
                status=status,
                voice_id=voice
            )
            print(f"Message from saved {client} successfully.")
        except Exception as e:
            print(f"Error saving message: {e}")

    def send_previous_messages(self):
        user_id = None
        token = self.scope['query_string'].decode('utf-8').split('=')[-1]
        try:
            # Decode the token
            decoded_token = jwt.decode(
                token,
                settings.SECRET_KEY,  # Use your Django secret key for decoding
                algorithms=["HS256"]  # Match the algorithm used to sign the token
            )
            user_id = decoded_token.get("user_id")  # Extract the user ID
        except ExpiredSignatureError:
            print("Token has expired")
            self.close()
        except InvalidTokenError:
            print("Invalid token")
            self.close()

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        tsk_id = self.room_group_name[-1]
        """Send previous messages when a user connects"""
        try:
            print(f"is {tsk_id}")
            # Query the Message model to get all previous messages
            messages = Message.objects.filter(task_project_id=tsk_id).order_by(
                'send_time')  # Retrieve all messages, ordered by the timestamp

            # Send each message to the client
            for msg in messages:
                self.send(text_data=json.dumps({
                    'type': 'chat',
                    'client': msg.user.username if msg.user else 'Unknown',
                    # Assuming the `client` is linked to the user,
                    'user_detail': {
                        "id": msg.user_id,
                        "photo": msg.user.photo.id if msg.user.photo else None,
                        "fullname": msg.user.full_name,
                    },
                    'message': msg.text,
                    'timestamp': msg.send_time.isoformat()
                    # Convert timestamp to ISO format for consistency
                }))
        except Exception as e:
            print(f"Error fetching messages: {e}")
