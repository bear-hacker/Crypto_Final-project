import secrets
import string
from typing import Tuple

def generate_strong_password(length: int = 16) -> str:
    if length < 8:
        raise ValueError("Password length should be >= 8")
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        pwd = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in pwd)
            and any(c.isupper() for c in pwd)
            and any(c.isdigit() for c in pwd)
            and any(c in string.punctuation for c in pwd)):
            return pwd

def assess_password_strength(pw: str) -> Tuple[str, int]:
    score = 0
    if len(pw) >= 6:
        score += 1
    if any(c.islower() for c in pw) and any(c.isupper() for c in pw):
        score += 1
    if any(c.isdigit() for c in pw):
        score += 1
    if any(c in string.punctuation for c in pw):
        score += 1
    if len(pw) >= 16:
        score += 1

    if score <= 1:
        label = "Very Weak"
    elif score == 2:
        label = "Weak"
    elif score == 3:
        label = "Medium"
    elif score == 4:
        label = "Strong"
    else:
        label = "Very Strong"
    return label, score
