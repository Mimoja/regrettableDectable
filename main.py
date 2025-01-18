import asyncio
import logging
import sys
import struct

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
    ApiHalLedReq,
    ApiHalWriteReq,
    ApiHalAreaType,
    ApiHalReadReq,
    ApiHalReadCfm,
)
from Api.IMAGE import ApiImageActivateReq, ApiImageInfoCfm, ApiImageInfoReq
from Api.INFOELEMENT import (
    ApiCallingPartyNumber,
    ApiCodecListType,
    InfoElement,
    ApiCallingPartyName,
    InfoElements,
    parseInfoElements,
    ApiCodecInfoType,
    ApiCodecType,
    ApiMacDlcServiceType,
    ApiCplaneRoutingType,
    ApiSlotSizeType,
    ApiNegotiationIndicatorType,
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
    ApiPpAudioModeType,
    ApiPpAudioUnmuteReq,
    ApiPcmFscFreqType,
    ApiPcmFscLengthType,
    ApiPpAudioCloseReq,
    ApiPpAudioMuteRxTxType,
    ApiPpAudioSetVolumeReq,
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
    pp_version = await dct.command(ApiPpGetFwVersionReq(), max_retries=2, timeout=2)

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
            await dct.wait_for(Commands.API_PP_RESET_IND, timeout=30)
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
            ApiHalWriteReq(ApiHalAreaType.AHA_NVS, 0x05, bytes([0x25])),
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
        print(colored("DECT Mode setting seemingly requires a reset", "green"))
        await dct.command(ApiPpResetReq(), timeout=0)
        await dct.wait_for(Commands.API_PP_RESET_IND, timeout=30)


async def lock(dct: DECT, request_lock=False):
    if request_lock:
        print(colored("Requesting Lock...", "yellow"))
    else:
        print(colored("Querrying Lock...", "yellow"))
    cmd = ApiPpMmLockReq(0) if request_lock else ApiPpMmLockedReq()
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
    print(colored(f"Blinking the LED {led}...", "yellow"))
    await dct.command(
        ApiHalLedReq(
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
        timeout = 10
        await dct.command(
            ApiPpMmRegistrationAutoReq(1, bytes([0xFF, 0xFF, 0x00, 0x00])),
            max_retries=1,
            timeout=0,
        )
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
                    f"Registration status not yet received after {total_time}s", "red"
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
                    f"Registration status not yet received after {total_time}s", "red"
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


def parse_call(call: ApiCcSetupInd):
    print(colored("We are beeing called:", "yellow"))
    print(colored("Connection (E)ID:", "yellow"), call.ConEi)
    print(colored("Call Class:", "yellow"), ApiCcCallClassType(call.CallClass).name)
    print(colored("Service:", "yellow"), ApiCcBasicServiceType(call.BasicService).name)
    print(colored("Call Class:", "yellow"), ApiCcCallClassType(call.CallClass).name)
    print(colored("Signal:", "yellow"), ApiCcSignalType(call.Signal).name)

    infoElements = call.infoElements()
    codecsIE: InfoElement = None
    for ie in infoElements:
        match ie.type:
            case InfoElements.API_IE_CALLING_PARTY_NUMBER:
                calling_number = ApiCallingPartyNumber.from_bytes(ie.data)
                print(colored("\tCalling Party Number:", "yellow"), calling_number)
            case InfoElements.API_IE_CALLING_PARTY_NAME:
                calling_name = ApiCallingPartyName.from_bytes(ie.data)
                print(colored("\tCalling Party Name:", "yellow"), calling_name)
            case InfoElements.API_IE_CODEC_LIST:
                codects = ApiCodecListType.from_bytes(ie.data)
                print(colored("\tCodecs:", "yellow"), codects)
                codecsIE = ie
            case _:
                print(colored("\tInfo Element (Unparsed):", "yellow"), ie)
    return codecsIE, call


async def read_eeprom(dct: DECT, target: EepromTypes.BaseNode):
    read_answer: ApiHalReadCfm = await dct.command(
        ApiHalReadReq(ApiHalAreaType.AHA_NVS, target.offset, target.length),
    )
    if read_answer.Status != RsStatusType.RSS_SUCCESS:
        return None
    data = read_answer.data()
    target.from_bytes(bytes(data))
    return target


async def known_fps(dct: DECT):
    for target in [
        EepromDef.EepromNotInRam.Subs0,
        EepromDef.EepromNotInRam.Subs1,
        EepromDef.EepromNotInRam.Subs2,
        EepromDef.EepromNotInRam.Subs3,
    ]:
        sub = await read_eeprom(dct, target)
        if sub is None:
            continue
        if sub.RFPI.values != [0xFF, 0xFF, 0xFF, 0xFF, 0xFF]:
            return True
    return False


async def config_audio(dct: DECT):
    print(colored("Configuring audio...", "yellow"))

    print(colored("Setting PCM...", "yellow"))
    cmd = ApiPpAudioInitPcmReq(
        PcmEnable=1,
        IsMaster=1,
        Reserved=0,
        PcmFscFreq=ApiPcmFscFreqType.AP_FSC_FREQ_16KHZ,
        PcmFscLength=0x03,
        PcmFscStartAligned=0x01,
        PcmClk=ApiPcmClkType.AP_PCM_CLK_4608,
        PcmClkOnRising=0x01,
        PcmClksPerBit=0x01,
        PcmFscInvert=0,
        PcmCh0Delay=0,
        PcmDoutIsOpenDrain=0,
        PcmIsOpenDrain=0,
    )
    pcm_init = await dct.command(cmd)

    if pcm_init.Status != RsStatusType.RSS_SUCCESS:
        print(
            colored(f"Failed to init PCM: {RsStatusType(pcm_init.Status).name}", "red")
        )


async def get_ipei(dct):
    Ipei = await read_eeprom(dct, EepromDef.EepromInRam.Ipei)
    Ipei = Ipei.values
    man = ((Ipei[0] & 0x0F) << 12) + (Ipei[1] << 4) + ((Ipei[2] & 0xF0) >> 4)
    dev = ((Ipei[2] & 0x0F) << 16) + (Ipei[3] << 8) + Ipei[4]
    print(colored("IPEI:", "yellow"), f"{man:05d}", " ", f"{dev:07d}")


async def main():
    logging.getLogger("DECT").setLevel(logging.INFO)
    logging.getLogger("MailProtocol").setLevel(logging.WARNING)

    port = "/dev/ttyUSB0"
    baudrate = 115200

    dct = DECT(port, baudrate)

    await dct.connect()

    # Uncomment to reset the DECT modules NV storage
    # await reset_nv_storage(dct)
    await get_ipei(dct)
    await ensure_pp_mode(dct)
    await set_dect_mode(dct)
    await list_images(dct)
    locked = await lock(dct, request_lock=False)

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
        can_lock = await known_fps(dct)
        if can_lock:
            print(colored("Found a known FP in EEPROM. Trying to connect", "green"))
            locked = await lock(dct, request_lock=True)
        else:
            print(
                colored(
                    "No known FP found. Registration is the only way from here on",
                    "red",
                )
            )
    # Still not locked?
    if not locked:
        # status = await manual_register(dct)
        status = await auto_register(dct)

        print(colored("Registration successful!", "green"))
        print(colored("Status", "yellow"), status)

    await config_audio(dct)

    await blink_led(dct, 2)
    await asyncio.sleep(0.250)
    await blink_led(dct, 3)

    while True:
        print(colored("Waiting for incoming call...", "yellow"))

        call_resp: ApiCcSetupInd = await dct.wait_for(
            [
                Commands.API_CC_SETUP_IND,
            ],
            timeout=None,
        )
        codecsIE, call = parse_call(call_resp)

        if not codecsIE:
            print(colored("No codec list received, building our own", "red"))
            single_codec = ApiCodecInfoType(
                ApiCodecType.API_CT_G722,
                ApiMacDlcServiceType.API_MDS_1_MD,
                ApiCplaneRoutingType.API_CPR_CS,
                ApiSlotSizeType.API_SS_LS640,
            )
            codecsIE = ApiCodecListType(
                ApiNegotiationIndicatorType.API_NI_NOT_POSSIBLE, codecs=[single_codec]
            )
            print(colored("Using G722 codec", "yellow"))
            print(colored("Codecs:", "yellow"), codecsIE)

        # print(colored("Setting Audio volume...", "yellow"))
        # await dct.command(ApiPpAudioSetVolumeReq(volume=0))

        print(colored("Opening Audio...", "yellow"))
        await dct.command(
            ApiPpAudioOpenReq(ApiPpAudioModeType.API_AUDIO_MODE_HEADSET),
            max_retries=1,
            timeout=0,
        )

        print(colored("Sending Alert status...", "yellow"))
        await dct.command(ApiCcAlertReq(call.ConEi, bytes()), max_retries=1, timeout=0)

        # Optionally start alerting
        # Use API_PP_AUDIO_START_TONE_REQ here to play a sound
        # print(colored("Inform FP about our alerting", "yellow"))
        # await dct.command(ApiCcAlertReq(call.ConEi, bytes()))
        await config_audio(dct)

        print(colored("Accepting call...", "yellow"))

        connect = await dct.command(
            ApiCcConnectReq(call.ConEi, codecsIE.to_bytes()), max_retries=3, timeout=1
        )
        print(colored("Unmuting", "yellow"))

        await dct.command(
            ApiPpAudioUnmuteReq(muteRxTx=ApiPpAudioMuteRxTxType.API_MUTE_TX),
            max_retries=1,
            timeout=0,
        )
        print(colored("Call connected!", "green"), connect)

        while True:
            call = await dct.wait_for(
                [
                    Commands.API_CC_INFO_IND,
                    Commands.API_CC_RELEASE_IND,
                    Commands.API_CC_REJECT_IND,
                ],
                timeout=None,
            )
            match call.Primitive:
                case Commands.API_CC_INFO_IND:
                    print(colored("Call info:", "yellow"), call)
                case Commands.API_CC_RELEASE_IND:
                    print(colored("Call release!", "magenta"), call)
                    await dct.command(
                        ApiCcRejectInd(
                            call.ConEi,
                            ApiCcReleaseReasonType.API_RR_USER_REJECTION,
                            bytes([]),
                        )
                    )
                    break
                case Commands.API_CC_REJECT_IND:
                    print(colored("Call ended!", "magenta"), call)
                    break
        print(colored("Closing Audio...", "yellow"))
        await dct.command(
            ApiPpAudioCloseReq(),
            max_retries=1,
            timeout=0,
        )

    await asyncio.Future()

if __name__ == "__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated.")
