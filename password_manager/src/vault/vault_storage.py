import json
import base64
from config import VAULT_FILE, AES_GCM_TAG_LEN

def save_encrypted_blob(ciphertext_and_tag: bytes, nonce: bytes) -> None:
    """
    Save one AES-GCM blob per line as JSON with separate base64 nonce, ciphertext, tag.
    """
    if not VAULT_FILE.parent.exists():
        VAULT_FILE.parent.mkdir(parents=True, exist_ok=True)

    if len(ciphertext_and_tag) < AES_GCM_TAG_LEN:
        raise ValueError("ciphertext too short")

    ciphertext = ciphertext_and_tag[:-AES_GCM_TAG_LEN]
    tag = ciphertext_and_tag[-AES_GCM_TAG_LEN:]

    payload = {
        "nonce": base64.b64encode(nonce).decode('ascii'),
        "ciphertext": base64.b64encode(ciphertext).decode('ascii'),
        "tag": base64.b64encode(tag).decode('ascii')
    }
    with VAULT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")

def load_all_blobs() -> list:
    """Return list of payload dicts (nonce/ciphertext/tag) from vault file (one JSON per line)."""
    blobs = []
    if not VAULT_FILE.exists():
        return blobs
    with VAULT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            blobs.append(json.loads(line))
    return blobs

def overwrite_blobs(blobs: list) -> None:
    """Overwrite vault file with given list of payload dicts."""
    with VAULT_FILE.open("w", encoding="utf-8") as f:
        for b in blobs:
            f.write(json.dumps(b, ensure_ascii=False) + "\n")

def vault_exists() -> bool:
    return VAULT_FILE.exists()
