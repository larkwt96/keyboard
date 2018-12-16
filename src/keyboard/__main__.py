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
              help='Dampen the note with time.')
@click.option('--play-note/--no-play-note', default=True,
              help='Specify whether or not to play current note. True by default.')
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
              help="Specify an arbitrary ratio. '--play-ratio 5 4' will play "
                   "{note frequency}*5/4. You can specify as many as these as "
                   "you want.")
@click.option('--duration', '-t', type=int, default=1000,
              help='Specify the number of milliseconds to play the notes and chords.')
@click.option('--play-separate', '-s', is_flag=True,
              help='Play each note separately. Can be specified with play_chord. False by default.')
@click.option('--play-chord/--no-play-chord', default=True, is_flag=True,
              help="Play each note as a chord. Can be specified with play_separate. True by default.")
@click.option('--root-note', '-n', type=str, default="A4",
              help='Specify which note to set the frequency on. A4 by default.')
@click.option('--root-freq', '-f', type=float, default=440,
              help='Specify what frequency to set for the root note. 440 by default.')
def note(notes, root_note, root_freq, play_note, play_minor_third,
         play_major_third, play_fourth, play_fifth, play_octave, play_ratio,
         duration, play_separate, play_chord, fade_note):
    """
    This command will play notes and specified intervals.

    Notes are in the format of Note, accidental and octave. It's case
    insensitive and no spaces. Notes are A-G or a-g.

    \b
    Accidentals are any of the following:
    - s, S, #, or ♯ will be considered as a sharp
    - x, X, ## or 𝄪 will be considered as a double sharp
    - nothing, n, N, or ♮ will be considered as a natural
    - b, B, and ♭ will be considered as a flat
    - Two adjacent flats will be considered a double flat.

    \b
    For example,
    - Cs4 cS4 c#4 will all be C4.
    - C##4 will be C double-sharp 4th octave

    \b
    Accidentals are simplified as much as possible. For example,
    - csssssbbbbx5 will simplify to C𝄪♯5 since there are 3 more sharps than flats.
    - cssbbb4 will simplify to C♭4, but not B3. However, the note that plays will technically be B3.

    \b
    Arguments:
    - notes: It will play these notes. Specify as many as you want.
    - root_note: Specify which note to set the frequency on. A4 by default.
    - root_freq: Specify what frequency to set for the root note. 440 by default.
    - play_note: Specify whether or not to play current note. True by default.
    - play_minor_third: Specify whether to play minor third. False by default.
    - play_major_third: Specify whether to play major third. False by default.
    - play_fourth: Specify whether to play fourth. False by default.
    - play_fifth: Specify whether to play fifth. False by default.
    - play_octave: Specify whether to play octave. False by default.
    - play_ratio: Specify an arbitrary ratio. '--play-ratio 5 4' will play {note frequency}*5/4. You can specify as many as these as you want.
    - duration: Specify the number of milliseconds to play the notes and chords.
    - play_separate: Play each note separately. Can be specified with play_chord. False by default.
    - play_chord: Play each note as a chord. Can be specified with play_separate. True by default.
    - fade_note: Dampen the note with time.
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
