import unittest

import keyboard


class TestModel(unittest.TestCase):
    def setUp(self):
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    def test_simplify_note_sharps_override(self):
        cb = keyboard.Note('C#4', use_flats=True)
        cb.simplify_note(use_flats=False)
        b = keyboard.Note('Db4')
        self.assertEqual(cb, b)
        self.assertNotEqual(cb.get_note(), b.get_note())

    def test_simplify_note_sharps(self):
        cb = keyboard.Note('C#4', use_flats=True)
        cb.simplify_note()
        b = keyboard.Note('Db4')
        self.assertEqual(cb, b)
        self.assertEqual(cb.get_note(), b.get_note())

    def test_simplify_note_sharps_default(self):
        cb = keyboard.Note('C#4')
        cb.simplify_note(use_flats=True)
        b = keyboard.Note('Db4')
        self.assertEqual(cb, b)
        self.assertEqual(cb.get_note(), b.get_note())

    def test_simplify_note_flats(self):
        cb = keyboard.Note('C#4')
        b = keyboard.Note('Db4')
        b.simplify_note()
        self.assertEqual(cb, b)
        self.assertEqual(cb.get_note(), b.get_note())

    def test_simplify_note_flats_extra_simple(self):
        cb = keyboard.Note('C#4')
        cb.simplify_note()
        b = keyboard.Note('Db4')
        b.simplify_note()
        self.assertEqual(cb, b)
        self.assertEqual(cb.get_note(), b.get_note())

    def test_simplify_note(self):
        cb = keyboard.Note('Cb4')
        cb.simplify_note()
        b = keyboard.Note('B3')
        self.assertEqual(cb, b)
        self.assertEqual(cb.get_note(), b.get_note())

    def test_super_simplify(self):
        cb = keyboard.Note('Cb4')
        cb_key = keyboard.Note(cb.get_key())
        b = keyboard.Note('B3')
        self.assertEqual(cb, cb_key)
        self.assertEqual(b, cb_key)
        self.assertEqual(cb_key.get_note(), b.get_note())
        self.assertNotEqual(cb.get_note(), cb_key.get_note())

    def test_note(self):
        note = keyboard.Note('C4')
        self.assertEqual(str(note), 'C4')
        self.assertEqual(note.__repr__(), "Note('C4')")
        self.assertEqual(note.get_key(), 39)

    def test_str(self):
        note = keyboard.Note('C4')
        self.assertEqual(str(note), 'C4')
        self.assertEqual(note.__repr__(), "{}('C4')".format(note.__class__.__name__))

    def test_repr(self):
        note = keyboard.Note('G###nn-2')
        Note = keyboard.Note
        note_copy = eval(repr(note))
        self.assertEqual(note, note_copy)
        self.assertEqual(note.get_note(), note_copy.get_note())

    def test_lower(self):
        for l in self.letters:
            noteu = keyboard.Note(l.upper()+'4')
            notel = keyboard.Note(l.lower()+'4')
            self.assertEqual(noteu, notel)

    def test_eq(self):
        note1 = keyboard.Note('C#4')
        note2 = keyboard.Note('Db4')
        self.assertEqual(note1, note2)
        self.assertNotEqual(note1.get_note(), note2.get_note())
        self.assertEqual(note1.get_key(), note2.get_key())

    def test_key(self):
        note = keyboard.Note('C4')
        self.assertEqual(note.get_key(), 39)
        note = keyboard.Note('A0')
        self.assertEqual(note.get_key(), 0)
        note = keyboard.Note('C#4')
        self.assertEqual(note.get_note()[1], keyboard.Note.SHARP)
        self.assertEqual(note.get_key(), 40)

    def test_int_build(self):
        for i in [2, 0, -12, -1, 12, 23, 25, 9]:
            note = keyboard.Note(i)
            self.assertEqual(note.calc_key(), i)

    def test_bad_input(self):
        self.assertRaises(ValueError, lambda: keyboard.Note('C'))
        self.assertRaises(TypeError, lambda: keyboard.Note({'C'}))

    def test_negative_octave(self):
        note = keyboard.Note('C###-2')
        self.assertEqual(note.get_note()[2], '-2')

    def test_simplify(self):
        values = {
            "####": keyboard.Note.DOUBLE_SHARP*2,
            "s###": keyboard.Note.DOUBLE_SHARP*2,
            "#S###b": keyboard.Note.DOUBLE_SHARP*2,
            "#S###bbbbbbb": keyboard.Note.FLAT*2,
            "#S##b": keyboard.Note.DOUBLE_SHARP+keyboard.Note.SHARP,
            "xbbnnn": '',
        }
        for s in keyboard.Note.DOUBLE_SHARPS:
            values[s] = keyboard.Note.DOUBLE_SHARP
        for s in keyboard.Note.SHARPS:
            values[s] = keyboard.Note.SHARP
        for s in keyboard.Note.FLAT:
            values[s] = keyboard.Note.FLAT
        for s in keyboard.Note.NATURALS:
            values[s] = ''

        for value, expected in values.items():
            note = keyboard.Note('C{}4'.format(value))
            accidental = note.get_note()[1]
            self.assertEqual(accidental, expected)
