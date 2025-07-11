import websockets
import asyncio

class WebSocketClient:

    uri = "ws://localhost:8765"

    def __init__(self, data_queue):
        self.data_queue = data_queue

    def create_connection(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(self.client())
    
    async def client(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                while True:
                    heart_rate = await websocket.recv()
                    self.data_queue.put(heart_rate)
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            self.data_queue.put(None)
