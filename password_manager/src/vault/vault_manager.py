import json
import base64
import secrets
from datetime import datetime
from typing import Optional, List, Dict
from core.crypto_engine import CryptoEngine
from core import password_generator
from config import AES_GCM_NONCE_LEN
from vault.vault_storage import save_encrypted_blob, load_all_blobs, overwrite_blobs, vault_exists, VAULT_FILE

class VaultManager:
    """
    Each saved password is stored as its own encrypted blob (one line per blob).
    Decryption uses the current key provided via CryptoEngine.
    """

    def __init__(self, crypto: CryptoEngine):
        self.crypto = crypto

    def create_empty(self) -> None:
        # Ensure file exists (empty)
        if not VAULT_FILE.parent.exists():
            VAULT_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not VAULT_FILE.exists():
            VAULT_FILE.write_text("")

    def vault_exists(self) -> bool:
        return vault_exists()

    def add_entry(self, site: str, username: str, password: str, notes: str = "") -> None:
        created = datetime.utcnow().strftime("%Y-%m-%d")
        entry = {
            "site": site,
            "username": username,
            "password": password,
            "notes": notes,
            "created": created
        }
        plaintext = json.dumps(entry, ensure_ascii=False).encode('utf-8')
        nonce = secrets.token_bytes(AES_GCM_NONCE_LEN)
        ciphertext_and_tag = self.crypto.encrypt(plaintext, nonce)
        save_encrypted_blob(ciphertext_and_tag, nonce)

    def list_entries(self) -> List[Dict]:
        entries = []
        blobs = load_all_blobs()
        for blob in blobs:
            try:
                nonce = base64.b64decode(blob["nonce"])
                ciphertext = base64.b64decode(blob["ciphertext"])
                tag = base64.b64decode(blob["tag"])
                plaintext = self.crypto.decrypt(ciphertext + tag, nonce)
                entries.append(json.loads(plaintext.decode('utf-8')))
            except Exception:
                # skip entries that cannot be decrypted with current key
                continue
        return entries

    def get_entry(self, site: str) -> Optional[Dict]:
        for e in self.list_entries():
            if e.get("site","").lower() == site.lower():
                return e
        return None

    def delete_entry(self, site: str) -> bool:
        blobs = load_all_blobs()
        kept = []
        deleted = False
        for blob in blobs:
            try:
                nonce = base64.b64decode(blob["nonce"])
                ciphertext = base64.b64decode(blob["ciphertext"])
                tag = base64.b64decode(blob["tag"])
                plaintext = self.crypto.decrypt(ciphertext + tag, nonce)
                entry = json.loads(plaintext.decode('utf-8'))
                if entry.get("site","").lower() == site.lower():
                    deleted = True
                    continue  # skip this blob
            except Exception:
                # cannot decrypt — keep to avoid data loss
                kept.append(blob)
                continue
            kept.append(blob)
        overwrite_blobs(kept)
        return deleted

    def generate_and_add(self, site: str, username: str, length: int = 16, notes: str = "") -> str:
        pwd = password_generator.generate_strong_password(length)
        self.add_entry(site, username, pwd, notes)
        return pwd
