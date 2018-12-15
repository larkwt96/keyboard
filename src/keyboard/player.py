from .keyboard import Keyboard
from .tuner import Note


class Player:
    def __init__(self, keyboard=None):
        self.keyboard = keyboard
        if self.keyboard is None:
            self.keyboard = Keyboard()

    def update(self, keyboard=None, data=None):
        if keyboard is None:
            keyboard = self.keyboard
        if data is not None:
            print(data)
        found = False
        for key, values in keyboard.keys.items():
            if values is not None:
                for value in values:
                    found = True
                    print('({} / {} at {})'.format(Note(key), *value))
        if found:
            print()

    def run(self):
        self.keyboard.watch(self)
        try:
            self.keyboard.listen()
        except IOError as err:
            print(err)
        except KeyboardInterrupt:
            print("Exiting.")
