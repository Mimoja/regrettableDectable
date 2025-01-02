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
            dect_mode_id = params[10]
            dect_mode = ""

            if dect_mode_id == 0:
                dect_mode = "EU"
            elif dect_mode_id == 1:
                dect_mode = "US"
            elif dect_mode_id == 2:
                dect_mode = "SA"
            elif dect_mode_id == 3:
                dect_mode = "Taiwan"
            elif dect_mode_id == 4:
                dect_mode = "Malaysia"
            elif dect_mode_id == 5:
                dect_mode = "China"
            elif dect_mode_id == 6:
                dect_mode = "Thailand"
            elif dect_mode_id == 7:
                dect_mode = "Brazil"
            elif dect_mode_id == 8:
                dect_mode = "US Extended"
            elif dect_mode_id == 9:
                dect_mode = "Korea"
            elif dect_mode_id == 10:
                dect_mode = "Japan (2ch)"
            elif dect_mode_id == 11:
                dect_mode = "Japan (5ch)"
            else:
                dect_mode = "Invalid"

            print(f"DECT mode: {dect_mode}")
        case 0x4005:
            print("API_FP_MM_GET_ID_CFM received.")
            print(f"ID: {params[1]:02x}{params[2]:02x}{params[3]:02x}{params[4]:02x}")
        case 0x400B:
            print("API_FP_MM_GET_ACCESS_CODE_CFM received.")
            access_code = (
                f"{params[1]:02x}{params[2]:02x}{params[3]:02x}{params[4]:02x}"
            )
            access_code = access_code.lstrip("f")
            print(f"Access Code: {access_code}")
        case 0x4106:
            print(
                "API_FP_MM_SET_REGISTRATION_MODE_CFM received:",
                "Success" if params[0] == 0 else f"Error: {params[0]}",
            )
        case 0x4107:
            print("API_FP_MM_REGISTRATION_COMPLETE_IND received.")
            print("Registration complete!")
            print("Handset ID", params[1])
            # print(f"resp len {params[2]:02x} {params[3]:02x}")
            # length = int(params[2:3])
            # print("InfoElement", params[4 : 4 + length])
        case 0x4108:
            print("API_FP_MM_HANDSET_PRESENT_IND received.")
            print("New handset present!")
            print("Handset ID", params[0])

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
