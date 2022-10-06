from pynput.keyboard import Controller, Key
from time import sleep

k = Controller()

if __name__ == "__main__":
    sleep(2)
    for _ in range(10000):
        sleep(0.1)
        k.press(Key.down)
        k.release(Key.down)
        sleep(0.1)
        k.press(Key.up)
        k.release(Key.up)