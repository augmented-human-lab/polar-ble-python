import asyncio
import websockets

class WebSocketService():
    def __init__(self):
        self.connected_clients = set()
        
    async def set_heart_rate(self, heart_rate):
        if self.connected_clients:
            await asyncio.gather(*[client.send(str(heart_rate)) for client in self.connected_clients])

    async def server(self, websocket, _):
        self.connected_clients.add(websocket)
        try:
            await websocket.recv()                
        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed")
        finally:
            self.connected_clients.remove(websocket)

    def run_server(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(websockets.serve(self.server, "localhost", 8765))
        asyncio.get_event_loop().run_forever()
