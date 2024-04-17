import streamlit as st
from datetime import datetime
import pytz
import sys
sys.path.append('..')
from utils import query_labs, query_period, most_recent_db

def update_cumulative_sums(entries):
    scanned_sum = 0
    linked_sum = 0
    aligned_sum = 0
    for entry in entries:
        scanned_sum += entry["scanned"]
        linked_sum += entry["linked"]
        aligned_sum += entry["aligned"]
    # Display cumulative sums and timestamp
    st.write("Scanned:", scanned_sum)
    st.write("Linked:", linked_sum)
    st.write("Aligned:", aligned_sum)
    st.write("Last change: ", st.session_state["timestamp"])
    return scanned_sum, linked_sum, aligned_sum

def select_lab(db):
    labs = query_labs(db)
    lab = st.selectbox('Select a Laboratory', labs)
    st.write('Selected lab:', lab)
    return lab

def select_period(db, lab):
    years, weeks, dates = query_period(db, lab)
    st.text(dates)
    period = st.selectbox('Period of report:', dates)
    st.write('Selected period:', period)
    return period

def entry(db, lab, period):
    st.subheader("Enter the number of emulsion plates that were scanned, linked and aligned:")
    if "timestamp" not in st.session_state:
        st.session_state["timestamp"] = ""
    if "entries" not in st.session_state:
        st.session_state["entries"] = []
    scanned = st.slider("Scanned", 0, 10, 0)
    linked = st.slider("Linked", 0, 10, 0)
    aligned = st.slider("Aligned", 0, 10, 0)
    # Initialize cumulative sums
    scanned_sum, linked_sum, aligned_sum = update_cumulative_sums(st.session_state["entries"])

    if st.button("Submit entry"):
        timestamp = datetime.now(pytz.timezone('UTC')).strftime("%Y-%m-%d %H:%M:%S %Z%z")
        entry = {"scanned": scanned, "linked": linked, "aligned": aligned, "timestamp": timestamp}
        st.write("Data updated with entry", entry)
        st.session_state["entries"].append(entry)
        st.session_state["timestamp"] = timestamp
        st.success("Entry was successfully submitted.")

def delete_entries():
    # Display previous entries and remove option
    to_delete = []
    st.subheader("Previous entries:")
    for i, entry in enumerate(st.session_state["entries"]):
        remove_entry = st.checkbox(f"Remove Entry {i+1} : {entry}")
        if remove_entry:
            to_delete.append(i)
    if st.button("Delete selected entries"):
        # Remove selected entries in reverse order to avoid index issues
        for index in sorted(to_delete, reverse=True):
            del st.session_state["entries"][index]

        # Update cumulative sums after deleting entries
        scanned_sum, linked_sum, aligned_sum = update_cumulative_sums(st.session_state["entries"])

        st.success("Entries were successfully deleted.")
        st.rerun()
    



if __name__ == '__main__':
    st.title("Shifter Update")
    db_folder = "./data/"
    db = most_recent_db(db_folder)
    lab = select_lab(db)
    period = select_period(db,lab)
    entry(db,lab,period)