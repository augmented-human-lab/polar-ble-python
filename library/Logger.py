import queue
import asyncio
import threading

from PolarBLE import *
from WebSocketService import *

POLAR_DEVICE_NAME = "Polar Sense D6A7E729"

flag = asyncio.Event()
buffered_queue = queue.Queue()

register_ble_service(POLAR_DEVICE_NAME, buffered_queue, flag)

websocket_service = WebSocketService()
threading.Thread(target=websocket_service.run_server, daemon=True).start()

async def main():
    while True:
        heart_rate = buffered_queue.get()
        await websocket_service.set_heart_rate(heart_rate)

def run_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

try:
    async_thread = threading.Thread(target=run_async_loop)
    async_thread.start()
    async_thread.join()
except KeyboardInterrupt:
    stop_ble_service(flag)
