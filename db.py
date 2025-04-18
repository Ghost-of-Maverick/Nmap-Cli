import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("nmap_scans.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            scan_type TEXT,
            command TEXT,
            result TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_scan(target, scan_type, command, result):
    conn = sqlite3.connect("nmap_scans.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scans (target, scan_type, command, result, timestamp) VALUES (?, ?, ?, ?, ?)", 
                   (target, scan_type, command, result, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_scan_history():
    conn = sqlite3.connect("nmap_scans.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, target, scan_type, timestamp FROM scans ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
