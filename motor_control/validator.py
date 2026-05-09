import random

from motor_control.primitives import Primitive

DEFAULT_NOTE_POOL = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]


class Validator:
    def __init__(self, note_pool: list[str] = None, seed: int | None = None):
        self.note_pool = note_pool or DEFAULT_NOTE_POOL
        self.rng = random.Random(seed)
        self.mapping: dict[str, Primitive] = {}
        self.reshuffle()

    def reshuffle(self) -> None:
        primitives = list(Primitive)
        chosen = self.rng.sample(self.note_pool, len(primitives))
        self.rng.shuffle(primitives)
        self.mapping = dict(zip(chosen, primitives))

    def validate(self, note: str) -> Primitive | None:
        return self.mapping.get(note)
