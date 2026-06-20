import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64
import json

SALT_FILE = "salt.bin"
VAULT_FILE = "vault.json"


def load_or_create_salt():
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    else:
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
        return salt


def derive_key(master_password):
    salt = load_or_create_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
    )
    key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key)


def save_vault(entries, key):
    f = Fernet(key)
    data = json.dumps(entries).encode()
    encrypted = f.encrypt(data)
    with open(VAULT_FILE, "wb") as file:
        file.write(encrypted)


def load_vault(key):
    if not os.path.exists(VAULT_FILE):
        return []
    f = Fernet(key)
    with open(VAULT_FILE, "rb") as file:
        encrypted = file.read()
    decrypted = f.decrypt(encrypted)
    return json.loads(decrypted)


def add_entry(entries):
    site = input("Site name: ")
    username = input("Username: ")
    password = input("Password: ")
    entries.append({"site": site, "username": username, "password": password})
    print("Entry added.")


def view_entries(entries):
    if not entries:
        print("No entries saved yet.")
        return
    for i, entry in enumerate(entries):
        print(f"{i+1}. Site: {entry['site']} | Username: {entry['username']} | Password: {entry['password']}")


def search_entry(entries):
    keyword = input("Enter site name to search: ").lower()
    results = [e for e in entries if keyword in e["site"].lower()]
    if not results:
        print("No matching entries found.")
        return
    for i, entry in enumerate(results):
        print(f"{i+1}. Site: {entry['site']} | Username: {entry['username']} | Password: {entry['password']}")


def delete_entry(entries):
    view_entries(entries)
    if not entries:
        return
    choice = input("Enter the number of the entry to delete: ")
    if choice.isdigit() and 1 <= int(choice) <= len(entries):
        removed = entries.pop(int(choice) - 1)
        print(f"Deleted entry for {removed['site']}.")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    master_password = input("Enter your master password: ")
    key = derive_key(master_password)
    entries = load_vault(key)

    while True:
        print("\n--- Password Manager ---")
        print("1. Add entry")
        print("2. View entries")
        print("3. Delete entry")
        print("4. Search entry")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_entry(entries)
            save_vault(entries, key)
        elif choice == "2":
            view_entries(entries)
        elif choice == "3":
            delete_entry(entries)
            save_vault(entries, key)
        elif choice == "4":
            search_entry(entries)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")