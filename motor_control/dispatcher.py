import serial

from motor_control.primitives import Primitive


class Dispatcher:
    """Sends primitive codes to the motor Arduino over serial."""

    def __init__(self, port: str | None, baud: int = 115200):
        self.ser = serial.Serial(port, baud, timeout=1) if port else None

    def dispatch(self, primitive: Primitive) -> None:
        print(f"[CMD] {primitive.name} ({primitive.value})")
        if self.ser is not None:
            self.ser.write(f"{primitive.value}\n".encode())

    def reject(self, note: str) -> None:
        print(f"[--- ] {note} not bound")

    def close(self) -> None:
        if self.ser is not None:
            self.ser.close()
