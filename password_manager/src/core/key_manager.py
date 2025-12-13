import json
import secrets
import base64
import time
from getpass import getpass
from typing import Optional

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

from config import MASTER_FILE, KDF_SALT_LEN, KDF_ITERATIONS, KEY_LENGTH, MAX_ATTEMPTS, LOCKOUT_SECONDS

class KeyManager:
    """
    Handles master.json: contains base64 salt, base64 master_hash (derived key),
    and lockout_until (unix timestamp) fields.
    """

    def __init__(self):
        self.master_file = MASTER_FILE

    def _write_master(self, salt: bytes, key_bytes: bytes, lockout_until: float = 0):
        payload = {
            "salt": base64.b64encode(salt).decode('ascii'),
            "master_hash": base64.b64encode(key_bytes).decode('ascii'),
            "lockout_until": lockout_until
        }
        with open(self.master_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def _read_master(self):
        with open(self.master_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _derive(self, master_password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KEY_LENGTH,
            salt=salt,
            iterations=KDF_ITERATIONS
        )
        return kdf.derive(master_password.encode('utf-8'))

    def create_new_master(self, master_password: str) -> bytes:
        salt = secrets.token_bytes(KDF_SALT_LEN)
        key_bytes = self._derive(master_password, salt)
        # store salt + derived key as master_hash
        self._write_master(salt, key_bytes, lockout_until=0)
        return key_bytes

    def unlock_master_interactive(self) -> Optional[bytes]:
        """
        Interactive unlocking. Implements attempts and lockout.
        Returns derived key bytes on success, None on exit/failure.
        """
        if not self.master_file.exists():
            return None
        data = self._read_master()
        salt = base64.b64decode(data["salt"])
        stored_key = base64.b64decode(data["master_hash"])
        lockout_until = data.get("lockout_until", 0)

        now = time.time()
        if now < lockout_until:
            remaining = int(lockout_until - now)
            print(f"❌ Vault locked. Try again in {remaining} seconds.")
            return None

        attempts = MAX_ATTEMPTS
        while attempts > 0:
            master = getpass("Enter Master Password: ").strip()
            if not master:
                attempts -= 1
                print(f"❌ Incorrect password. {attempts} attempt(s) remaining.")
                continue
            try:
                key_bytes = self._derive(master, salt)
            except Exception:
                attempts -= 1
                print(f"❌ Incorrect password. {attempts} attempt(s) remaining.")
                continue

            if key_bytes == stored_key:
                # success: reset lockout
                self._write_master(salt, stored_key, lockout_until=0)
                return key_bytes
            else:
                attempts -= 1
                print(f"❌ Incorrect password. {attempts} attempt(s) remaining.")
                if attempts == 0:
                    print("❌ Maximum attempts reached.")
                    # apply lockout
                    new_lockout = time.time() + LOCKOUT_SECONDS
                    self._write_master(salt, stored_key, lockout_until=new_lockout)
                    return None
        return None
