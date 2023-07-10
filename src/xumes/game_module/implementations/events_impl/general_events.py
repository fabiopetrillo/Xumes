from pynput.keyboard import Key, Controller

from xumes.game_module.i_game_event import IGameEvent

keyboard = None


def get_keyboard():
    global keyboard
    if keyboard is None:
        keyboard = Controller()
    return keyboard


def key_down(key):
    get_keyboard().press(key)


def key_up(key):
    get_keyboard().release(key)


# noinspection DuplicatedCode
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
        key_down(key=Key.space)

    def release(self) -> None:
        key_up(key=Key.space)


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
