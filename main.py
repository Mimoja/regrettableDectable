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

    await asyncio.sleep(5)
    print("Sending 'CVM_PP_AUDIO_START_TONE_REQ' request command...")
    protocol.send_command(
            program_id=0,
            task_id=1,
            primitive=0x510B,
            params=[0x01, 0xFF, 0xFF, 0x00, 0x00],
        )

    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated.")
