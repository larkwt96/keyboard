import numpy as np
import pygame
import pygame.sndarray


class PlayerNote:
    def __init__(self, note_id, duration, f, f_config):
        self.note_id = note_id
        self.duration = duration
        self.f = f
        self.f_config = f_config
        self.wave = None

    def get_duration(self):
        return self.duration

    def get_wave(self, x=None):
        if self.wave is None:
            self.wave = self.f(x, self.f_config)
        return self.wave

    def __hash__(self) -> int:
        return hash(self.note_id)


class PlayerBasicNote(PlayerNote):
    def __init__(self, note_id, frequency, volume, fade=True):
        super().__init__(note_id, 7, self.sin, (frequency, volume))
        self.fade = fade
        self.time_constant = .5

    def sin(self, x, config):
        frequency, volume = config
        volume = volume/127
        if self.fade:
            volume = volume * np.exp(-x/self.time_constant)
        return volume*np.sin(2*np.pi*frequency*x)


class Player:
    """
    This player is so that you can play notes.

    Each note has several configuration components:
        (id, duration, f(t, f_config), f_config)
    * id must be hashable
    * duration is in seconds and can be float
    * f_config should have a volume component

    The wave f(t, f_config) + {other playing notes} for t in [0, duration]
    is played. f should return [-1, 1] and will be multiplied by vol_max
    to [vol_min, vol_max] dropping extras.
    """

    def __init__(self, x_max=20):
        self.sample_rate, _, self.channels = pygame.mixer.get_init()
        vol_info = np.iinfo(np.int16)
        self.volume = .3
        self.vol_max = vol_info.max
        self.vol_min = vol_info.min
        self.x_max = x_max
        self.x = self.build_x()
        self.sound = None
        self.notes = {}

    def build_x(self):
        length = int(self.x_max*self.sample_rate)
        x = np.linspace(0, self.x_max, length, endpoint=True)
        x = x.repeat(self.channels).reshape(length, self.channels)
        x = np.ascontiguousarray(x)
        return x

    def sub_x(self, time):
        length = int(time*self.sample_rate)
        return self.x[:length, :]

    def build_wave(self, time):
        total_wave = None
        for note, note_time in self.notes.items():
            if note_time is None:
                continue
            wave = note.get_wave()
            delta_t = (time - note_time)/1000  # seconds after
            current_pos = int(delta_t * self.sample_rate)
            if current_pos >= wave.shape[0]:
                continue
            length = wave[current_pos:, :].shape[0]
            if total_wave is None:
                total_wave = np.zeros(wave.shape)
            total_wave[:length, :] += wave[current_pos:, :]
        if total_wave is not None:
            total_wave *= self.vol_max*self.volume
            total_wave[total_wave > self.vol_max] = self.vol_max
            total_wave[total_wave < self.vol_min] = self.vol_min
        return total_wave

    def build_sound(self, time):
        wave = self.build_wave(time)
        if wave is None:
            return
        else:
            wave = wave.astype(np.int16)
        self.sound = pygame.sndarray.make_sound(wave)

    def play(self, note, time=None):
        if time is None:
            time = pygame.time.get_ticks()
        note.get_wave(self.sub_x(note.get_duration()))
        self.notes[note] = time
        self.render(time)

    def play_all(self, notes, times=None):
        if times is None:
            curr_time = pygame.time.get_ticks()
            times = [curr_time for _ in notes]
        for note, time in zip(notes, times):
            note.get_wave(self.sub_x(note.get_duration()))
            self.notes[note] = time
        if len(notes) > 0:
            self.render(pygame.time.get_ticks())

    def stop(self, note):
        self.notes[note] = None
        self.render(pygame.time.get_ticks())

    def stop_all(self, notes):
        for note in notes:
            self.notes[note] = None
        if len(notes) > 0:
            self.render(pygame.time.get_ticks())

    def render(self, time):
        old_sound = self.sound
        self.build_sound(time)
        if self.sound is not None:
            self.sound.play()
        if old_sound is not None:
            old_sound.stop()

    @staticmethod
    def delay(ms):
        pygame.time.delay(ms)


class KeyboardPlayer:
    def __init__(self, keyboard, player, generator):
        self.keyboard = keyboard
        self.player = player
        self.generator = generator
        self.playing = {}

    def update(self, keyboard):
        keep = set()
        to_play = set()
        for key, values in keyboard.keys.items():
            if values is None:
                continue
            for value in values:
                freq = self.generator.get_freq(key)
                volume, time = value
                note_id = (freq, volume, time)
                keep.add(note_id)
                if note_id not in self.playing:
                    note = PlayerBasicNote(note_id, freq, volume)
                    self.playing[note_id] = note
                    to_play.add((note, time))
        notes = [note for note, time in to_play]
        times = [time for note, time in to_play]
        self.player.play_all(notes, times)

        to_stop = []
        for note_id in self.playing.copy():
            if note_id not in keep:
                note = self.playing[note_id]
                to_stop.append(note)
                del self.playing[note_id]
        self.player.stop_all(to_stop)

    def run(self):
        self.keyboard.watch(self)
        try:
            self.keyboard.listen()
        except IOError as err:
            print(err)
        except KeyboardInterrupt:
            print("Exiting.")


