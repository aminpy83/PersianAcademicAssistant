import re
from hazm import Normalizer

normalizer = Normalizer()


def cleaner(text: str) -> str:
    text = normalizer.normalize(text)

    text = re.sub(r'\s+', ' ', text)

    text = text.strip()

    return text
