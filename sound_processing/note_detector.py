import re
import serial

from sound_processing.semitone import freq_to_note

LINE_RE = re.compile(r"F0:\s*([\d.]+)\s*Hz")
STABLE_FRAMES = 3
MIN_FREQ = 80.0


def stream_notes(port: str, baud: int = 115200):
    """Yield note names as they're detected (debounced, change-triggered)."""
    ser = serial.Serial(port, baud, timeout=1)
    last_emitted = None
    candidate = None
    candidate_count = 0

    while True:
        line = ser.readline().decode(errors="ignore").strip()
        m = LINE_RE.search(line)
        if not m:
            continue
        freq = float(m.group(1))
        if freq < MIN_FREQ:
            note = None
        else:
            note = freq_to_note(freq)

        if note == candidate:
            candidate_count += 1
        else:
            candidate = note
            candidate_count = 1

        if candidate_count == STABLE_FRAMES and candidate != last_emitted:
            last_emitted = candidate
            if candidate is not None:
                yield candidate
