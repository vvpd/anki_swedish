import json
from dataclasses import dataclass, is_dataclass, asdict

@dataclass
class BasicSentence:
    """ Hold the basic unaugmented senteces """
    from_lang: str # Code of main language
    original: str # Main sentence
    to_lang: str # Code of lang to translate into
    translation: str # Translated sentence
    tatoeba_id: str # Id of original sentence on tatoeba

class SentenceEncoder(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)

@dataclass
class FrequencyData:
    """ Load frequency list into this format """
    raw_freq: int
    wpm: float
    cefr: str
    marker: str
    item: str

@dataclass
class AugmentedSentence:
    """ Additional info about a sentence """
    text: BasicSentence
    average_wpm: float
    words: int
    cefr: str
    cefr_level: int
    hardest_word: FrequencyData
    lemmas: "list[str]"
