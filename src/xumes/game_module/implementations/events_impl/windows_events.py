import ctypes
from ctypes import wintypes

from xumes.game_module.i_game_event import IGameEvent

user32 = ctypes.WinDLL('user32', use_last_error=True)
INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
MAPVK_VK_TO_VSC = 0
# msdn.microsoft.com/en-us/library/dd375731
wintypes.ULONG_PTR = wintypes.WPARAM


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))

    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD),
                ("_input", _INPUT))


LPINPUT = ctypes.POINTER(INPUT)


def press_key(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def release_key(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def key_down(key):
    press_key(to_key_code(key))


def key_up(key):
    release_key(to_key_code(key))


def to_key_code(c):
    key_code = key_code_map[c[0]]
    return int(key_code, base=16)


key_code_map = {
    'shift': "0x10",
    '0': "0x30",
    '1': "0x31",
    '2': "0x32",
    '3': "0x33",
    '4': "0x34",
    '5': "0x35",
    '6': "0x36",
    '7': "0x37",
    '8': "0x38",
    '9': "0x39",
    'a': "0x41",
    'b': "0x42",
    'c': "0x43",
    'd': "0x44",
    'e': "0x45",
    'f': "0x46",
    'g': "0x47",
    'h': "0x48",
    'i': "0x49",
    'j': "0x4A",
    'k': "0x4B",
    'l': "0x4C",
    'm': "0x4D",
    'n': "0x4E",
    'o': "0x4F",
    'p': "0x50",
    'q': "0x51",
    'r': "0x52",
    's': "0x53",
    't': "0x54",
    'u': "0x55",
    'v': "0x56",
    'w': "0x57",
    'x': "0x58",
    'y': "0x59",
    'z': "0x5A",
    'enter': "0x0D",
    'esc': "0x1B",
    'space': "0x20",
    'left': "0x25",
    'up': "0x26",
    'right': "0x27",
    'down': "0x28",

}


class Up(IGameEvent):

    def press(self) -> None:
        key_down(key='up')

    def release(self) -> None:
        key_up(key='up')


class Down(IGameEvent):
    def press(self) -> None:
        key_down(key='down')

    def release(self) -> None:
        key_up(key='down')


class Left(IGameEvent):
    def press(self) -> None:
        key_down(key='left')

    def release(self) -> None:
        key_up(key='left')


class Right(IGameEvent):
    def press(self) -> None:
        key_down(key='right')

    def release(self) -> None:
        key_up(key='right')


class Space(IGameEvent):
    def press(self) -> None:
        key_down(key='space')

    def release(self) -> None:
        key_up(key='space')


class KeyA(IGameEvent):
    def press(self) -> None:
        key_down(key='a')

    def release(self) -> None:
        key_up(key='a')


class KeyB(IGameEvent):
    def press(self) -> None:
        key_down(key='b')

    def release(self) -> None:
        key_up(key='b')


class KeyC(IGameEvent):
    def press(self) -> None:
        key_down(key='c')

    def release(self) -> None:
        key_up(key='c')


class KeyD(IGameEvent):
    def press(self) -> None:
        key_down(key='d')

    def release(self) -> None:
        key_up(key='d')


class KeyE(IGameEvent):
    def press(self) -> None:
        key_down(key='e')

    def release(self) -> None:
        key_up(key='e')


class KeyF(IGameEvent):
    def press(self) -> None:
        key_down(key='f')

    def release(self) -> None:
        key_up(key='f')


class KeyG(IGameEvent):
    def press(self) -> None:
        key_down(key='g')

    def release(self) -> None:
        key_up(key='g')


class KeyH(IGameEvent):
    def press(self) -> None:
        key_down(key='h')

    def release(self) -> None:
        key_up(key='h')


class KeyI(IGameEvent):
    def press(self) -> None:
        key_down(key='i')

    def release(self) -> None:
        key_up(key='i')


class KeyJ(IGameEvent):
    def press(self) -> None:
        key_down(key='j')

    def release(self) -> None:
        key_up(key='j')


class KeyK(IGameEvent):
    def press(self) -> None:
        key_down(key='k')

    def release(self) -> None:
        key_up(key='k')


class KeyL(IGameEvent):
    def press(self) -> None:
        key_down(key='l')

    def release(self) -> None:
        key_up(key='l')


class KeyM(IGameEvent):
    def press(self) -> None:
        key_down(key='m')

    def release(self) -> None:
        key_up(key='m')


class KeyN(IGameEvent):
    def press(self) -> None:
        key_down(key='n')

    def release(self) -> None:
        key_up(key='n')


class KeyO(IGameEvent):
    def press(self) -> None:
        key_down(key='o')

    def release(self) -> None:
        key_up(key='o')


class KeyP(IGameEvent):
    def press(self) -> None:
        key_down(key='p')

    def release(self) -> None:
        key_up(key='p')


class KeyQ(IGameEvent):
    def press(self) -> None:
        key_down(key='q')

    def release(self) -> None:
        key_up(key='q')


class KeyR(IGameEvent):
    def press(self) -> None:
        key_down(key='r')

    def release(self) -> None:
        key_up(key='r')


class KeyS(IGameEvent):
    def press(self) -> None:
        key_down(key='s')

    def release(self) -> None:
        key_up(key='s')


class KeyT(IGameEvent):
    def press(self) -> None:
        key_down(key='t')

    def release(self) -> None:
        key_up(key='t')


class KeyU(IGameEvent):
    def press(self) -> None:
        key_down(key='u')

    def release(self) -> None:
        key_up(key='u')


class KeyV(IGameEvent):
    def press(self) -> None:
        key_down(key='v')

    def release(self) -> None:
        key_up(key='v')


class KeyW(IGameEvent):
    def press(self) -> None:
        key_down(key='w')

    def release(self) -> None:
        key_up(key='w')


class KeyX(IGameEvent):
    def press(self) -> None:
        key_down(key='x')

    def release(self) -> None:
        key_up(key='x')


class KeyY(IGameEvent):
    def press(self) -> None:
        key_down(key='y')

    def release(self) -> None:
        key_up(key='y')


class KeyZ(IGameEvent):
    def press(self) -> None:
        key_down(key='z')

    def release(self) -> None:
        key_up(key='z')


class Key0(IGameEvent):
    def press(self) -> None:
        key_down(key='0')

    def release(self) -> None:
        key_up(key='0')


class Key1(IGameEvent):
    def press(self) -> None:
        key_down(key='1')

    def release(self) -> None:
        key_up(key='1')


class Key2(IGameEvent):
    def press(self) -> None:
        key_down(key='2')

    def release(self) -> None:
        key_up(key='2')


class Key3(IGameEvent):
    def press(self) -> None:
        key_down(key='3')

    def release(self) -> None:
        key_up(key='3')


class Key4(IGameEvent):
    def press(self) -> None:
        key_down(key='4')

    def release(self) -> None:
        key_up(key='4')


class Key5(IGameEvent):
    def press(self) -> None:
        key_down(key='5')

    def release(self) -> None:
        key_up(key='5')


class Key6(IGameEvent):
    def press(self) -> None:
        key_down(key='6')

    def release(self) -> None:
        key_up(key='6')


class Key7(IGameEvent):
    def press(self) -> None:
        key_down(key='7')

    def release(self) -> None:
        key_up(key='7')


class Key8(IGameEvent):
    def press(self) -> None:
        key_down(key='8')

    def release(self) -> None:
        key_up(key='8')


class Key9(IGameEvent):
    def press(self) -> None:
        key_down(key='9')

    def release(self) -> None:
        key_up(key='9')


class Key0Pad(IGameEvent):
    def press(self) -> None:
        key_down(key='0pad')

    def release(self) -> None:
        key_up(key='0pad')


class Key1Pad(IGameEvent):
    def press(self) -> None:
        key_down(key='1pad')

    def release(self) -> None:
        key_up(key='1pad')


class Key2Pad(IGameEvent):
    def press(self) -> None:
        key_down(key='2pad')

    def release(self) -> None:
        key_up(key='2pad')


class Key3Pad(IGameEvent):
    def press(self) -> None:
        key_down(key='3pad')

    def release(self) -> None:
        key_up(key='3pad')


class Key4Pad(IGameEvent):
    def press(self) -> None:
        key_down(key='4pad')

    def release(self) -> None:
        key_up(key='4pad')


class Key5Pad(IGameEvent):
    def press(self) -> None:
        key_down(key='5pad')

    def release(self) -> None:
        key_up(key='5pad')


class Key6Pad(IGameEvent):
    def press(self) -> None:
        key_down(key='6pad')

    def release(self) -> None:
        key_up(key='6pad')


class Key7Pad(IGameEvent):
    def press(self) -> None:
        key_down(key='7pad')

    def release(self) -> None:
        key_up(key='7pad')


class Key8Pad(IGameEvent):
    def press(self) -> None:
        key_down(key='8pad')

    def release(self) -> None:
        key_up(key='8pad')


class Key9Pad(IGameEvent):
    def press(self) -> None:
        key_down(key='9pad')

    def release(self) -> None:
        key_up(key='9pad')
