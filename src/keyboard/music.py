import re


class KeySetBuilder:
    def __init__(self,
                 root=440,
                 root_index=48,
                 num_keys=88,
                 keys_per_octave=12):
        self.root = root
        self.root_index = root_index
        self.num_keys = num_keys
        self.keys_per_octave = keys_per_octave

    def build_keys(self):
        return [self.get_freq(i) for i in range(self.num_keys)]

    def get_freq(self, key):
        steps = (key-self.root_index)/self.keys_per_octave
        ratio = 2**steps
        return self.root * ratio

    def build(self):
        return KeySet(self, True)


class KeySet:
    standard = []

    def __init__(self, builder=None, build=True):
        self.keys = None
        self.builder = builder

        if builder is None:
            self.keys = KeySet.standard
        elif build:
            self.keys = builder.build_keys()

    def get_freq(self, key):
        if self.keys is None:
            return self.builder.get_freq(key)
        else:
            return self.keys[key]


class Note:
    # primary symbols
    SHARP = '♯'
    DOUBLE_SHARP = '𝄪'
    NATURAL = '♮'
    FLAT = '♭'

    # groups
    SHARPS = 'sS#' + SHARP
    DOUBLE_SHARPS = 'xX' + DOUBLE_SHARP
    NATURALS = 'nN' + NATURAL
    FLATS = 'bB' + FLAT

    # symbol values
    NOTE_VALUES = {
        'C': 0,
        'D': 2,
        'E': 4,
        'F': 5,
        'G': 7,
        'A': 9,
        'B': 11,
    }
    ACCIDENTAL_VALUES = {
        DOUBLE_SHARP: 2,
        SHARP: 1,
        NATURAL: 0,
        FLAT: -1,
    }

    def __init__(self, note, use_flats=False):
        self.use_flats = use_flats
        if isinstance(note, str):
            self.note = self.parse_note(note)
            self.key = self.calc_key()
        elif isinstance(note, int):
            self.key = note
            self.note = self.calc_note()
        else:
            raise TypeError("Expected str or int, not {}.".format(type(note)))

    def __str__(self):
        return '{}{}{}'.format(*self.note)

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, str(self))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Note):
            return False
        return self.key == o.key

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def get_note(self):
        return self.note

    def get_key(self):
        return self.key

    def parse_note(self, note):
        letter, accidentals, octave = self.parse_note_groups(note)
        letter = letter.upper()
        accidentals = self.reformat_accidentals(accidentals)
        return letter, accidentals, octave

    @staticmethod
    def parse_note_groups(note):
        note_regex = '([A-Ga-g])([{}]*)([-]?[0-9]+)'
        accidentals = Note.SHARPS + Note.DOUBLE_SHARPS + Note.NATURALS + Note.FLATS
        note_regex = note_regex.format(accidentals)
        m = re.search(note_regex, note)
        if m is None:
            raise ValueError("Invalid note format: {}".format(note))
        return m.groups()

    @staticmethod
    def replace_any(value, old_set, new):
        for old in old_set:
            value = value.replace(old, new)
        return value

    def reformat_accidentals(self, accidentals):
        accidentals = self.replace_any(accidentals, Note.SHARPS, Note.SHARP)
        accidentals = self.replace_any(accidentals, Note.DOUBLE_SHARPS, Note.DOUBLE_SHARP)
        accidentals = self.replace_any(accidentals, Note.FLATS, Note.FLAT)
        accidentals = self.replace_any(accidentals, Note.NATURALS, Note.NATURAL)
        value = 0
        for accidental in accidentals:
            value += Note.ACCIDENTAL_VALUES[accidental]
        return self.value_to_accidental(value)

    @staticmethod
    def value_to_accidental(value):
        if value < 0:
            return Note.FLAT*(-value)
        elif value == 0:
            return ''
        else:
            return Note.DOUBLE_SHARP*(value // 2) + Note.SHARP*(value % 2)

    def calc_key(self):
        note, accidentals, octave = self.note
        value = Note.NOTE_VALUES[note]  # get note value
        for accidental in accidentals:
            value += Note.ACCIDENTAL_VALUES[accidental]  # add accidentals
        value -= 9  # adjust for A0
        value += 12*int(octave)  # add octave shift
        return value

    def simplify_note(self, use_flats=None):
        if use_flats is None:
            use_flats = self.use_flats
        self.note = self.calc_note(use_flats)

    def calc_note(self, use_flats=None):
        if use_flats is None:
            use_flats = self.use_flats
        value = self.key
        value += 9  # undo A0 adjustment
        octave = str(value // 12)
        value_to_note = {value: key for key, value in Note.NOTE_VALUES.items()}
        note_value = value % 12
        if note_value not in value_to_note:
            if use_flats:
                note = value_to_note[(note_value+1) % 12]
                accidental = Note.FLAT
            else:
                note = value_to_note[(note_value-1) % 12]
                accidental = Note.SHARP
        else:
            note = value_to_note[note_value]
            accidental = ''
        return note, accidental, octave
