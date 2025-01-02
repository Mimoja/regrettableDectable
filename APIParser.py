def parseMail(primitive, params):
    match primitive:
        case 0x4003:
            print("API_FP_GET_FW_VERSION_CFM received.")
            print(
                f"Version: {params[3]:02x}{params[2]:02x}{params[1]:02x}{params[0]:02x}"
            )
            print(
                f"Link Date: {params[7]:02}/{params[6]:02}/{params[5]:02} at {params[8]:02}:{params[9]:02}"
            )
            # Mode can be changed with an API_PROD_TEST_REQ command
            print(f"Dect mode: {params[10]}")
        case 0x5903:
            print("API_HAL_LED_CFM  received.")
            print("LEDs toggled.")
        case _:
            print("Unknown primitive: ", hex(primitive))
