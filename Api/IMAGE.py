from ctypes import (
    c_uint8,
    c_uint32,
    c_ubyte,
)
from enum import IntEnum
from .Commands import Commands
from .Api import BaseCommand, RsStatusType, VariableSizeCommand


class ApiImageID(IntEnum):
    SYSTEM = 1 << 0
    COLA = 1 << 1
    FP = 1 << 2
    PP = 1 << 3
    ULP = 1 << 4


class ApiImageInfoReq(BaseCommand):

    _fields_ = [
        ("ImageIndex", c_uint8),
    ]

    def __init__(self, image: ApiImageID):
        self.Primitive = Commands.API_IMAGE_INFO_REQ
        self.ImageIndex = image


class ApiImageInfoCfm(VariableSizeCommand):

    _fields_ = [
        ("Status", c_uint8),
        ("ImageIndex", c_uint8),
        ("ImageId", c_uint32),
        ("DeviceId", c_uint32),
        ("LinkDate", c_uint8 * 5),
        ("NameLength", c_uint8),
        ("LabelLength", c_uint8),
        ("Data", c_ubyte * 1),
    ]

    def __init__(
        self,
        status: RsStatusType,
        image: ApiImageID,
        image_id: int,
        device_id: int,
        link_date: bytes,
        name_length: int,
        data: bytes,
    ):
        self.Primitive = Commands.API_IMAGE_INFO_CFM
        self.Status = status
        self.ImageIndex = image
        self.ImageId = image_id
        self.DeviceId = device_id
        self.LinkDate = (c_uint8 * 5)(*link_date)
        self.NameLength = name_length
        self.LabelLength = len(data)
        self.set_array(self.Data, (c_ubyte * len(data))(*data))

    def to_dict(self):
        rep = super().to_dict()
        data = rep["Data"]
        rep["LinkDate"] = BaseCommand.parseDate(self.LinkDate)
        rep["name"] = bytes(data[: self.NameLength]).decode("utf-8", errors="ignore")
        rep["label"] = bytes(
            data[self.NameLength : self.NameLength + self.LabelLength]
        ).decode("utf-8", errors="ignore")
        del rep["Data"]
        return rep


class ApiImageActivateReq(BaseCommand):

    _fields_ = [
        ("ImageIndex", c_uint8),  # Index of the image that should be activated.
        #         0xFF means no change in index i.e. only change
        #         COLA activationg.
        ("ActivateCola", c_uint8),  # Set true to activate Co-Located Application
        #         (COLA) for the ImageIndex specified.
    ]

    def __init__(self, image: ApiImageID, activate_cola: bool):
        self.Primitive = Commands.API_IMAGE_ACTIVATE_REQ
        self.ImageIndex = image
        self.ActivateCola = 1 if activate_cola else 0


class ApiImageActivateCfm(BaseCommand):

    _fields_ = [
        ("Status", c_uint8),
    ]

    def __init__(self, status: RsStatusType):
        self.Status = status
