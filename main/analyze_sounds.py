
import numpy as np
from scipy.stats import norm

class FrequencyNoteModel:
    def __init__(self, note_name, frequencies, confidence=0.95):
        """
        note_name: string label for the note
        frequencies: list or array of sample frequencies
        confidence: probability range to define likely boundaries
        """
        self.note_name = note_name
        self.frequencies = np.array(frequencies)

        # Statistics
        self.mean = np.mean(self.frequencies)
        self.std = np.std(self.frequencies, ddof=1)

        # Confidence interval boundaries
        z = norm.ppf((1 + confidence) / 2)
        self.lower_bound = self.mean - z * self.std
        self.upper_bound = self.mean + z * self.std

    def is_likely(self, frequency):
        """
        Returns True if frequency is within likely range
        """
        return self.lower_bound <= frequency <= self.upper_bound

    def probability_score(self, frequency):
        """
        Returns probability density score
        Higher = more likely
        """
        return norm.pdf(frequency, self.mean, self.std)

    def summary(self):
        return {
            "note": self.note_name,
            "mean": self.mean,
            "std_dev": self.std,
            "lower_bound": self.lower_bound,
            "upper_bound": self.upper_bound
        }


samples = [130.2 
    , 141.2 
    , 142.1 
    , 249.8 
    , 135.2 
    , 139.3 
    , 137.1 
    , 162.5 
    , 127.3 
    , 155.3 
    , 251.1 
    , 139.1 
    , 134.3 
    , 147.7 ]
def analyze_note_frequencies(samples, f):
    # Example training data

    # Build model
    model = FrequencyNoteModel("A4", samples)

    # Print stats
    print(model.summary())

    # Test unknown frequencies

    print(
        f"Frequency {f} Hz -> "
        f"Likely note? {model.is_likely(f)} "
        f"(score={model.probability_score(f):.5f})"
    )
    return (f, model.is_likely(f), model.probability_score(f))

samples = {[130.2 
    , 141.2 
    , 142.1 
    , 249.8 
    , 135.2 
    , 139.3 
    , 137.1 
    , 162.5 
    , 127.3 
    , 155.3 
    , 251.1 
    , 139.1 
    , 134.3 
    , 147.7 ]}

analyze_note_frequencies(samples, 140.0)
analyze_note_frequencies(samples, 171.2)
analyze_note_frequencies(samples, 250.0)