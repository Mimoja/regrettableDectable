import asyncio
from MailProtocol import MailProtocol
import serial_asyncio
from ppApi import PpApi, ApiPpUle


async def main():
    port = "/dev/ttyUSB0"
    baudrate = 115200

    print(f"Connecting to {port} at {baudrate} baud...")
    loop = asyncio.get_running_loop()
    transport, protocol = await serial_asyncio.create_serial_connection(
        loop, lambda: MailProtocol(), port, baudrate
    )
    protocol.transport = transport

    asyncio.create_task(protocol.poll_timer())

    await asyncio.sleep(2)
    print("Sending 'API_FP_GET_FW_VERSION' request command...")

    protocol.send_command(
        program_id=0,
        task_id=1,
        primitive=0x4002,
        params=[],
    )
    print("Sending 'API_HAL_LED_REQ' request command...")

    protocol.send_command(
        program_id=0,
        task_id=1,
        primitive=0x5902,
        params=[0x02, 0x03, 0x01, 0x2C, 0x01, 0x00, 0x2C, 0x01, 0x02, 0x0A, 0x00],
    )

    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated.")
