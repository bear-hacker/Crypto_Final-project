# 🔐 Secure Password Manager (CLI)

A secure command-line password manager built with **Python** and **modern cryptography**. This application allows users to safely store, manage, and generate passwords using a single master password. All sensitive data is encrypted locally using industry-standard cryptographic algorithms.

---

## 📌 Features

* 🔑 Master password–protected vault
* 🔒 AES-256-GCM encryption for stored passwords
* 🧠 PBKDF2 key derivation with salt and high iteration count
* 🧾 Add, view, list, and delete password entries
* 🎲 Strong random password generator
* 🚫 Brute-force protection with login attempt limits and lockout
* 💻 Fully offline (no internet required)

---

## 🛠️ Technologies Used

* **Python 3**
* **cryptography** library
* AES-GCM (Authenticated Encryption)
* PBKDF2-HMAC-SHA256

---

## 📂 Project Structure

```
password_manager/
│   requirements.txt
│   README.md
│
└───src/
    ├───config.py
    ├───main.py
    │
    ├───core/
    │   ├───crypto_engine.py
    │   ├───key_manager.py
    │   └───password_generator.py
    │
    ├───vault/
    │   ├───vault_manager.py
    │   └───vault_storage.py
    │
    └───ui/
        └───menu.py
```

Sensitive runtime files are created automatically in the `data/` directory and are excluded from version control.

---

## ⚙️ Installation

### 1️⃣ Requirements

* Python 3.9 or higher
* pip package manager

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` contains:

```txt
cryptography
```

---

## ▶️ How to Run

Navigate to the `src` directory and run:

```bash
python main.py
```

---

## 🔐 First-Time Setup

1. On first launch, you will be prompted to create a **master password**.
2. The password strength will be evaluated and displayed.
3. A cryptographic key is derived using PBKDF2 and stored securely.
4. An encrypted vault is initialized.

⚠️ **Important:** There is no password recovery. If the master password is lost, the vault must be reset.

---

## 🔓 Unlocking the Vault

* Enter the correct master password to unlock the vault.
* After multiple failed attempts, the vault is temporarily locked.
* This prevents brute-force password attacks.

---

## 📋 Available Menu Options

1. **Add New Password** – Store credentials securely
2. **List Saved Passwords** – View stored sites/usernames
3. **Show Password** – Decrypt and reveal a selected password
4. **Delete Password** – Remove a stored entry
5. **Generate Random Password** – Create a strong password
6. **Exit** – Lock the vault and exit

All decryption occurs **only in memory**.

---

## 🔒 Security Design

* Passwords are encrypted using **AES-256-GCM**
* Encryption keys are derived with **PBKDF2 + salt**
* Each entry uses a unique nonce
* No plaintext passwords are written to disk
* Vault data remains secure even if files are stolen

---

## 🧪 Example Use Case

* Create a vault with a strong master password
* Generate and store unique passwords for each website
* Retrieve credentials securely when needed
* Safely delete outdated entries

---

## 🚀 Future Enhancements

* Web-based version
* SQL database storage
* Email (Gmail) login support
* Multi-Factor Authentication (MFA)
* Cloud deployment with encryption-at-rest

---

## 📚 References

* NIST FIPS 197 – Advanced Encryption Standard (AES)
* NIST SP 800-132 – Password-Based Key Derivation
* OWASP Password Storage Cheat Sheet
* Python Cryptography Documentation

---

## 👤 Author

bear-hacker

---

## ⚠️ Disclaimer

This project is for **educational purposes**. While it follows best practices, it should be professionally audited before use in production environments.
