import streamlit as st
import sqlite3
import os
from datetime import datetime, timedelta


def get_latest_run_name(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(CAST(SUBSTR(run, 4) AS INTEGER)) FROM SummaryRunInfo")
    latest_run_number = cursor.fetchone()[0]
    conn.close()
    new_run_number = latest_run_number + 1 if latest_run_number is not None else 0
    return f"RUN{new_run_number}"

def calc_stype():
    st.session_state.stype = st.session_state.emu_tot-st.session_state.ntype
def calc_ntype():
    st.session_state.ntype = st.session_state.emu_tot-st.session_state.stype

def add_run(db, newdb):
    st.subheader("Add New Run")
    run = get_latest_run_name(db)
    st.write(f"Adding {run}")

    col1, col2 = st.columns([1,1])
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now())
        mass = st.number_input("Mass (kg)")
    with col2:
        end_date = st.date_input("End Date", value=datetime.now()+timedelta(days=90), min_value=start_date)
        luminosity = st.number_input("Luminosity (fb-1)")
    
    st.session_state.emu_tot = st.number_input("Total number of emulsions", value=0)

    if "ntype" not in st.session_state:
        st.session_state.ntype = 0
    if "stype" not in st.session_state:
        st.session_state.stype = 0

    st.caption("Emulsion types:")
  
    col3, col4 = st.columns([1,1])
    with col3:
        emu_ntype = st.number_input("Number of Nagoya films", key="ntype", min_value=0, max_value=st.session_state.emu_tot, value=int(st.session_state.emu_tot/2)+(st.session_state.emu_tot%2), on_change=calc_stype)
    with col4:
        emu_stype = st.number_input("Number of Nagoya films", key="stype", min_value=0, max_value=st.session_state.emu_tot, value=int(st.session_state.emu_tot/2), on_change=calc_ntype)    
    emu_remaining1 = st.session_state.emu_tot-emu_stype-emu_ntype
    if emu_remaining1 > 0 :
        st.error(f"{emu_remaining1} films remain for distribution. Please distribute accordingly.")
    elif emu_remaining1 < 0:
        st.error(f"Distribution exceeded {-emu_remaining1} films. Please distribute accordingly.")

    st.caption("Distributions:")
    emu_to_na = st.number_input("Distribution to NA", min_value=0, max_value=st.session_state.emu_tot, value=int(st.session_state.emu_tot/4)+(st.session_state.emu_tot%4), placeholder=f"Remaining films: {int(st.session_state.emu_tot/4)+(st.session_state.emu_tot%4)}")
    emu_to_bo = st.number_input("Distribution to BO", min_value=0, max_value=st.session_state.emu_tot, value=int((st.session_state.emu_tot-emu_to_na)/3)+((st.session_state.emu_tot-emu_to_na)%3), placeholder=f"Remaining films: {int((st.session_state.emu_tot-emu_to_na)/3)+((st.session_state.emu_tot-emu_to_na)%3)}")
    emu_to_cr = st.number_input("Distribution to CR", min_value=0, max_value=st.session_state.emu_tot, value=int((st.session_state.emu_tot-emu_to_na-emu_to_bo)/2)+((st.session_state.emu_tot-emu_to_na-emu_to_bo)%2), placeholder=f"Remaining films: {int((st.session_state.emu_tot-emu_to_na-emu_to_bo)/2)+((st.session_state.emu_tot-emu_to_na-emu_to_bo)%2)}")
    emu_to_le = st.number_input("Distribution to LE", min_value=0, max_value=st.session_state.emu_tot-emu_to_na-emu_to_bo-emu_to_cr, value=st.session_state.emu_tot-emu_to_na-emu_to_bo-emu_to_cr, placeholder=f"Remaining films: {st.session_state.emu_tot - emu_to_na - emu_to_bo - emu_to_cr}")
    emu_remaining2 = st.session_state.emu_tot-emu_to_na-emu_to_bo-emu_to_cr-emu_to_le
    if emu_remaining2>0 :
        st.error(f"{emu_remaining2} films remain for distribution. Please distribute accordingly.")
    elif emu_remaining2<0 :
        st.error(f"Distribution exceeded {-emu_remaining2} films. Please distribute accordingly.")

    assigned = 0 # TODO to be calculated
    scanned = 0 # TODO to be calculated
    linked = 0 # TODO to be calculated
    aligned = 0 # TODO to be calculated
    
    if st.button("Add Run"):
        conn = sqlite3.connect(newdb)
        cursor = conn.cursor()
        try:
            # Copy structure and data from the original DB to new DB
            with sqlite3.connect(db) as src_conn:
                src_conn.backup(conn)
            # Insert new run
            cursor.execute("""
                INSERT INTO SummaryRunInfo 
                (run, start, end, [mass_kg], [luminosity_inv_fb], [emu_tot], 
                [emu_ntype], [emu_stype], [emu_to_na], [emu_to_bo], [emu_to_cr], 
                [emu_to_le], assigned, scanned, linked, aligned)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (run, start_date, end_date, mass, luminosity, st.session_state.emu_tot, emu_ntype, emu_stype, 
                  emu_to_na, emu_to_bo, emu_to_cr, emu_to_le, assigned, scanned, 
                  linked, aligned))
            conn.commit()
            st.success("Run added successfully.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()

if __name__ == '__main__':
    st.title("Add New Run")

    # Return most recent db
    db_folder = './data/'  
    db_files = os.listdir(db_folder)
    if len(db_files) == 1: 
        db = os.path.join(db_folder, db_files[0])
    else:

        db_files = [f for f in db_files if f.startswith('emu_') and f.endswith('.db')] # filter files that don't match
        timestamps = [datetime.strptime(f.split('emu_')[1], "%Y-%m-%d_%H-%M-%S.db") for f in db_files]
        idx_most_recent = timestamps.index(max(timestamps))
        db = os.path.join(db_folder, db_files[idx_most_recent])

    # Update db and save with a new datetime filename 
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    newdb = os.path.join(db_folder, f"emu_{current_datetime}.db")

    add_run(db, newdb)
