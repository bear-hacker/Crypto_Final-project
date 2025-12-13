from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

MASTER_FILE = DATA_DIR / "master.json"
VAULT_FILE = DATA_DIR / "vault.data"

# KDF settings
KDF_SALT_LEN = 16
KDF_ITERATIONS = 200_000
KEY_LENGTH = 32  # bytes

# AES-GCM
AES_GCM_NONCE_LEN = 12
AES_GCM_TAG_LEN = 16

# Lockout settings
MAX_ATTEMPTS = 3
LOCKOUT_SECONDS = 60  # 1 minute
