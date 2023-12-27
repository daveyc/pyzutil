from pyzutil import *
import struct


# helper functions
def ptr32(addr: int, high_bit=False) -> int:
    (ptr,) = struct.unpack('>I', storage(addr, 4))
    return ptr if high_bit else ptr & 0x7FFFFFFF  # return ensuring the high order bit is not set


def ptr24(addr: int) -> int:
    (ptr,) = struct.unpack('>I', b'\x00' + storage(addr, 3))
    return ptr


def int8(addr: int) -> int:
    (ret,) = struct.unpack('>b', storage(addr, 1))
    return ret


def uint8(addr: int) -> int:
    (ret,) = struct.unpack('>B', storage(addr, 1))
    return ret


def int16(addr: int) -> int:
    (ret,) = struct.unpack('>h', storage(addr, 2))
    return ret


def uint16(addr: int) -> int:
    (ret,) = struct.unpack('>H', storage(addr, 2))
    return ret


def int32(addr: int) -> int:
    (ret,) = struct.unpack('>i', storage(addr, 4))
    return ret


def uint32(addr: int) -> int:
    (ret,) = struct.unpack('>I', storage(addr, 4))
    return ret


def int64(addr: int) -> int:
    (ret,) = struct.unpack('>q', storage(addr, 8))
    return ret


def uint64(addr: int) -> int:
    (ret,) = struct.unpack('>Q', storage(addr, 8))
    return ret


def string(addr: int, length: int, encoding='ibm037', rtrim=False) -> str:
    ret = str(storage(addr, length).decode(encoding))
    if rtrim:
        ret = ret.rstrip()
    return ret


def bytes(addr: int, length: int) -> bytes:
    return storage(addr, length)


def tcb() -> int:
    return ptr32(540)
