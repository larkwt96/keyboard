import click
from . import KeyboardMidi, KeyboardPlayer, Player, KeySetBuilder, Note, PlayerBasicNote


@click.group()
def main():
    pass


@main.command()
def keyboard():
    keyboard_midi = KeyboardMidi()
    player = Player()
    keys = KeySetBuilder().build()
    KeyboardPlayer(keyboard_midi, player, keys).run()


@main.command()
@click.argument('notes', type=str, nargs=-1)
@click.option('--fade-note/--no-fade-note', default=True,
              help='Fade the note with time')
@click.option('--play-note/--no-play-note', default=True,
              help='Play the main note. Defaults to True.')
@click.option('--play-minor-third', '-2', is_flag=True,
              help='Play the minor third (6:5).')
@click.option('--play-major-third', '-3', is_flag=True,
              help='Play the major third (5:4).')
@click.option('--play-fourth', '-4', is_flag=True,
              help='Play the fourth (4:3).')
@click.option('--play-fifth', '-5', is_flag=True,
              help='Play the fifth (3:2).')
@click.option('--play-octave', '-8', is_flag=True,
              help='Play an octave (2:1).')
@click.option('--play-ratio', '-r', type=(int, int), multiple=True,
              help='Play an arbitrary ratio.')
@click.option('--duration', '-t', type=int, default=1000,
              help='Duration to play note, in milliseconds.')
@click.option('--play-separate', '-s', is_flag=True,
              help='Play sequence of notes and their intervals separately.')
@click.option('--play-chord/--no-play-chord', default=True, is_flag=True,
              help="Play sequence of notes as a chord. Defaults to True.")
@click.option('--root-note', '-r', type=str, default="A4",
              help='The primary note to base tuning. Defaults to A4.')
@click.option('--root-freq', '-f', type=float, default=440,
              help='The frequency of the primary note. Defaults to 440.')
def note(notes, root_note, root_freq, play_note, play_minor_third,
         play_major_third, play_fourth, play_fifth, play_octave, play_ratio,
         duration, play_separate, play_chord, fade_note):
    """
    Play notes and intervals.
    """
    try:
        root_note = Note(root_note)
    except (ValueError, TypeError) as err:
        print('Error:', err)
        return
    parsed_notes = []
    for _note in notes:
        try:
            _note = Note(_note)
        except (ValueError, TypeError) as err:
            print('Error:', err)
            return
        parsed_notes.append(_note)
    keyset = KeySetBuilder(root_freq, root_note.get_key()).build()

    for _note in parsed_notes:
        freq = keyset.get_freq(_note.get_key())
        to_play = []
        if play_note:
            to_play.append(freq)
        if play_minor_third:
            to_play.append(freq*6/5)
        if play_major_third:
            to_play.append(freq*5/4)
        if play_fourth:
            to_play.append(freq*4/3)
        if play_fifth:
            to_play.append(freq*3/2)
        if play_octave:
            to_play.append(freq*2)
        for ratio in play_ratio:
            to_play.append(freq*ratio[0]/ratio[1])

        play(_note, freq, to_play, duration, play_separate, play_chord, fade_note)


def play(curr_note, base_freq, to_play, duration, play_separate, play_chord, fade_note):
    print('Base note: {} at {} hz'.format(curr_note, base_freq))
    print('Playing:')
    volume = 127
    for freq in to_play:
        print('{} hz ({} ratio)'.format(freq, freq/base_freq))
    print()
    player = Player()
    if play_separate:
        for freq in to_play:
            _note = PlayerBasicNote((freq, 0), freq, volume, fade=fade_note)
            player.play(_note)
            player.delay(duration)
            player.stop(_note)
    if play_chord:
        notes = []
        for freq in to_play:
            notes.append(PlayerBasicNote((freq, 1), freq, volume, fade=fade_note))
        player.play_all(notes)
        player.delay(duration)
        player.stop_all(notes)


if __name__ == '__main__':
    main()
