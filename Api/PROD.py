from .Api import BaseCommand, VariableSizeCommand
from .Commands import Commands
from ctypes import c_uint8, c_uint16, c_uint32, Structure, ARRAY
from enum import IntEnum


class DectMode(IntEnum):
    EU = 0
    US = 1
    SA = 2
    Taiwan = 3
    Malaysia = 4
    China = 5
    Thailand = 6
    Brazil = 7
    US_Extended = 8
    Korea = 9
    Japan_2ch = 10
    Japan_5ch = 11


class ApiProdTestReq(VariableSizeCommand):
    _pack_ = 1
    _fields_ = [
        ("Opcode", c_uint16),
        ("ParameterLength", c_uint16),
        ("Parameters", c_uint8 * 1),
    ]

    def __init__(self, opcode: int, data: bytes = []):
        self.Primitive = Commands.API_PROD_TEST_REQ
        self.Opcode = opcode
        self.ParameterLength = len(data) & 0xFF
        self.set_array(self.Parameters, (c_uint8 * len(data))(*data))


class ApiProdTestCfm(VariableSizeCommand):
    _fields_ = [
        ("Opcode", c_uint16),
        ("ParameterLength", c_uint16),
        ("Parameters", c_uint8 * 1),
    ]

    def __init__(self, opcode: int, data: bytes):
        self.Primitive = Commands.API_PROD_TEST_CFM
        self.Opcode = opcode
        self.ParameterLength = len(data)
        self.set_array(self.Parameters, data)

    def getParameters(self):
        return self.to_bytes()[2 + 2 + 2 :]
