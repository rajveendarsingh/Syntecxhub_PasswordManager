# Syntecxhub_PasswordManager

A simple command-line password manager built in Python 

## Overview

This project securely stores login credentials (site, username, password) on the local machine using strong encryption. Instead of saving passwords as plain readable text, all data is encrypted before being written to disk, and can only be unlocked using a single master password.

## Features

- Master password protected access
- AES encryption (via Python's `cryptography` library, using Fernet) for all stored credentials
- Key derivation from the master password using PBKDF2-HMAC-SHA256 (200,000 iterations + random salt)
- Add, view, search, and delete password entries
- Encrypted local storage (`vault.json`) — no plaintext passwords ever written to disk

## How It Works

1. On startup, the user enters a master password.
2. The password is combined with a randomly generated salt and passed through PBKDF2-HMAC-SHA256 to derive a 32-byte AES encryption key.
3. This key is used with Fernet (AES) to encrypt and decrypt the vault file.
4. All entries are stored as a JSON list in memory, converted to JSON text, and encrypted as a single block before being saved to `vault.json`.
5. The master password itself is never stored anywhere — only a salt (random, non-secret data) is saved, allowing the same key to be re-derived on future runs.

## Requirements

- Python 3.x
- `cryptography` library

Install dependencies:
```bash
pip install cryptography
```

## Usage

Run the program:
```bash
python password_manager.py
```

You'll be prompted for your master password, then presented with a menu:
```
--- Password Manager ---
1. Add entry
2. View entries
3. Delete entry
4. Search entry
5. Exit
```

- **Add entry** – save a new site, username, and password
- **View entries** – display all saved entries
- **Search entry** – find entries matching a keyword in the site name
- **Delete entry** – remove a saved entry by its number
- **Exit** – close the program

## Project Structure

password_manager/
├── password_manager.py   # main program
├── salt.bin               # randomly generated salt (created on first run, not committed)
├── vault.json              # encrypted password storage (created on first run, not committed)
├── .gitignore
└── README.md


## Security Notes

- The master password is never stored anywhere — only a derived key is used in memory during the session.
- `vault.json` and `salt.bin` are excluded from version control via `.gitignore`, since they may contain personal/encrypted data specific to each user.
- AES encryption via Fernet ensures the vault file is unreadable without the correct master password.
- This project was built for educational purposes as part of an internship task and is **not intended for production use** without further security review.

## What I Learned

- Practical use of symmetric encryption (AES) in a real application
- How key derivation functions (PBKDF2) turn a human password into a secure encryption key
- Why salts are used and why master passwords should never be stored directly
- Structuring a Python CLI application with clear, single-responsibility functions
- Safe handling of sensitive files in Git using `.gitignore`

## Author

Built by **Rajveendar Singh** as part of the Syntecxhub Internship Program — Cybersecurity Track.

## Disclaimer

This is a learning project. While it demonstrates real encryption concepts, it has not undergone professional security auditing and should not be used to store real, sensitive passwords in production environments.
