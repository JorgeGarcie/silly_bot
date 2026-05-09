import sys

from motor_control.dispatcher import dispatch, reject
from motor_control.validator import Validator
from sound_processing.note_detector import stream_notes


def main():
    if len(sys.argv) < 2:
        print("usage: python app.py <serial_port>  e.g. COM3")
        sys.exit(1)
    port = sys.argv[1]

    validator = Validator()
    print("[INIT] mapping (hidden in the real game):", validator.mapping)

    for note in stream_notes(port):
        prim = validator.validate(note)
        if prim is None:
            reject(note)
        else:
            dispatch(prim)


if __name__ == "__main__":
    main()
