import asyncio
import json
import requests

from channels.consumer import AsyncWebsocketConsumer

class ExternalAPIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        pass

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass 

    async def send_to_client(self, data):
        pass
