from hazm import Normalizer

normalize = Normalizer().normalize


def cleaner(text: str):
    return normalize(text)
