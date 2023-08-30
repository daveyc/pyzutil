import ctypes
import pathlib
from ctypes import *

# load the shared lib
lib_file = pathlib.Path(__file__).parent / "libpyzutil.so"
lib = ctypes.CDLL(str(lib_file))

# set the function prototypes
lib.pyzutil_stck.argtypes = [c_char_p, c_size_t]
lib.pyzutil_stck.restype = c_int

lib.pyzutil_stcke.argtypes = [c_char_p, c_size_t]
lib.pyzutil_stcke.restype = c_int

lib.pyzutil_time_used.restype = c_ulonglong

lib.pyzutil_time.restype = c_int

lib.pyzutil_clock.restype = c_double

lib.pzutil_storage.argtypes = [c_ulonglong, c_char_p, c_size_t]
lib.pzutil_storage.restype = c_bool


# functions
def storage(addr: int, stck_size: int) -> bytes:
    buffer = ctypes.create_string_buffer(stck_size)
    ret = lib.pzutil_storage(addr, buffer, len(buffer))
    assert ret is True
    return buffer.raw


def stck() -> bytes:
    """
    Returns a STCK TOD unit

    :return: a STCK TOD unit as a byte string
    """
    stck_size = 8
    buffer = ctypes.create_string_buffer(stck_size)
    rc = lib.pyzutil_stck(buffer, len(buffer))
    assert rc == 0
    return buffer.raw


def stcke() -> bytes:
    """
    Returns a STCKE TOD unit

    :return: a STCKE TOD unit as a byte string
    """
    stcke_size = 16
    buffer = ctypes.create_string_buffer(stcke_size)
    rc = lib.pyzutil_stcke(buffer, len(buffer))
    assert rc == 0
    return buffer.raw


def time_used() -> float:
    return float(lib.pyzutil_time_used() / 1000000)


def time() -> int:
    return lib.pyzutil_time()


def clock() -> float:
    return lib.pyzutil_clock()
