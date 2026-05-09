from motor_control.primitives import Primitive


def dispatch(primitive: Primitive) -> None:
    print(f"[CMD] {primitive.value}")


def reject(note: str) -> None:
    print(f"[--- ] {note} not bound")
