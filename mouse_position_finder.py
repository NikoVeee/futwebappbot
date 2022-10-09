from time import sleep
from pynput.mouse import Controller

def find_mouse_position(mouse):
    while True:
        sleep(1)
        print(mouse.position)

if __name__ == "__main__":
    mouse = Controller()
    find_mouse_position(mouse)