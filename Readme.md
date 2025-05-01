📄 README.md
# 🔐 Padlock – Encrypted Password Manager

Padlock is a personal, GUI-based password manager built in Python with full AES encryption, a secure master password system, and a MySQL backend.

It stores your login credentials for websites securely, with the ability to:
- Add, update, delete, and view entries
- Generate strong random passwords
- Copy passwords to clipboard (auto-clears after 20 seconds)
- Protect access using a master password

---

## 📦 Features

- ✅ AES-CBC encryption (via `cryptography`)
- ✅ Encrypted entries stored in MySQL
- ✅ Master password with PBKDF2 key derivation
- ✅ Tkinter GUI for ease of use
- ✅ Clipboard auto-clear
- ✅ Password generator
- ✅ Master password reset support

---

## 🛠 Requirements

- Python 3.10+
- MySQL Server (e.g. via XAMPP or MySQL Workbench)
- pip & virtualenv (recommended)

---

## ⚙️ Setup Instructions

### 1. Clone or download the repository

```bash
git clone https://github.com/yourname/padlock.git
cd padlock

2. Set up a virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Configure the database
Create a database named padlock using phpMyAdmin or the MySQL CLI:
CREATE DATABASE padlock;

Then import the schema:
mysql -u root -p < create.sql

Or use phpMyAdmin → Select padlock → Import → Choose create.sql
5. Update your .env file
Make sure .env contains:
DB_HOST=localhost
DB_USER=root
DB_PASS=
DB_NAME=padlock


🚀 Running the App
python3 app.py

First time: You’ll be asked to set a master password


After that: You’ll be asked to enter your master password


Add new password entries with the form


Select any row to update, delete, or copy the password



🔐 Security Notes
All passwords are AES-CBC encrypted in MySQL


Master password is stored as a hashed key with a salt using PBKDF2


Clipboard is automatically cleared after 20 seconds


Master password can be reset securely (via identity check)



🧠 Future Ideas
Search and filter by site name


Export encrypted vault to a file


Biometric unlock or file-based key support



📁 File Structure
padlock/
├── app.py              # Entry point
├── gui.py              # Tkinter GUI
├── db.py               # Database CRUD operations
├── crypto.py           # Encryption & password generation
├── utils.py            # Clipboard utilities
├── config.py           # Loads DB config from .env
├── create.sql          # MySQL table schema
├── requirements.txt    # Dependencies
├── .env                # DB credentials (excluded in .gitignore)
└── README.md


✅ Credits
Made by John. Inspired by real-world vault apps and the desire to learn encryption, GUIs, and databases.

