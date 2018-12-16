# Keyboard

This package is a frequency tone generator. It's fairly customizable if you use
the modules; otherwise, you can just use the cli.

## Install

```
python3 -m pip install .
```

or

```
python3 -m pip install git+git://github.com/larkwt96/keyboard.git
```

To install it without cloning. Additionally, you can update the package with

```
python3 -m pip install --upgrade keyboard
```

## Using

### Play notes with midi input

```
python3 -m keyboard keyboard
```

### Play notes and intervals.

```
python3 -m keyboard note --help
```

#### Examples:

Play A440 for 2 seconds
```
python3 -m keyboard note --no-fade-note --duration 2000 A4
```

Play C4 with exact minor third frequency ratio
```
python3 -m keyboard note --play-major-third --play-fifth C4
```
or..
```
python3 -m keyboard note -35 C4
```
It plays actual frequencies: 440 + 440x5:4 + 440x3:2.
Equal temperament C4-E4-G4 are slightly different.

Play C4 minor chord
```
python3 -m keyboard note -25 C4
```

Play slightly out of key chord progression: I-V-VI-IV
```
python3 -m keyboard note -35 C4 G4 A4 F4
```

Play chord with own ratios
```
python3 -m keyboard note -r 6 7 -r 5 2 C4
```

Play 2:3 ratio, down a fifth, from E5 resulting in A4 with frequency 439.503
```
python3 -m keyboard note a4
python3 -m keyboard note --no-play-note -r 2 3 e5
```

Play with different frequency standards
```
python3 -m keyboard note --root-note A4 --root-freq 435 -35 C4
```

Play G7 chord for 1500 milliseconds
```
python3 -m keyboard note -58 G4 --duration 1500
```

Play the same note three different ways
```
python3 -m keyboard note cb4 B3 a#s3
```
