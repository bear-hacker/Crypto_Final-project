#!/usr/bin/env python3
import sys

from pathlib import Path
from getpass import getpass
import json
import time

from config import DATA_DIR, MASTER_FILE, VAULT_FILE, MAX_ATTEMPTS, LOCKOUT_SECONDS
from core.key_manager import KeyManager
from core.crypto_engine import CryptoEngine
from vault.vault_manager import VaultManager
from ui.menu import Menu
from core.password_generator import assess_password_strength
from vault.vault_storage import vault_exists, load_all_blobs

def print_header():
    print("========================================")
    print("🔐 SECURE PASSWORD MANAGER 🔐")
    print("========================================")
    print()

def create_new_vault_flow(km: KeyManager):
    print("========================================")
    print("          CREATE NEW VAULT")
    print("========================================")
    print("ℹ️  Set up your master password")
    print("⚠️  Remember this password! There is no recovery option.")
    print()

    while True:
        pw = getpass("Enter Master Password: ").strip()
        if not pw:
            print("❌ Password must be at least 6 characters")
            continue
        label, _ = assess_password_strength(pw)
        # show strength
        print(f"\nℹ️  Password strength: {label}")
        confirm = getpass("Confirm Master Password: ").strip()
        if pw != confirm:
            print("\n❌ Passwords do not match. Please try again.")
            continue
        # create new salt and save master hash
        key = km.create_new_master(pw)
        print("\n✅ New vault created successfully!\n")
        return key

def reset_vault():
    # delete vault file if exists
    if VAULT_FILE.exists():
        VAULT_FILE.unlink()
    # reset master file will be handled by create flow
    if MASTER_FILE.exists():
        MASTER_FILE.unlink()
    print("✅ Old vault deleted.\n")

def unlock_menu(km: KeyManager):
    """
    Show unlock menu with options:
    1. Enter password
    2. Forgot password (Reset vault)
    3. Exit
    """
    while True:
        print("========================================")
        print("           UNLOCK VAULT")
        print("========================================")
        print()
        print("Options:")
        print("1. Enter password")
        print("2. Forgot password (Reset vault)")
        print("3. Exit")
        print()
        choice = input("Choose option (1-3): ").strip()
        if choice == "1":
            key = km.unlock_master_interactive()
            return key
        elif choice == "2":
            print()
            print("========================================")
            print("        ⚠️  RESET VAULT")
            print("========================================")
            print("⚠️  This will DELETE ALL saved passwords!")
            print("⚠️  This action CANNOT be undone!")
            confirm = input("\nType 'RESET' to confirm: ").strip()
            if confirm == "RESET":
                reset_vault()
                # create new vault now
                return create_new_vault_flow(km)
            else:
                print("ℹ️  Reset cancelled.\n")
                continue
        elif choice == "3":
            print("\nℹ️  Exiting...")
            return None
        else:
            print("❌ Invalid choice. Please choose 1-3.\n")

def main():
    print_header()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    km = KeyManager()

    # If master file doesn't exist -> create new vault flow
    if not MASTER_FILE.exists():
        key = create_new_vault_flow(km)
    else:
        key = unlock_menu(km)
        if key is None:
            print("❌ Failed to initialize vault. Exiting.")
            return

    crypto = CryptoEngine(key)
    vault = VaultManager(crypto)

    # If vault file missing or empty, ensure an empty vault exists
    if not vault_exists():
        vault.create_empty()
    else:
        try:
            # Validate that key can be used to decrypt (list_entries attempts decryption)
            _ = vault.list_entries()
        except Exception as e:
            # If decryption fails in an unexpected way, return an informative message
            print("❌ Failed to load vault (wrong password or corrupted).")
            print("Error:", e)
            return

    # Now show main menu
    menu = Menu(vault)
    menu.run()

if __name__ == "__main__":
    main()
