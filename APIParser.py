from Api.Commands import Commands
from Api.IMAGE import ApiImageActivateCfm

def parseMail(primitive, params):
    payload = bytes([primitive & 0xFF, primitive >> 8, *params])
    match primitive:
        case Commands.API_FP_RESET_IND:
            print(
                "API_FP_RESET_IND received:",
                "Success" if params[0] == 0 else f"Error: {params[0]}",
            )
        case Commands.API_FP_GET_FW_VERSION_CFM:
            print("API_FP_GET_FW_VERSION_CFM received.")
            print(
                f"Version: {params[3]:02x}{params[2]:02x}{params[1]:02x}{params[0]:02x}"
            )
            print(
                f"Link Date: {params[7]:02}/{params[6]:02}/{params[5]:02} at {params[8]:02}:{params[9]:02}"
            )
            # Mode can be changed with an API_PROD_TEST_REQ command
            dect_mode = ""

            match params[10]:
                case 0:
                    dect_mode = "EU"
                case 1:
                    dect_mode = "US"
                case 2:
                    dect_mode = "SA"
                case 3:
                    dect_mode = "Taiwan"
                case 4:
                    dect_mode = "Malaysia"
                case 5:
                    dect_mode = "China"
                case 6:
                    dect_mode = "Thailand"
                case 7:
                    dect_mode = "Brazil"
                case 8:
                    dect_mode = "US Extended"
                case 9:
                    dect_mode = "Korea"
                case 10:
                    dect_mode = "Japan (2ch)"
                case 11:
                    dect_mode = "Japan (5ch)"
                case _:
                    dect_mode = "Invalid"

            print(f"DECT mode: {dect_mode}")
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
        case Commands.API_PROD_TEST_CFM:
            print(
                f"API_PROD_TEST_CFM received. OpCode: {params[1]:02x} {params[0]:02x}"
            )
        case Commands.API_IMAGE_ACTIVATE_CFM:
            print(
                "API_IMAGE_ACTIVATE_CFM received:",
                "Success" if params[0] == 0 else f"Error: {params[0]}",
            )

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
