# gui.py
import os
import base64
import tkinter as tk
from tkinter import ttk, messagebox

from db import (
    get_master_record, set_master_record,
    add_entry, get_all_entries,
    update_entry, delete_entry
)
from crypto import derive_key, encrypt, decrypt, generate_password
from utils import copy_to_clipboard, clear_clipboard_after

AES_KEY = None  # will hold the derived key once logged in

def launch_app():
    if get_master_record() is None:
        show_setup_window()
    else:
        show_login_window()

def show_setup_window():
    def submit():
        pw = pw_entry.get()
        confirm = confirm_entry.get()
        if not pw or pw != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        salt = os.urandom(16)
        key = derive_key(pw, salt)
        set_master_record(salt, key)
        setup.destroy()
        show_vault_window(key)

    setup = tk.Tk()
    setup.title("Set Master Password")
    tk.Label(setup, text="Master Password:").pack(padx=10, pady=5)
    pw_entry = tk.Entry(setup, show="*"); pw_entry.pack(padx=10)
    tk.Label(setup, text="Confirm Password:").pack(padx=10, pady=5)
    confirm_entry = tk.Entry(setup, show="*"); confirm_entry.pack(padx=10)
    tk.Button(setup, text="Set Password", command=submit).pack(pady=10)
    setup.mainloop()

def show_login_window():
    def submit():
        pw = pw_entry.get()
        record = get_master_record()
        if record is None:
            messagebox.showerror("Error", "No master password set.")
            return
        salt, stored_hash = record
        key = derive_key(pw, salt)
        if key == stored_hash:
            login.destroy()
            show_vault_window(key)
        else:
            messagebox.showerror("Error", "Wrong password.")

    login = tk.Tk()
    login.title("Enter Master Password")
    tk.Label(login, text="Master Password:").pack(padx=10, pady=5)
    pw_entry = tk.Entry(login, show="*"); pw_entry.pack(padx=10)
    tk.Button(login, text="Login", command=submit).pack(pady=10)
    login.mainloop()

def reset_master_password():
    def do_reset():
        old_pw = old_pw_entry.get()
        new_pw = new_pw_entry.get()
        confirm_pw = confirm_pw_entry.get()

        if new_pw != confirm_pw:
            messagebox.showerror("Error", "New passwords do not match.")
            return

        record = get_master_record()
        if record is None:
            messagebox.showerror("Error", "Master record not found.")
            return

        salt, current_hash = record
        try:
            test_key = derive_key(old_pw, salt)
        except Exception:
            messagebox.showerror("Error", "Password derivation failed.")
            return

        if test_key != current_hash:
            messagebox.showerror("Error", "Old password incorrect.")
            return

        # Validated — save new salt/hash
        new_salt = os.urandom(16)
        new_key = derive_key(new_pw, new_salt)
        set_master_record(new_salt, new_key)

        messagebox.showinfo("Success", "Master password reset.")
        reset_window.destroy()

    reset_window = tk.Toplevel()
    reset_window.title("Reset Master Password")

    tk.Label(reset_window, text="Current Password:").pack()
    old_pw_entry = tk.Entry(reset_window, show="*")
    old_pw_entry.pack()

    tk.Label(reset_window, text="New Password:").pack()
    new_pw_entry = tk.Entry(reset_window, show="*")
    new_pw_entry.pack()

    tk.Label(reset_window, text="Confirm New Password:").pack()
    confirm_pw_entry = tk.Entry(reset_window, show="*")
    confirm_pw_entry.pack()

    tk.Button(reset_window, text="Submit", command=do_reset).pack(pady=5)


def show_vault_window(key):
    global AES_KEY
    AES_KEY = key

    root = tk.Tk()
    root.title("Padlock Vault")
    # Reset password button
    tk.Button(root, text="Reset Master Password", command=reset_master_password).pack(pady=10)


    # ─── Inputs ───────────────────────────────────
    frm = tk.Frame(root); frm.pack(padx=10, pady=5)
    tk.Label(frm, text="Site:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    site_entry = tk.Entry(frm); site_entry.grid(row=0, column=1, padx=5, pady=2)
    tk.Label(frm, text="Login:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
    login_entry = tk.Entry(frm); login_entry.grid(row=1, column=1, padx=5, pady=2)
    tk.Label(frm, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
    pw_entry = tk.Entry(frm); pw_entry.grid(row=2, column=1, padx=5, pady=2)

    # ─── Table ────────────────────────────────────
    tree = ttk.Treeview(root, columns=("ID","Site","Login","Blob","IV"), show="headings")
    for col, w in [("ID",40),("Site",150),("Login",150),("Blob",200),("IV",120)]:
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")
    tree.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    # ─── Callbacks ───────────────────────────────
    def refresh():
        for r in tree.get_children():
            tree.delete(r)
        for e in get_all_entries():
            # Base64-encode for safe storage in Treeview
            blob_b64 = base64.b64encode(e['password_blob']).decode('ascii')
            iv_b64   = base64.b64encode(e['iv']).decode('ascii')
            tree.insert('', tk.END, values=(
                e['id'], e['site'], e['login'], blob_b64, iv_b64
            ))

    def generate():
        pwd = generate_password()
        pw_entry.delete(0, tk.END)
        pw_entry.insert(0, pwd)

    def save():
        site = site_entry.get().strip()
        login_ = login_entry.get().strip()
        pwd = pw_entry.get()
        if not (site and login_ and pwd):
            messagebox.showerror("Error", "Fill all fields.")
            return
        blob, iv = encrypt(pwd, AES_KEY)
        add_entry(site, login_, blob, iv)
        refresh()

    def update_selected():
        sel = tree.focus()
        if not sel:
            return
        rid = tree.item(sel)['values'][0]
        blob, iv = encrypt(pw_entry.get(), AES_KEY)
        update_entry(rid, site_entry.get(), login_entry.get(), blob, iv)
        refresh()

    def delete_selected():
        sel = tree.focus()
        if not sel:
            return
        delete_entry(tree.item(sel)['values'][0])
        refresh()

    def copy_selected():
        sel = tree.focus()
        if not sel:
            return
        vals    = tree.item(sel)['values']
        blob_b64 = vals[3]
        iv_b64   = vals[4]
        # Base64-decode back to raw bytes
        blob = base64.b64decode(blob_b64)
        iv   = base64.b64decode(iv_b64)
        pwd  = decrypt(blob, iv, AES_KEY)
        copy_to_clipboard(pwd)
        clear_clipboard_after(20)

    # ─── Buttons ─────────────────────────────────
    btn_frm = tk.Frame(root); btn_frm.pack(pady=5)
    tk.Button(btn_frm, text="Generate",      command=generate).grid(row=0,column=0,padx=5)
    tk.Button(btn_frm, text="Save",          command=save).grid(row=0,column=1,padx=5)
    tk.Button(btn_frm, text="Update",        command=update_selected).grid(row=0,column=2,padx=5)
    tk.Button(btn_frm, text="Delete",        command=delete_selected).grid(row=0,column=3,padx=5)
    tk.Button(btn_frm, text="Copy Password", command=copy_selected).grid(row=0,column=4,padx=5)

    refresh()
    root.mainloop()
