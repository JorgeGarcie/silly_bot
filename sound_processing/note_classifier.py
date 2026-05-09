from main import analyze_sounds
from main.analyze_sounds import FrequencyNoteModel


def _load_calibration() -> dict[str, list[float]]:
    """Pull the calibration dict from buddy's analyze_sounds module.
    Expects a top-level `CALIBRATION = {note: [samples]}`. Returns {} if missing.
    """
    return getattr(analyze_sounds, "CALIBRATION", {})


class NoteClassifier:
    def __init__(self, samples_per_note: dict[str, list[float]], confidence: float = 0.95):
        self.models = {
            note: FrequencyNoteModel(note, samples, confidence=confidence)
            for note, samples in samples_per_note.items()
            if len(samples) >= 2
        }

    def classify(self, freq: float) -> str | None:
        best_note, best_score = None, 0.0
        for note, model in self.models.items():
            if not model.is_likely(freq):
                continue
            score = model.probability_score(freq)
            if score > best_score:
                best_note, best_score = note, score
        return best_note


default_classifier = NoteClassifier(_load_calibration())
