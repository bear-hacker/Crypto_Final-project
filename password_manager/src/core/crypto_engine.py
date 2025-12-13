from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets

class CryptoEngine:
    """
    AES-GCM wrapper using a 32-byte key.
    encrypt returns ciphertext||tag (bytes). We'll let vault_storage split tag.
    """

    def __init__(self, key: bytes):
        if not isinstance(key, (bytes, bytearray)) or len(key) != 32:
            raise ValueError("Key must be 32 bytes.")
        self._aead = AESGCM(key)

    def encrypt(self, plaintext: bytes, nonce: bytes) -> bytes:
        return self._aead.encrypt(nonce, plaintext, None)

    def decrypt(self, ciphertext_and_tag: bytes, nonce: bytes) -> bytes:
        return self._aead.decrypt(nonce, ciphertext_and_tag, None)
