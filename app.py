import sys

from motor_control.dispatcher import Dispatcher
from motor_control.validator import Validator
from sound_processing.note_detector import stream_notes


def main():
    if len(sys.argv) < 2:
        print("usage: python app.py <fft_port> [motor_port]")
        print("  fft_port:   serial port of the Arduino running FFT (e.g. COM3)")
        print("  motor_port: serial port of the motor Arduino (omit for terminal-only)")
        sys.exit(1)
    fft_port = sys.argv[1]
    motor_port = sys.argv[2] if len(sys.argv) > 2 else None

    validator = Validator()
    dispatcher = Dispatcher(motor_port)
    print("[INIT] mapping (hidden in the real game):", {n: p.name for n, p in validator.mapping.items()})

    try:
        for note in stream_notes(fft_port):
            prim = validator.validate(note)
            if prim is None:
                dispatcher.reject(note)
            else:
                dispatcher.dispatch(prim)
    finally:
        dispatcher.close()


if __name__ == "__main__":
    main()
