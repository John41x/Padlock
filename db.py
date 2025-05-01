# db.py
import mysql.connector
from config import DB_CONFIG

def get_conn():
    """Return a new MySQL connection using DB_CONFIG."""
    return mysql.connector.connect(**DB_CONFIG)

def get_master_record() -> tuple[bytes, bytes] | None:
    """
    Returns (salt, master_hash) or None if not set.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT master_salt, master_hash FROM master_credentials WHERE id=1")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return (row[0], row[1]) if row else None

def set_master_record(salt: bytes, master_hash: bytes) -> None:
    """
    Insert or update the single master-password record.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM master_credentials WHERE id=1")
    exists = cur.fetchone()[0] > 0

    if exists:
        cur.execute(
            "UPDATE master_credentials SET master_salt=%s, master_hash=%s WHERE id=1",
            (salt, master_hash)
        )
    else:
        cur.execute(
            "INSERT INTO master_credentials (id, master_salt, master_hash) VALUES (1, %s, %s)",
            (salt, master_hash)
        )
    conn.commit()
    cur.close()
    conn.close()

def add_entry(site: str, login: str, password_blob: bytes, iv: bytes) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO vault_entries (site, login, password_blob, iv) VALUES (%s, %s, %s, %s)",
        (site, login, password_blob, iv)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_all_entries() -> list[dict]:
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM vault_entries ORDER BY id")
    entries = cur.fetchall()
    cur.close()
    conn.close()
    return entries

def update_entry(entry_id: int, site: str, login: str, password_blob: bytes, iv: bytes) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE vault_entries SET site=%s, login=%s, password_blob=%s, iv=%s WHERE id=%s",
        (site, login, password_blob, iv, entry_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_entry(entry_id: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM vault_entries WHERE id=%s", (entry_id,))
    conn.commit()
    cur.close()
    conn.close()
