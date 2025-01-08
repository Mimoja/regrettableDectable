from Api.Commands import Commands
from Api.IMAGE import ApiImageActivateCfm, ApiImageInfoCfm
from Api.PROD import ApiProdTestCfm
from termcolor import colored
from Api.PPGENERAL import ApiPpGetFwVersionCfm
from Api.FPGENERAL import ApiFpGetFwVersionCfm
from enum import Enum
from Api.PROD import DectMode
from Api.PPMM import (
    ApiPpMmFpNameInd,
    ApiPpMmRegistrationSearchInd,
    ApiPpMmRegistrationFailedInd,
    ApiPpMmRejectReasonType,
)


def dectMode(mode_id: int):
    dect_mode = ""
    match DectMode(mode_id):
        case DectMode.EU:
            dect_mode = "EU"
        case DectMode.US:
            dect_mode = "US"
        case DectMode.SA:
            dect_mode = "SA"
        case DectMode.Taiwan:
            dect_mode = "Taiwan"
        case DectMode.Malaysia:
            dect_mode = "Malaysia"
        case DectMode.China:
            dect_mode = "China"
        case DectMode.Thailand:
            dect_mode = "Thailand"
        case DectMode.Brazil:
            dect_mode = "Brazil"
        case DectMode.US_Extended:
            dect_mode = "US Extended"
        case DectMode.Korea:
            dect_mode = "Korea"
        case DectMode.Japan_2ch:
            dect_mode = "Japan (2ch)"
        case DectMode.Japan_5ch:
            dect_mode = "Japan (5ch)"
        case _:
            dect_mode = "Invalid"
    return dect_mode


def parseMail(primitive, params):
    payload = bytes([primitive & 0xFF, primitive >> 8, *params])
    match primitive:
        case Commands.API_FP_RESET_IND:
            print(
                "API_FP_RESET_IND received:",
                "Success" if params[0] == 0 else f"Error: {params[0]}",
            )

        case Commands.API_PP_GET_FW_VERSION_CFM:
            print("API_PP_GET_FW_VERSION_CFM received.")
            return ApiPpGetFwVersionCfm.from_bytes(payload)
        case Commands.API_FP_GET_FW_VERSION_CFM:
            print("API_FP_GET_FW_VERSION_CFM received.")
            return ApiFpGetFwVersionCfm.from_bytes(payload)
        case Commands.API_FP_MM_GET_ID_CFM:
            print("API_FP_MM_GET_ID_CFM received.")
            print(f"ID: {params[1]:02x}{params[2]:02x}{params[3]:02x}{params[4]:02x}")
        case Commands.API_FP_MM_GET_ACCESS_CODE_CFM:
            print("API_FP_MM_GET_ACCESS_CODE_CFM received.")
            access_code = (
                f"{params[1]:02x}{params[2]:02x}{params[3]:02x}{params[4]:02x}"
            )
            access_code = access_code.lstrip("f")
            print(f"Access Code: {access_code}")
        case Commands.API_FP_MM_SET_REGISTRATION_MODE_CFM:
            print(
                "API_FP_MM_SET_REGISTRATION_MODE_CFM received:",
                "Success" if params[0] == 0 else f"Error: {params[0]}",
            )
        case Commands.API_FP_MM_REGISTRATION_COMPLETE_IND:
            print("API_FP_MM_REGISTRATION_COMPLETE_IND received.")
            print("Registration complete!")
            print("Handset ID", params[1])
            # print(f"resp len {params[2]:02x} {params[3]:02x}")
            # length = int(params[2:3])
            # print("InfoElement", params[4 : 4 + length])
        case Commands.API_FP_MM_HANDSET_PRESENT_IND:
            print("API_FP_MM_HANDSET_PRESENT_IND received.")
            print("New handset present!")
            print("Handset ID", params[0])
        case Commands.API_PP_MM_FP_NAME_IND:
            print("API_PP_MM_FP_NAME_IND received.")
            return ApiPpMmFpNameInd.from_bytes(payload)
        case Commands.API_PP_MM_REGISTRATION_SEARCH_IND:
            print("API_PP_MM_REGISTRATION_SEARCH_IND received.")
            return ApiPpMmRegistrationSearchInd.from_bytes(payload)
        case Commands.API_PROD_TEST_REQ:
            print(
                f"API_PROD_TEST_REQ received. OpCode: {params[1]:02x} {params[0]:02x}"
            )
        case Commands.API_PROD_TEST_CFM:
            print(
                f"API_PROD_TEST_CFM received. OpCode: {params[1]:02x} {params[0]:02x}"
            )
            cfm = ApiProdTestCfm.from_bytes(payload)
            print("Opcode", cfm.Opcode)
            print("Param Length=", cfm.ParameterLength)
            print("Parameters=", cfm.getParameters())
            return cfm
        case Commands.API_IMAGE_ACTIVATE_CFM:
            print(
                "API_IMAGE_ACTIVATE_CFM received:",
                "Success" if params[0] == 0 else f"Error: {params[0]}",
            )
        case Commands.API_PP_MM_REGISTRATION_FAILED_IND:
            print("API_PP_MM_REGISTRATION_FAILED_IND received.")
            return ApiPpMmRegistrationFailedInd.from_bytes(payload)
        case Commands.API_HAL_LED_CFM:
            print("API_HAL_LED_CFM  received.")
            print("LEDs toggled.")
        case Commands.API_IMAGE_ACTIVATE_CFM:
            print("API_IMAGE_ACTIVATE_CFM received.")
            print(ApiImageActivateCfm.from_bytes(payload).Status)
        case Commands.API_PP_CRADLE_DETECT_IND:
            print("API_PP_CRADLE_DETECT_IND received.")
        case Commands.API_HAL_DEVICE_CONTROL_CFM:
            print("API_HAL_DEVICE_CONTROL_CFM received.")
        case Commands.API_PP_RESET_IND:
            print("API_PP_RESET_IND received.")
        case Commands.API_FP_RESET_IND:
            print("API_FP_RESET_IND received.")
        case Commands.API_PP_BAT_NON_CHARGEABLE_IND:
            print("API_PP_BAT_NON_CHARGEABLE_IND received.")
        case Commands.API_PP_BAT_CAPACITY_IND:
            print("API_PP_BAT_CAPACITY_IND received")
        case Commands.API_PP_BAT_CHARGE_IND:
            print("API_PP_BAT_CHARGE_IND received")
        case Commands.API_IMAGE_INFO_CFM:
            print("API_IMAGE_INFO_CFM received")
            try:
                cfm = ApiImageInfoCfm.from_bytes(payload)
                print("Status", cfm.Status)
                print("ImageIndex", cfm.ImageIndex)
                print("ImageId", cfm.ImageId)
                print("DeviceId", cfm.DeviceId)
                print("LinkDate", cfm.LinkDate)
                print("NameLength", cfm.NameLength)
                print("LabelLength", cfm.LabelLength)
                print("Data", cfm.Data.decode("utf-8"))
            except Exception:
                pass

        case Commands.RTX_EAP_TARGET_RESET_IND:
            print("RTX_EAP_TARGET_RESET_IND recieved")
            print("=================================")
            print("TARGET RESET")
            print("=================================")

        case _:
            print(
                colored("Unknown primitive: ", "blue"),
                colored(Commands(primitive).name, "blue"),
            )
            return
