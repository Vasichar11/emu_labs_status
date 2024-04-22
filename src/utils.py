import os
from datetime import datetime
import sqlite3 

# Return most recent db
def most_recent_db(db_folder):
    db_files = os.listdir(db_folder)
    if len(db_files) == 1: 
        db = os.path.join(db_folder, db_files[0])
    else:

        db_files = [f for f in db_files if f.startswith('emu_') and f.endswith('.db')] # filter files that don't match
        timestamps = [datetime.strptime(f.split('emu_')[1], "%Y-%m-%d_%H-%M-%S.db") for f in db_files]
        idx_most_recent = timestamps.index(max(timestamps))
        db = os.path.join(db_folder, db_files[idx_most_recent])
        
    return db

def query_labs(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT lab FROM SummaryLabProgress")
        labs = cursor.fetchall()
        lab_names = [lab[0] for lab in labs]
        return lab_names
    finally:
        cursor.close()
        conn.close() 

def query_period(db, lab):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    past = {}
    upcoming = {}
    try:
        cursor.execute("""
            SELECT year, week, date
            FROM LabProgress
            WHERE lab=?
        """, (lab,))
        years, weeks, dates = cursor.fetchone()
        
        return years, weeks, dates 
    
    finally:
        cursor.close()
        conn.close()