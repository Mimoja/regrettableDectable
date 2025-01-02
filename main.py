import asyncio
from MailProtocol import MailProtocol
import serial_asyncio
from Api.HAL import ApiHalLedReqType, ApiHalLedCmdType, ApiHalLedCmdIdType
from Api.FPGENERAL import ApiFpGetFwVersionReq
from Api.IMAGE import ApiImageActivateReq
from Api.PROD import ApiProdTestReq
from Api.PPMM import (
    ApiPpMmRegistrationAutoReq,
)
from Api.FPMM import ApiFpMmGetIdReq, ApiFpMmGetAccessCodeReq


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

    # Uncomment to set region
    # print("Sending 'API_PROD_TEST_REQ' request command...")
    #  #        0x02,  # SET_DECT_MODE
    #  #       0x00,
    #  #       0x01,  # Parameter len
    #  #       0x00,  # EU
    # protocol.send(ApiProdTestReq(opcode=0x00, data=bytes([0x02, 0x00, 0x01, 0x00])))

    await asyncio.sleep(2)
    print("Sending 'API_FP_GET_FW_VERSION' request command...")
    protocol.send(
        ApiFpGetFwVersionReq(),
    )
    await asyncio.sleep(1)
    print("Sending 'API_FP_MM_GET_ID_REQ' request command...")
    protocol.send(ApiFpMmGetIdReq())
    
    await asyncio.sleep(1)
    print("Sending 'API_FP_MM_GET_ACCESS_CODE_REQ' request command...")
    protocol.send(ApiFpMmGetAccessCodeReq())

    await asyncio.sleep(1)
    print("Sending 'API_HAL_LED_REQ' request command...")
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
    protocol.send(ApiPpMmRegistrationAutoReq(0x01, bytes([0xFF, 0xFF, 0x00, 0x00])))

    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated.")
