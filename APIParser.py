def parseMail(primitive, params):
    match primitive:
        case 0x4001:
            print(
                "API_FP_RESET_IND received:",
                "Success" if params[0] == 0 else f"Error: {params[0]}",
            )
        case 0x4003:
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
        case 0x4FFF:
            print(
                f"API_PROD_TEST_CFM received. OpCode: {params[1]:02x} {params[0]:02x}"
            )
        case 0x5803:
            print(
                "API_IMAGE_ACTIVATE_CFM received:",
                "Success" if params[0] == 0 else f"Error: {params[0]}",
            )

        case 0x5903:
            print("API_HAL_LED_CFM  received.")
            print("LEDs toggled.")
        case _:
            print("Unknown primitive: ", hex(primitive))
