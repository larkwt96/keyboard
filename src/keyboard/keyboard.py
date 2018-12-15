import sys
import os

with open(os.devnull, 'w') as devnull:
    sys.stdout = devnull
    sys.stderr = devnull
    import pygame
    import pygame.midi
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


class Keyboard:
    def __init__(self, verbose=False, wait_time=10):
        self.input = None
        self.listening = False
        self.dev = None
        self.keys = {}
        self.sustain = None
        self.verbose = verbose
        self.wait_time = wait_time
        self.observers = set()

        pygame.init()
        pygame.midi.init()
        pygame.fastevent.init()

    def check_dev(self):
        if self.dev == -1:
            raise IOError("No Midi device found")

    def listen(self):
        self.listening = True
        self.dev = pygame.midi.get_default_input_id()
        self.check_dev()
        self.input = pygame.midi.Input(self.dev)
        try:
            self.loop()
        except KeyboardInterrupt:
            self.input.close()
            raise

    def loop(self):
        while self.listening:
            if self.input.poll():
                midi_events = self.input.read(10)
                for e in midi_events:
                    self.handle_event(e)
            self.update()
            if self.wait_time is not None:
                pygame.time.wait(self.wait_time)

    def update(self):
        for observer in self.observers:
            observer.update(self)

    def handle_event(self, event):
        [[status, key, velocity, _], time] = event
        if status == 144:
            self.press(key-21, velocity, time)
        elif status == 128:
            self.release(key-21)
        elif status == 176 or status == 177:
            if velocity == 127:
                self.press_sustain()
            else:
                self.release_sustain()
        else:
            raise Exception("Unknown Status: {}".format(status))

    def stop_listening(self):
        self.listening = False

    def is_pressed(self, key):
        return self.keys.get(key, False)

    def press_sustain(self):
        if self.sustain is not None:
            return
        self.sustain = {}

    def release_sustain(self):
        if self.sustain is None:
            return
        for key, value in self.sustain.items():
            if value:
                self.keys[key] = []
        self.sustain = None

    def press(self, key, velocity, time):
        if self.sustain is not None:
            self.sustain[key] = False
        if key not in self.keys:
            self.keys[key] = []
        self.keys[key].append((velocity, time))

    def release(self, key):
        if self.sustain is not None:
            self.sustain[key] = True
        else:
            self.keys[key] = []

    def watch(self, observer):
        self.observers.add(observer)

    def __del__(self):
        pygame.midi.quit()
        pygame.quit()
