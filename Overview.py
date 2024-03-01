import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

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


if __name__ == '__main__':
    st.title("Overview")
    st.sidebar.success("Select a page above.")
    
    # Return most recent db
    db_folder = './data/'  
    db_files = os.listdir(db_folder)
    db_files = [f for f in db_files if f.startswith('emu_') and f.endswith('.db')] # filter files that don't match
    timestamps = [datetime.strptime(f.split('emu_')[1], "%Y-%m-%d_%H-%M-%S.db") for f in db_files]
    idx_most_recent = timestamps.index(max(timestamps))
    db = os.path.join(db_folder, db_files[idx_most_recent])

    st.header('Lab Progress')
    visualize(db, table='LabProgress', column1="week", column2="scanned", key1="lab", key2="run")
    st.header('Run Info')
    visualize(db, table='RunInfo', column1="wall", column2="num_films", key1="run", key2="lab")
