# test_db_connection.py
import mysql.connector
from config import DB_CONFIG

if __name__ == "__main__":
    conn = mysql.connector.connect(**DB_CONFIG)
    cur  = conn.cursor()
    cur.execute("SELECT NOW()")
    print("✔ Database time is:", cur.fetchone()[0])
    cur.close()
    conn.close()
