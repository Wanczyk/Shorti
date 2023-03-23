from random import choices
from string import ascii_letters


def generate_id() -> str:
    return "".join(choices(ascii_letters, k=8))
