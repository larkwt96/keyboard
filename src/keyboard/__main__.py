from . import KeyboardMidi, KeyboardPlayer, Player, KeySetBuilder


if __name__ == '__main__':
    keyboard = KeyboardMidi()
    player = Player()
    keys = KeySetBuilder().build()
    KeyboardPlayer(keyboard, player, keys).run()
