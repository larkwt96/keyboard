import os
import unittest

import keyboard

class TestModel(unittest.TestCase):
    def setUp(self):
        self.builder = keyboard.KeySetBuilder()
        self.keyset = self.builder.build()

    def test_x(self):
        c4 = 3+12*3
        self.assertTrue(self.keyset.get_freq(c4) - 261.6 < 1)
        print(self.keyset.keys)
