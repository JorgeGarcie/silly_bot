import math

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def freq_to_note(freq: float) -> str | None:
    if freq <= 0:
        return None
    midi = round(12 * math.log2(freq / 440.0)) + 69
    if midi < 0 or midi > 127:
        return None
    return f"{NOTE_NAMES[midi % 12]}{midi // 12 - 1}"
