from .keyboard import KeyboardMidi
from .music import Note


class Player:
    def __init__(self, keyboard=None):
        self.keyboard = keyboard
        if self.keyboard is None:
            self.keyboard = KeyboardMidi()

    @staticmethod
    def update(keyboard):
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


if __name__ == '__main__':
    player = Player()
    player.run()
