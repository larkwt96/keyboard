import keyboard

class Player:
    def __init__(self):
        self.keyboard = keyboard.Keyboard()

    def update(self, keyboard):
        print('update')
        for key, value in keyboard.keys.items():
            if value is not None:
                print('key: {}, velocity: {}, time: {}'.format(key, *value))

    def run(self):
        self.keyboard.watch(self)
        self.keyboard.listen()

