"""Offline operational affect state, not a model of subjective experience."""
from dataclasses import dataclass, field

CATEGORIES = (
    'admiration','adoration','aesthetic_appreciation','amusement','anger',
    'anxiety','awe','awkwardness','boredom','calmness','confusion',
    'craving','disgust','empathic_pain','entrancement','excitement',
    'fear','horror','interest','joy','nostalgia','relief','romance',
    'sadness','satisfaction','sexual_desire','surprise'
)

@dataclass
class AffectState:
    valence: float = 0.0
    arousal: float = 0.0
    dominance: float = 0.5
    intensities: dict[str, float] = field(default_factory=lambda: {name: 0.0 for name in CATEGORIES})

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not -1 <= self.valence <= 1:
            raise ValueError('valence outside [-1,1]')
        if not 0 <= self.arousal <= 1 or not 0 <= self.dominance <= 1:
            raise ValueError('arousal/dominance outside [0,1]')
        if set(self.intensities) != set(CATEGORIES):
            raise ValueError('category mismatch')
        if any(not 0 <= x <= 1 for x in self.intensities.values()):
            raise ValueError('intensity outside [0,1]')

    def set_intensity(self, category: str, value: float):
        if category not in CATEGORIES:
            raise KeyError(category)
        if not 0 <= value <= 1:
            raise ValueError('intensity outside [0,1]')
        self.intensities[category] = float(value)

    def decay(self, factor: float):
        if not 0 <= factor <= 1:
            raise ValueError('factor outside [0,1]')
        for name in CATEGORIES:
            self.intensities[name] *= factor

    def active(self, threshold: float = 0.5):
        if not 0 <= threshold <= 1:
            raise ValueError('threshold outside [0,1]')
        return {k: v for k, v in self.intensities.items() if v >= threshold}
