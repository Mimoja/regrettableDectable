from .Api import BaseCommand
from .Commands import Commands
from ctypes import c_uint8, c_uint16, c_uint32, Structure, ARRAY


def ApiProdTestReq(opcode: int, data: bytes):
    class ApiProdTestReqClass(BaseCommand):
        _fields_ = [
            ("Opcode", c_uint16),
            ("ParameterLength", c_uint16),
            ("Parameters", c_uint8 * len(data)),
        ]

        def __init__(self, opcode: int, data: bytes):
            self.Primitive = Commands.API_PROD_TEST_REQ
            self.Opcode = opcode
            self.ParameterLength = len(data)
            self.Parameters = (c_uint8 * len(data))(*data)

    return ApiProdTestReqClass(opcode, data)


def ApiProdTestCfm(opcode: int, data: bytes):
    class ApiProdTestCfmClass(BaseCommand):
        _fields_ = [
            ("Opcode", c_uint16),
            ("ParameterLength", c_uint16),
            ("Parameters", c_uint8 * len(data)),
        ]

        def __init__(self, opcode: int, data: bytes):
            self.Primitive = Commands.API_PROD_TEST_CFM
            self.Opcode = opcode
            self.ParameterLength = len(data)
            self.Parameters = data

    return ApiProdTestCfmClass(opcode, data)
