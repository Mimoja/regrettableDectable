import asyncio
from MailProtocol import MailProtocol
import serial_asyncio
from Api.HAL import (
    ApiHalLedReqType,
    ApiHalLedCmdType,
    ApiHalLedCmdIdType,
    ApiHalWriteReq,
    HalAreaType,
)
from Api.FPGENERAL import ApiFpGetFwVersionReq
from Api.PPGENERAL import ApiPpGetFwVersionReq
from Api.IMAGE import ApiImageActivateReq, ApiImageInfoReq
from Api.PROD import ApiProdTestReq, DectMode
from Api.PPMM import (
    ApiPpMmRegistrationAutoReq,
    ApiPpMmRegistrationSearchReq,
    ApiMmSearchModeType,
    ApiPpMmRegistrationSelectedReq,
)
from Api.Commands import PtCommand, Commands
from Api.FPMM import ApiFpMmGetIdReq, ApiFpMmGetAccessCodeReq
from util import hexdump
from termcolor import colored
from Dect import DECT
import sys
from APIParser import dectMode


async def main():
    port = "/dev/ttyUSB1"
    baudrate = 115200

    dct = DECT(port, baudrate)

    await dct.connect()

    await asyncio.sleep(1)

    print(colored("Sending 'API_PP_GET_FW_VERSION' request command...", "yellow"))
    pp_version = await dct.command(ApiPpGetFwVersionReq(), max_retries=2)

    if not pp_version:
        print(colored("Sending 'API_FP_GET_FW_VERSION' request command...", "yellow"))
        fp_version = await dct.command(ApiFpGetFwVersionReq(), max_retries=1)

        # Check if the DECT Chip is in FP or PP mode
        if fp_version:
            print(colored("DECT Chip is in FP mode, switching to PP mode", "yellow"))

            # Only needed if the image is offline (status = 0x1c / 28)
            print(
                colored("Sending 'API_IMAGE_ACTIVATE_REQ' request command...", "yellow")
            )
            await dct.command(ApiImageActivateReq(0x01, False))
            await asyncio.sleep(12)
        else:
            print(colored("DECT Chip is in unknown mode", "yellow"))
            sys.exit(1)
    else:
        print(colored("DECT Chip is in PP mode", "yellow"))

    print(colored("Sending API_PROD_TEST_REQ :: PT_CMD_GET_DECT_MODE", "yellow"))
    prod = await dct.command(
        ApiProdTestReq(opcode=PtCommand.PT_CMD_GET_DECT_MODE, data=[0x00])
    )
    dect_mode = prod.getParameters()[0]

    print(colored(f"DECT Mode: {dectMode(dect_mode)} {hex(dect_mode)}", "yellow"))
    if dect_mode != DectMode.EU:
        print(colored("DECT Mode is not EU, Setting now...", "yellow"))
        print(colored("Sending API_HAL_WRITE_REQ to write NVS", "yellow"))
        await dct.command(
            ApiHalWriteReq(HalAreaType.AHA_NVS, 0x05, bytes([0x25])),
        )
        print(colored("Sending API_PROD_TEST_REQ :: PT_CMD_SET_DECT_MODE", "yellow"))
        await dct.command(
            ApiProdTestReq(opcode=PtCommand.PT_CMD_SET_DECT_MODE, data=[0x00]),
        )

        prod = await dct.command(
            ApiProdTestReq(opcode=PtCommand.PT_CMD_GET_DECT_MODE, data=[0x00])
        )
        dect_mode = prod.getParameters()[0]
        print("DECT Mode after setting:", dectMode(dect_mode))
        if dect_mode != DectMode.EU:
            print(colored("Failed to set DECT Mode to EU", "red"))
            sys.exit(1)

    print(colored("Blinking the blue LED...", "blue"))
    print(colored("Sending 'API_HAL_LED_REQ' request command...", "yellow"))
    await dct.command(
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

    print(colored("Trying auto registration", "green"))

    await dct.command(
        ApiPpMmRegistrationAutoReq(1, bytes([0xFF, 0xFF, 0x00, 0x00])),
    )

    baseStationName = await dct.wait_for(Commands.API_PP_MM_FP_NAME_IND, timeout=40)
    if not baseStationName:
        print(colored("Base Station not found!", "red"))
        sys.exit(1)

    print(colored("Base Station found!", "green"))
    print(baseStationName.caps())

    # print(
    #     colored(
    #         "Sending 'API_PP_MM_REGISTRATION_SEARCH_REQ' request command...", "yellow"
    #     )
    # )
    # await dct.command(
    #     ApiPpMmRegistrationSearchReq(ApiMmSearchModeType.API_MM_CONTINOUS_SEARCH),
    #     max_retries=1,
    #     timeout=0,
    # )

    # baseStation = await dct.wait_for(
    #     Commands.API_PP_MM_REGISTRATION_SEARCH_IND, timeout=40
    # )

    # if not baseStation:
    #     print(colored("Base Station not found!", "red"))
    #     sys.exit(1)
    # print(colored("Base Station found!", "green"))
    # print(baseStation.caps())

    # await dct.command(
    #     ApiPpMmRegistrationSelectedReq(
    #         subscription_no=1,
    #         ac_code=bytes([0xFF, 0xFF, 0x00, 0x00]),
    #         rfpi=baseStation.Rfpi,
    #     ),
    #     max_retries=1,
    #     timeout=0,
    # )

    # status = await dct.wait_for(
    #     [
    #         Commands.API_PP_MM_REGISTRATION_COMPLETE_IND,
    #         Commands.API_PP_MM_REGISTRATION_FAILED_IND,
    #     ],
    #     timeout=40,
    # )
    # if status:
    #     if status.Primitive == Commands.API_PP_MM_REGISTRATION_COMPLETE_IND:
    #         print(colored("Registration complete!", "green"))
    #     else:
    #         print(colored("Registration failed!", "red"))
    #         print(status.Reason)
    #         await dct.command(
    #             ApiPpMmRegistrationAutoReq(0, bytes([0xFF, 0xFF, 0x00, 0x00])),
    #             max_retries=1,
    #         )

    await asyncio.Future()


if __name__ == "__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated.")
