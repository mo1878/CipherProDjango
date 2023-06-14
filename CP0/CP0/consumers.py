import asyncio
import json
import requests

from channels.consumer import AsyncWebsocketConsumer

class ExternalAPIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        pass

class ClientConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        pass
