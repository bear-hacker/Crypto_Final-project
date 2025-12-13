from typing import Optional
from vault.vault_manager import VaultManager
from core import password_generator
import shutil

class Menu:
    def __init__(self, vault: VaultManager):
        self.vault = vault

    def run(self):
        while True:
            self.print_main_menu()
            choice = input("Choose an option (1-6): ").strip()
            if choice == "1":
                self.add_password_flow()
            elif choice == "2":
                self.list_saved_passwords()
            elif choice == "3":
                self.show_password_flow()
            elif choice == "4":
                self.delete_password_flow()
            elif choice == "5":
                self.generate_password_flow()
            elif choice == "6":
                if self.confirm_exit():
                    print("✅ Locking vault and exiting...\n")
                    print("Stay Secure! 🔒")
                    break
            else:
                print("❌ Invalid option. Please choose 1-6")

    def print_main_menu(self):
        print("\n========================================")
        print("             MAIN MENU")
        print("========================================")
        print("1. Add new password")
        print("2. List saved passwords")
        print("3. Show password")
        print("4. Delete password")
        print("5. Generate random password")
        print("6. Exit")
        print("----------------------------------------")

    def prompt_nonempty(self, prompt_text: str) -> str:
        while True:
            v = input(prompt_text).strip()
            if not v:
                print("❌ Website name cannot be empty")
            else:
                return v

    def add_password_flow(self):
        print("\n========================================")
        print("        ➕ ADD NEW PASSWORD")
        print("========================================")
        site = self.prompt_nonempty("Website/App name: ")
        username = self.prompt_nonempty("Username/Email: ")

        print("\n1. Enter password manually\n2. Generate strong password")
        choice = input("Choose (1/2): ").strip()
        notes = ""
        if choice == "1":
            password = input("Enter password: ").strip()
            notes = input("Notes (optional): ").strip()
            self.vault.add_entry(site, username, password, notes)
            print(f"\n✅ Password for '{site}' saved successfully!")
            input("\nPress Enter to continue...")
            return
        else:
            try:
                length = int(input("Password length (default 16): ").strip() or 16)
            except ValueError:
                length = 16
            pwd = password_generator.generate_strong_password(length)
            notes = input("Notes (optional): ").strip()
            self.vault.add_entry(site, username, pwd, notes)
            print("\nGenerated password:", pwd)
            print(f"\n✅ Password for '{site}' saved successfully!")
            input("\nPress Enter to continue...")
            return

    def list_saved_passwords(self):
        print("\n========================================")
        print("       📋 LIST SAVED PASSWORDS")
        print("========================================")
        entries = self.vault.list_entries()
        total = len(entries)
        print(f"\nTotal entries: {total}\n")
        if total == 0:
            print("ℹ️  No passwords stored yet")
            input("\nPress Enter to continue...")
            return
        width = shutil.get_terminal_size((80, 20)).columns
        print(f"{'Website':<25} {'Username':<30}")
        print("-" * min(width, 80))
        for e in entries:
            site = e.get("site","")
            username = e.get("username","")
            print(f"{site:<25} {username:<30}")
        input("\nPress Enter to continue...")

    def show_password_flow(self):
        print("\n========================================")
        print("         🔍 SHOW PASSWORD")
        print("========================================")
        entries = self.vault.list_entries()
        total = len(entries)
        print(f"\nTotal entries: {total}\n")
        if total == 0:
            print("ℹ️  No passwords stored yet")
            input("\nPress Enter to continue...")
            return
        print(f"{'Website':<25} {'Username':<30}")
        print("-" * 60)
        for e in entries:
            print(f"{e.get('site',''):<25} {e.get('username',''):<30}")

        choice = input("\nEnter Website name to show (or 'c' to cancel): ").strip()
        if choice.lower() == 'c':
            return
        entry = self.vault.get_entry(choice)
        if not entry:
            print("\n❌ Password entry not found")
            input("\nPress Enter to continue...")
            return

        print(f"\nWebsite: {entry.get('site')}")
        print("Username:", entry.get('username'))
        print("Password:", entry.get('password'))
        print("Notes:", entry.get('notes', ''))
        print("Created:", entry.get('created', ''))
        input("\nPress Enter to continue...")

    def delete_password_flow(self):
        print("\n========================================")
        print("        🗑️  DELETE PASSWORD")
        print("========================================")
        entries = self.vault.list_entries()
        total = len(entries)
        print(f"\nTotal entries: {total}\n")
        if total == 0:
            print("ℹ️  No passwords stored yet")
            input("\nPress Enter to continue...")
            return
        print(f"{'Website':<25} {'Username':<30}")
        print("-" * 60)
        for e in entries:
            print(f"{e.get('site',''):<25} {e.get('username',''):<30}")

        choice = input("\nEnter Website name to delete (or 'c' to cancel): ").strip()
        if choice.lower() == 'c':
            return
        entry = self.vault.get_entry(choice)
        if not entry:
            print("\n❌ Not found.")
            input("\nPress Enter to continue...")
            return

        print(f"\nWebsite: {entry.get('site')}")
        print("Username:", entry.get("username"))
        print("Password: ********")
        print("Notes:", entry.get("notes", ""))
        print("Created:", entry.get("created", ""))
        confirm = input("\nAre you sure you want to delete this entry? (y/n): ").strip().lower()
        if confirm == 'y':
            ok = self.vault.delete_entry(choice)
            if ok:
                print("✅ Password deleted successfully!")
            else:
                print("❌ Delete failed.")
        else:
            print("Deletion cancelled.")
        input("\nPress Enter to continue...")

    def generate_password_flow(self):
        print("\n========================================")
        print("        🎲 GENERATE PASSWORD")
        print("========================================")
        try:
            length = int(input("Password length (default 16): ").strip() or 16)
        except ValueError:
            length = 16
        pwd = password_generator.generate_strong_password(length)
        strength, _ = password_generator.assess_password_strength(pwd)
        print(f"\nGenerated password: {pwd}")
        print("Strength:", strength)
        print(f"Length: {len(pwd)} characters")
        input("\nPress Enter to continue...")

    def confirm_exit(self) -> bool:
        confirm = input("\nAre you sure you want to exit? (y/n): ").strip().lower()
        return confirm == 'y'
