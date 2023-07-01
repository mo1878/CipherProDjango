import asyncio
import json
import certifi
import ssl
from channels.generic.websocket import AsyncWebsocketConsumer
import websockets
from web3 import Web3
import logging

logger = logging.getLogger(__name__)

INFURA_WEBSOCKET = 'wss://mainnet.infura.io/ws/v3/9a5c13770c2d4e669f17b587a0baf952'
INFURA_HTTP = 'https://mainnet.infura.io/v3/9a5c13770c2d4e669f17b587a0baf952'

web3 = Web3(Web3.HTTPProvider(INFURA_HTTP))
print(f'connected via HTTP: {web3.is_connected()}')

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

ADDRESSES = [
    '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D', 
    '0x1111111254EEB25477B68fb85Ed929f73A960582',
    '0x03f7724180AA6b939894B5Ca4314783B0b36b329',
    '0x1c87257F5e8609940Bc751a07BB085Bb7f8cDBE6',
]

CHECKSUM_ADDRESSES = [web3.to_checksum_address(address) for address in ADDRESSES]

UNISWAPV2_ABI = json.load(open('../uniswapv2_abi.json', 'r'))


class InfuraWebSocketConsumer(AsyncWebsocketConsumer):
    MAX_RECONNECT_ATTEMPTS = 5

    async def connect(self, *args, **kwargs):
        await self.accept()

        self.websocket = None
        self.connect_attempts = 0

        while self.connect_attempts < self.MAX_RECONNECT_ATTEMPTS:
            try:
                self.websocket = await websockets.connect(INFURA_WEBSOCKET, ssl=ssl_context, ping_interval=None)
                self.ping_task = asyncio.create_task(self.keep_alive())

                # Subscribe to 'newPendingTransactions'
                subscribe_payload = {
                    'jsonrpc': '2.0',
                    'id': 2,
                    'method': 'eth_subscribe',
                    'params': ['newPendingTransactions'],
                }

                await self.websocket.send(json.dumps(subscribe_payload))
                await self.handle_messages()

                # if we reach this point, the connection was successful
                break
            except Exception as e:
                self.connect_attempts += 1
                logger.error(f"Attempt {self.connect_attempts} to connect to websocket failed: {e}")

        if self.connect_attempts >= self.MAX_RECONNECT_ATTEMPTS:
            logger.error("Unable to establish websocket connection after %s attempts", self.MAX_RECONNECT_ATTEMPTS)
            raise Exception(f"Unable to establish websocket connection after {self.MAX_RECONNECT_ATTEMPTS} attempts")

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Handle received data

    async def keep_alive(self):
        while True:
            if self.websocket and self.websocket.open:
                try:
                    await self.websocket.ping()
                except Exception as e:
                    logger.error("Failed to send ping: %s", e)
                    break
            await asyncio.sleep(10)  # Sleep for 10 seconds

    async def handle_messages(self):
        while True:
            try:
                # Returns pending transaction JSON-RPC response
                pending_transactions = await asyncio.wait_for(self.websocket.recv(), timeout=15)

                # Load JSON-RPC response into a dictionary
                transaction_dict = json.loads(pending_transactions)

                # Get transaction data from the transaction dictionary
                transaction_data = web3.eth.get_transaction(transaction_dict['params']['result'])

                # Check if the transaction is posted to one of the DeFI addresses we are interested in
                if transaction_data['to'] in CHECKSUM_ADDRESSES:

                    # Converts the transaction data hash to hex
                    transaction_data_hash = web3.to_hex(transaction_data['hash'])

                    # Get the transaction data from the transaction hex
                    transaction_hash_dict = web3.eth.get_transaction(transaction_data_hash)

                    # Print the input data to the DeFI router
                    print(f"Contract Address: {transaction_data['to']}, transaction_data_hash: {transaction_hash_dict['input']}")

                    # Send the input data to the react front end
                    await self.send(text_data=json.dumps({
                        'type': 'processed_data',
                        'data': transaction_hash_dict['input']
                    }))

            except Exception as e:
                logger.error("An error occurred: %s", e)
                continue

    async def disconnect(self, close_code):
        if self.websocket and self.websocket.open:
            await self.websocket.close()
        self.ping_task.cancel()  # Cancel the keep-alive task
        