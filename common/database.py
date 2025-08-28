# Simple SQLite wrapper for demonstration
import sqlite3

def get_connection(db_name="nexus_enroll.db"):
    return sqlite3.connect(db_name)