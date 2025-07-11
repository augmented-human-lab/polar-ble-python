import asyncio
import threading

from bleak import BleakScanner
from bleak import BleakClient

from PolarPpgHelper import PolarDataHandler

DISCOVERY_DURATION = 10

PMD_CONTROL_UUID = "FB005C81-02E7-F387-1CAD-8ACD2D8DF0C8"
PMD_DATA_UUID = "FB005C82-02E7-F387-1CAD-8ACD2D8DF0C8"
HR_DATA_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

PPG_STREAM_SETTING = bytearray([0x02, 0x01, 0x00, 0x01, 0x37, 0x00, 0x01, 0x01, 0x16, 0x00, 0x04, 0x01, 0x04])
PPG_END_STREAM = bytearray([0x03, 0x01])

async def get_polar_address(polar_device_name):
    print("Searching for device...")

    async with BleakScanner() as scanner:
        for _ in range(DISCOVERY_DURATION):
            await asyncio.sleep(1.0)
            for device in scanner.discovered_devices:
                if device.name and device.name == polar_device_name:
                    return device.address
                
async def attempt_polar_connection(address):
    if address is None:
        print("Issue finding device")
        return None, False
    
    print("Device address: ", address)

    client = BleakClient(address)
    connection_status = await client.connect()
    
    return client, connection_status

async def write_control_data(client, pmd_setting, notification_handler):
    await client.start_notify(PMD_CONTROL_UUID, notification_handler)
    await client.write_gatt_char(PMD_CONTROL_UUID, pmd_setting, response=True)
    await client.stop_notify(PMD_CONTROL_UUID)

async def start_data_stream(client, uuid, notification_handler):
    await client.start_notify(uuid, notification_handler)

async def start_ble_service(polar_device_name, data_queue, flag):
    polar_mac_address = await get_polar_address(polar_device_name)
    polar_client, status = await attempt_polar_connection(polar_mac_address)
    if not status:
        print("Issue connecting to device")
        return
    
    polar_data_handler = PolarDataHandler(data_queue)

    await write_control_data(polar_client, PPG_STREAM_SETTING, polar_data_handler.control_point_handler)
    await start_data_stream(polar_client, PMD_DATA_UUID, polar_data_handler.ppg_data_handler)
    await start_data_stream(polar_client, HR_DATA_UUID, polar_data_handler.hr_data_handler)

    await flag.wait()

    await write_control_data(polar_client, PPG_END_STREAM, polar_data_handler.control_point_handler)
    await polar_client.stop_notify(PMD_DATA_UUID)
    await polar_client.stop_notify(HR_DATA_UUID)
    await polar_client.disconnect()

def run_async_function(polar_device_name, data_queue, flag):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_ble_service(polar_device_name, data_queue, flag))
    
def register_ble_service(polar_device_name, data_queue, flag):
    threading.Thread(target=run_async_function, args=(polar_device_name, data_queue, flag)).start()

def stop_ble_service(flag):
    flag.set()
