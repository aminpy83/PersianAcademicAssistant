import re
from hazm import Normalizer

normalizer = Normalizer()


def cleaner(text: str) -> str:

    text = normalizer.normalize(text)

    # حذف فاصله‌های انتهای خطوط
    text = re.sub(r'[ \t]+', ' ', text)

    # حذف خطوط خالی اضافی
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    # حذف فاصله‌های اضافی اطراف خطوط
    lines = [line.strip() for line in text.splitlines()]

    text = "\n".join(lines)

    return text.strip()