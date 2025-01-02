from Api.Commands import Commands
from Api.IMAGE import ApiImageActivateCfm
from util import hexdump


def parseMail(primitive, params):
    payload = bytes([primitive & 0xFF, primitive >> 8, *params])
    match primitive:
        case Commands.API_FP_GET_FW_VERSION_CFM:
            print("API_FP_GET_FW_VERSION_CFM received.")
            print(
                f"Version: {params[3]:02x}{params[2]:02x}{params[1]:02x}{params[0]:02x}"
            )
            print(
                f"Link Date: {params[7]:02}/{params[6]:02}/{params[5]:02} at {params[8]:02}:{params[9]:02}"
            )
            # Mode can be changed with an API_PROD_TEST_REQ command
            print(f"Dect mode: {params[10]}")
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
        case Commands.API_PROD_TEST_CFM:
            print("API_PROD_TEST_CFM received.")
        case _:
            print("Unknown primitive: ", hex(primitive))
