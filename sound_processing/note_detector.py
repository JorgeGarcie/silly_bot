import re
import sys

import serial

try:
    from sound_processing.note_classifier import default_classifier
except ImportError:
    sys.path.insert(0, "..")
    from sound_processing.note_classifier import default_classifier

LINE_RE = re.compile(r"F0:\s*([\d.]+)\s*Hz")
STABLE_FRAMES = 3
MIN_FREQ = 80.0


def stream_notes(port: str, baud: int = 115200, classifier=default_classifier):
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
        note = classifier.classify(freq) if freq >= MIN_FREQ else None

        if note == candidate:
            candidate_count += 1
        else:
            candidate = note
            candidate_count = 1

        if candidate_count == STABLE_FRAMES and candidate != last_emitted:
            last_emitted = candidate
            if candidate is not None:
                yield candidate


if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else "COM3"
    print(f"listening on {port}")
    for note in stream_notes(port):
        print(f"[NOTE] {note}")
