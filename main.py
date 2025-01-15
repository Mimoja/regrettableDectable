import asyncio
import logging
import sys

import serial_asyncio
from termcolor import colored
import EepromTypes
from Api.Api import RsStatusType
from Api.CC import (
    ApiCcAlertReq,
    ApiCcBasicServiceType,
    ApiCcCallClassType,
    ApiCcConnectReq,
    ApiCcGetConEiReq,
    ApiCcRejectInd,
    ApiCcReleaseReasonType,
    ApiCcSetupInd,
    ApiCcSetupReq,
    ApiCcSignalType,
)
from Api.Commands import Commands, PtCommand
from Api.FPGENERAL import ApiFpGetFwVersionReq
from Api.FPMM import ApiFpMmGetAccessCodeReq, ApiFpMmGetIdReq
from Api.HAL import (
    ApiHalLedCmdIdType,
    ApiHalLedCmdType,
    ApiHalLedReqType,
    ApiHalWriteReq,
    ApiHalAreaType,
    ApiHalReadReq,
    ApiHalReadCfm,
)
from Api.IMAGE import ApiImageActivateReq, ApiImageInfoCfm, ApiImageInfoReq
from Api.INFOELEMENT import (
    ApiCallingPartyNumberType,
    ApiCodecListType,
    InfoElement,
    InfoElements,
    parseInfoElements,
)
from Api.PPGENERAL import ApiPpGetFwVersionReq, ApiPpResetReq
from Api.PPMM import (
    ApiMmSearchModeType,
    ApiPpMmEasyPairingSearchReq,
    ApiPpMmGetExtHigherLayerCap2Cfm,
    ApiPpMmGetExtHigherLayerCap2Req,
    ApiPpMmLockedInd,
    ApiPpMmLockedReq,
    ApiPpMmLockReq,
    ApiPpMmRegistrationAutoReq,
    ApiPpMmRegistrationSearchInd,
    ApiPpMmRegistrationSearchReq,
    ApiPpMmRegistrationSelectedReq,
    ApiPpMmRegistrationStopReq,
    ApiPpMmRejectReason,
    ApiPpMmUnlockedInd,
)
from Api.PROD import ApiProdTestReq, DectMode
from APIParser import dectMode
from Dect import DECT
from MailProtocol import MailProtocol
from util import hexdump
from Api.AUDIO import (
    ApiPpAudioInitPcmReq,
    ApiPcmClkType,
    ApiPpAudioOpenReq,
    ApiPpAudioUnmuteReq,
    ApiPcmFscFreqType,
    ApiPcmFscLengthType,
    ApiPpAudioMuteRxTxType,
)
from EepromDefinitions import EepromDef


async def reset_pp(dct: DECT):
    print(colored("Resetting PP...", "yellow"))
    await dct.command(ApiPpResetReq(), timeout=20)
    print(colored("PP reset", "green"))


async def reset_nv_storage(dct: DECT):
    print(colored("Resetting NV Storage...", "yellow"))
    await dct.command(ApiProdTestReq(opcode=PtCommand.PT_CMD_NVS_DEFAULT, data=[0x01]))
    await dct.command(ApiPpResetReq(), timeout=20)
    print(colored("NV Storage reset", "green"))


async def ensure_pp_mode(dct: DECT):
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
            await dct.command(ApiImageActivateReq(0x00, False))
            await asyncio.sleep(12)
        else:
            print(colored("DECT Chip is in unknown mode", "yellow"))
            sys.exit(1)
    else:
        print(colored("DECT Chip is in PP mode", "yellow"))
        print(colored("PP Version:", "yellow"), pp_version)


async def set_dect_mode(dct: DECT):
    print(
        colored(
            "Requesting Dect mode (API_PROD_TEST_REQ :: PT_CMD_GET_DECT_MODE)", "yellow"
        )
    )
    prod = await dct.command(
        ApiProdTestReq(opcode=PtCommand.PT_CMD_GET_DECT_MODE, data=[0x00])
    )
    dect_mode = prod.getParameters()[0]

    print(colored(f"DECT Mode: {dectMode(dect_mode)} {hex(dect_mode)}", "yellow"))
    if dect_mode == 0xFF:
        print(colored("DECT Mode is 0xFF, resetting NVS first...", "red"))
        await reset_nv_storage(dct)
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


async def lock(dct: DECT, request_lock=False):
    print(colored("Sending / Requesting Lock command...", "yellow"))
    cmd = ApiPpMmLockReq() if request_lock else ApiPpMmLockedReq()
    await dct.command(cmd, timeout=0, max_retries=1)
    locked_resp = await dct.wait_for(
        [
            Commands.API_PP_MM_LOCKED_IND,
            Commands.API_PP_MM_UNLOCKED_IND,
        ],
        timeout=30,
    )
    if not locked_resp:
        print(colored("PPMM locking status failed", "red"))
        return False

    if type(locked_resp) is ApiPpMmLockedInd:
        print(colored("PPMM is locked", "white"))
        return True
    else:
        print(colored("PPMM is unlocked", "white"))
        return False


async def list_images(dct: DECT):
    i = 0
    images = []
    while True:
        print(colored(f"Getting info for image = {i}", "yellow"))
        image_info: ApiImageInfoCfm = await dct.command(ApiImageInfoReq(image=i))
        if not image_info:
            break

        status = RsStatusType(image_info.Status)
        if status == RsStatusType.RSS_NOT_FOUND or image_info.ImageIndex == 0xFF:
            print(colored(f"Stopping Enumeration after {i} images", "yellow"))
            break

        if status == RsStatusType.RSS_NO_DATA:
            print(colored(f"Skipping image {i} due to no data", "yellow"))
            i += 1
            continue

        image = image_info.to_dict()
        images.append(
            {
                "index": i,
                "status": status.name,
                "id": image.get("ImageId"),
                "device_id": image.get("DeviceId"),
                "link_date": image.get("LinkDate"),
                "name": image.get("name"),
                "label": image.get("label"),
            }
        )
        i += 1

    for image in images:
        color = "green" if image["status"] == "RSS_SUCCESS" else "magenta"
        print(colored(f"Image {image['index']}:", color))
        print(colored(f"Status: {image['status']}", color))
        print(colored(f"ID: {image['id']}", color))
        print(colored(f"Device ID: {image['device_id']}", color))
        print(colored(f"Link Date: {image['link_date']}", color))
        print(colored(f"Name: {image['name']}", color))
        print(colored(f"Label: {image['label']}", color))


async def blink_led(dct: DECT, led: int):
    print(colored(f"Blinking the LED {led}...", "blue"))
    await dct.command(
        ApiHalLedReqType(
            led=led,
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


async def auto_register(dct: DECT):
    print(colored("Auto registering", "yellow"))

    await dct.command(
        ApiPpMmRegistrationAutoReq(1, bytes([0xFF, 0xFF, 0x00, 0x00])),
        max_retries=1,
        timeout=0,
    )

    total_time = 0
    while True:
        timeout = 5
        status = await dct.wait_for(
            [
                Commands.API_PP_MM_REGISTRATION_COMPLETE_IND,
                Commands.API_PP_MM_REGISTRATION_FAILED_IND,
            ],
            timeout=timeout,
        )
        total_time += timeout
        if not status:
            print(
                colored(
                    f"Registration status not yet received after {total_time}", "red"
                )
            )
        else:
            break

    if status.Primitive == Commands.API_PP_MM_REGISTRATION_FAILED_IND:
        print(colored("Registration failed!", "red"))
        print(
            colored("Reason: ", "red"),
            colored(ApiPpMmRejectReason(status.Reason).name, "red"),
        )
        sys.exit(1)
    return status


async def manual_register(dct: DECT):
    print(colored("Starting registration scan", "yellow"))

    await dct.command(
        ApiPpMmRegistrationSearchReq(1),
        max_retries=1,
        timeout=0,
    )

    baseStation = await dct.wait_for(
        Commands.API_PP_MM_REGISTRATION_SEARCH_IND, timeout=40
    )

    if not baseStation:
        print(colored("Base Station not found!", "red"))
        sys.exit(1)
    print(colored("Base Station found!", "green"))
    print(baseStation.caps())
    rfpi = baseStation.Rfpi
    print(colored("RFPI:", "yellow"), hexdump(bytes(rfpi), False))

    print(colored("Requesting search stop", "yellow"))
    await dct.command(ApiPpMmRegistrationStopReq(), max_retries=1, timeout=10)

    print(colored("Connecting to base station", "yellow"))
    await dct.command(
        ApiPpMmRegistrationSelectedReq(
            subscription_no=1,
            ac_code=bytes([0xFF, 0xFF, 0x00, 0x00]),
            rfpi=rfpi,
        ),
        max_retries=1,
        timeout=0,
    )
    status = await dct.wait_for(
        [
            Commands.API_PP_MM_REGISTRATION_COMPLETE_IND,
            Commands.API_PP_MM_REGISTRATION_FAILED_IND,
        ],
        timeout=40,
    )
    if not status:
        print(colored("Registration status not received!", "red"))
        sys.exit(1)

    if status.Primitive == Commands.API_PP_MM_REGISTRATION_FAILED_IND:
        print(colored("Registration failed!", "red"))
        print(
            colored("Reason: ", "red"),
            colored(ApiPpMmRejectReason(status.Reason).name, "red"),
        )
        sys.exit(1)
    return status


def parse_call(call_resp):
    call = call_resp.to_dict()
    print(colored("We are beeing called:", "yellow"))
    print(colored("Connection (E)ID:", "yellow"), call.get("ConEi"))
    print(
        colored("Call Class:", "yellow"),
        ApiCcCallClassType(call.get("CallClass")).name,
    )
    print(
        colored("Basic Service:", "yellow"),
        ApiCcBasicServiceType(call.get("BasicService")).name,
    )
    print(
        colored("Call Class:", "yellow"),
        ApiCcCallClassType(call.get("CallClass")).name,
    )
    print(colored("Signal:", "yellow"), ApiCcSignalType(call.get("Signal")).name)

    infoElements = parseInfoElements(call.get("InfoElement"))
    codectsIE: InfoElement = None
    for ie in infoElements:
        match ie.type:
            case InfoElements.API_IE_CALLING_PARTY_NUMBER:
                callingNumber = ApiCallingPartyNumberType.from_bytes(ie.data)
                print(colored("\tCalling Party Number:", "yellow"), callingNumber)
            case InfoElements.API_IE_CODEC_LIST:
                codects = ApiCodecListType.from_bytes(ie.data)
                print(colored("\tCodecs:", "yellow"), codects)
                codectsIE = ie
            case _:
                print(colored("\tInfo Element (Unparsed):", "yellow"), ie)
    return codectsIE, call


async def main():
    logging.getLogger("DECT").setLevel(logging.INFO)
    logging.getLogger("MailProtocol").setLevel(logging.WARNING)

    port = "/dev/ttyUSB0"
    baudrate = 115200

    dct = DECT(port, baudrate)

    await dct.connect()

    # Uncomment to reset the DECT modules NV storage
    # await reset_nv_storage(dct)
    await blink_led(dct, 2)
    await asyncio.sleep(0.250)
    await blink_led(dct, 3)

    await ensure_pp_mode(dct)
    await set_dect_mode(dct)
    await list_images(dct)
    locked = await lock(dct, request_lock=False)
    if not locked:
        locked = await lock(dct, request_lock=True)

    if locked is None:
        print(
            colored(
                "Failed to receive lock reponse. Resetting and exiting. Please try again",
                "red",
            )
        )
        await reset_pp()
        sys.exit(1)

    if not locked:
        # status = await manual_register(dct)
        status = await auto_register(dct)

        print(colored("Registration successful!", "green"))
        print(colored("Status", "yellow"), status)

    print(colored("Waiting for incoming call...", "yellow"))
    while True:
        call_resp: ApiCcSetupInd = await dct.wait_for(
            [
                Commands.API_CC_SETUP_IND,
            ],
            timeout=None,
        )
        codectsIE, call = parse_call(call_resp)

        if not codectsIE:
            print(colored("No codec list received, rejecting call", "red"))
            await dct.command(
                ApiCcRejectInd(
                    call.get("ConEi"),
                    ApiCcReleaseReasonType.API_RR_NEGOTIATION_NOT_SUPPORTED,
                )
            )
            continue

        print(colored("Accepting call...", "yellow"))
        # Optionally start alerting
        # Use API_PP_AUDIO_START_TONE_REQ here to play a sound
        # print(colored("Inform FP about our alerting", "yellow"))
        # await dct.command(ApiCcAlertReq(call.get("ConEi"), bytes()))

        connect = await dct.command(
            ApiCcConnectReq(call.get("ConEi"), codectsIE.to_bytes())
        )
        print(colored("Call connected!", "green"), connect)
        print(colored("Unmuting", "yellow"))

        await dct.command(
            ApiPpAudioUnmuteReq(muteRxTx=ApiPpAudioMuteRxTxType.API_MUTE_BOTH)
        )
        print(colored("Unmuted", "green"))

        call = await dct.wait_for(
            [
                Commands.API_CC_REJECT_IND,
            ],
            timeout=None,
        )
        print(colored("Call ended!", "magenta"), call)

    await asyncio.Future()


if __name__ == "__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated.")
