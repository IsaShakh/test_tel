import re

mask_symbols = {
    "N": "[0-9]",
    "A": "[A-Z]",
    "a": "[a-z]",
    "X": "[A-Z0-9]",
    "Z": "[-_@]"
}


def convert_mask_to_regex(mask: str) -> str:
    """Приведение маски к регулярке"""
    pattern = ''.join([mask_symbols.get(ch, re.escape(ch)) for ch in mask])
    return '^' + pattern + '$'


def validate_serial_number_mask(serial_number: str, mask: str) -> bool:
    """Сам метод валидации"""
    regex = convert_mask_to_regex(mask)
    return re.match(regex, serial_number) is not None
