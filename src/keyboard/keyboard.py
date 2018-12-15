import pygame
import pygame.midi


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
            self.keys = standard
        elif build:
            self.keys = builder.build_keys()

    def get_freq(self, key):
        if self.keys is None:
            return self.builder.get_freq(key)
        else:
            return self.keys[key]


class Keyboard:
    def __init__(self, verbose=False, wait_time=10):
        pygame.init()
        pygame.midi.init()
        pygame.fastevent.init()
        self.listening = False
        self.dev = pygame.midi.get_default_input_id()
        self.check_dev()
        self.keys = {}
        self.sustain = None
        self.verbose = verbose
        self.input = pygame.midi.Input(self.dev)
        self.wait_time = wait_time
        self.observers = set()

    def check_dev(self):
        if self.dev != -1:
            raise Exception("No Midi device found")

    def listen(self):
        self.listening = True
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
        [[status, key, velocity, data3], time] = event
        #msg = "status: {}, key: {}, vel: {}, data3: {}, time: {}"
        #print(msg.format(status, key, velocity, data3, time))
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
            print('key, value = {}, {}'.format(key, value))
            if value:
                self.keys[key] = None
        self.sustain = None

    def press(self, key, velocity, time):
        if self.verbose:
            print('pressed {}'.format(key))
        if self.sustain is not None:
            self.sustain[key] = False
        self.keys[key] = (velocity, time)

    def release(self, key):
        if self.verbose:
            print('pressed {}'.format(key))
        if self.sustain is not None:
            self.sustain[key] = True
        else:
            self.keys[key] = None

    def watch(self, observer):
        self.observers.add(observer)

    def __del__(self):
        pygame.midi.quit()
