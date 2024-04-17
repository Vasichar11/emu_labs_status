import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('..')
from utils import most_recent_db 
from aggregations import aggregate_lab_progress, aggregate_runs_weekly, aggregate_runs
import numpy as np


def visualize(db, table, column1, column2, key1, key2):
    conn = sqlite3.connect(db)
    
    # Retrieve unique values for the key
    allowed_selections1 = pd.read_sql_query(f"SELECT DISTINCT {key1} FROM {table}", conn)[key1].tolist()
    allowed_selections2 = pd.read_sql_query(f"SELECT DISTINCT {key2} FROM {table}", conn)[key2].tolist()
    # Generate unique keys for the select boxes
    id_selectionbox1 = f"{table}_{key1}_selectbox"
    id_selectionbox2 = f"{table}_{key2}_selectbox"
    selection1 = st.selectbox(f'Select {key1}', allowed_selections1, key=id_selectionbox1)
    selection2 = st.selectbox(f'Select {key2}', allowed_selections2, key=id_selectionbox2)


    # Fetch data based on the selected key1
    cursor = conn.cursor()
    cursor.execute(f"SELECT {column1}, {column2} FROM {table} WHERE {key1} = ? AND {key2} = ?", (selection1, selection2))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert fetched data into DataFrame
    df = pd.DataFrame(rows, columns=[column1, column2])
    df = df.replace('', pd.NA) # replace empty strings with NANs
    df = df.fillna(0) # replace NANs with 0s
    
    # Generate a unique key for the radio button
    radio_key = f"{table}_{key1}_{key2}_radio"
    
    # Option for Chart or Table
    display_option = st.radio(f"Display Option", ["Chart", "Table"], key=radio_key)
    
    # Plotting or showing table based on selected option
    if display_option == "Chart":
        # Plotting
        plt.bar(df[column1], df[column2])
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title(f'{selection1} / {selection2}')
        st.pyplot(plt)
    else:
        # Displaying as table
        st.write(df)


def visualize_SummaryRunInfo(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Query the data
    c.execute("SELECT run, assigned, scanned, linked, aligned FROM SummaryRunInfo")
    data = c.fetchall()

    # Extracting data for visualization
    runs = [row[0] for row in data]
    assigned = [row[1] if row[1] is not None else 0 for row in data]
    scanned = [row[2] if row[2] is not None else 0 for row in data]
    linked = [row[3] if row[3] is not None else 0 for row in data]
    aligned = [row[4] if row[4] is not None else 0 for row in data]

    # Streamlit radio button to choose display option
    display_option = st.radio("Display Option", ["Chart", "Table"])

    if display_option == "Chart":
        # Multiselect to select data series
        selected_series = st.multiselect("Select data series to visualize:", 
                                         ["Assigned", "Scanned", "Linked", "Aligned"],
                                         ["Assigned", "Scanned", "Linked", "Aligned"])

        # Plotting the bar chart with increased size
        fig, ax = plt.subplots(figsize=(10, 8))
        index = np.arange(len(runs))
        bar_width = 0.2
        opacity = 0.8

        if "Assigned" in selected_series:
            rects1 = plt.barh(index, assigned, bar_width, alpha=opacity, color='b', label='Assigned')
            for i, v in enumerate(assigned):
                if v != 0:
                    plt.text(v, i, str(v), color='black', va='center', fontsize=10, fontweight='bold')
        if "Scanned" in selected_series:
            rects2 = plt.barh(index + bar_width, scanned, bar_width, alpha=opacity, color='g', label='Scanned')
            for i, v in enumerate(scanned):
                if v != 0:
                    plt.text(v, i + bar_width, str(v), color='black', va='center', fontsize=10, fontweight='bold')
        if "Linked" in selected_series:
            rects3 = plt.barh(index + 2*bar_width, linked, bar_width, alpha=opacity, color='r', label='Linked')
            for i, v in enumerate(linked):
                if v != 0:
                    plt.text(v, i + 2*bar_width, str(v), color='black', va='center', fontsize=10, fontweight='bold')
        if "Aligned" in selected_series:
            rects4 = plt.barh(index + 3*bar_width, aligned, bar_width, alpha=opacity, color='y', label='Aligned')
            for i, v in enumerate(aligned):
                if v != 0:
                    plt.text(v, i + 3*bar_width, str(v), color='black', va='center', fontsize=10, fontweight='bold')

        plt.xlabel('Number of Emulsion Films')
        plt.ylabel('Run ID')
        plt.title('Summary Run Info')
        plt.yticks(index + bar_width * 1.5, runs)
        plt.legend()
        plt.gca().invert_yaxis()  # Invert the vertical axis
        plt.tight_layout()
        st.pyplot(fig)
    elif display_option == "Table":
        df = pd.DataFrame(data, columns=['Run ID', 'Assigned', 'Scanned', 'Linked', 'Aligned'])
        st.write(df)

    conn.close()

if __name__ == '__main__':
    st.title("Overview")
    st.sidebar.success("Select a page above.")
    
    db_folder = './data/'  
    db = most_recent_db(db_folder)

    # Make aggregations
    aggregate_lab_progress(db)
    aggregate_runs_weekly(db)
    aggregate_runs(db)

    # Visualize
    st.header('Lab Progress')
    visualize(db, table='LabProgress', column1="week", column2="scanned", key1="lab", key2="run")
    st.header('Run Info')
    visualize(db, table='RunInfo', column1="wall", column2="num_films", key1="run", key2="lab")
    st.header('Summary Run Info')
    visualize_SummaryRunInfo(db)