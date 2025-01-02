import asyncio
from MailProtocol import MailProtocol
import serial_asyncio
from Api.HAL import ApiHalLedReqType, ApiHalLedCmdType, ApiHalLedCmdIdType
from Api.FPGENERAL import ApiFpGetFwVersionReq
from Api.IMAGE import ApiImageActivateReq, ApiImageID
from Api.PROD import ApiProdTestReq
from Api.PPMM import (
    ApiPpMmRegistrationSearchReq,
    ApiMmSearchModeType,
    ApiPpMmRegistrationAutoReq,
)

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
    protocol.send(
        ApiFpGetFwVersionReq(),
    )

    print("Sending 'API_HAL_LED_REQ' request command...")
    # protocol.send_command(
    #     program_id=0,
    #     task_id=1,
    #     primitive=0x5902,
    #     params=[0x02, 0x03, 0x01, 0x2C, 0x01, 0x00, 0x2C, 0x01, 0x02, 0x0A, 0x00],
    # )

    protocol.send(
        ApiHalLedReqType(
            led=2,
            commands=[
                ApiHalLedCmdType(
                    command=ApiHalLedCmdIdType.ALI_LED_ON,
                    duration=300,
                ),
                ApiHalLedCmdType(
                    command=ApiHalLedCmdIdType.ALI_LED_OFF,
                    duration=300,
                ),
                ApiHalLedCmdType(
                    command=ApiHalLedCmdIdType.ALI_REPEAT_SEQUENCE,
                    duration=10,
                ),
            ],
        )
    )
    await asyncio.sleep(5)
    print("Sending 'API_IMAGE_ACTIVATE_REQ' request command...")

    protocol.send(ApiImageActivateReq(0x01, False))

    await asyncio.sleep(15)
    protocol.send(ApiProdTestReq(opcode=0x02, data=bytes([0x01, 0x01, 0x00, 0x01])))

    await asyncio.sleep(2)
    protocol.send(ApiProdTestReq(opcode=0x00, data=bytes([0x02, 0x01, 0x00, 0x00])))

    await asyncio.sleep(2)
    protocol.send(ApiProdTestReq(opcode=0x00, data=bytes([0x02, 0x01, 0x00, 0x00])))

    await asyncio.sleep(2)
    protocol.send(ApiPpMmRegistrationAutoReq(0x01, bytes([0xFF, 0xFF, 0x00, 0x00])))

    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated.")
