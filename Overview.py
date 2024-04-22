import streamlit as st
import os

#import sys
#sys.path.append('..')
from src import utils, aggregations, visualizations

if __name__ == '__main__':
    st.title("Overview")
    st.sidebar.success("Select a page above.")
    current_directory = os.getcwd()
    st.text(f"Current directory: {current_directory}")

    db_folder = './data/'  
    db = utils.most_recent_db(db_folder)

    # Make aggregations
    aggregations.aggregate_lab_progress(db)
    aggregations.aggregate_runs_weekly(db)
    aggregations.aggregate_runs(db)

    # Visualize
    st.header('Lab Progress')
    visualizations.visualize(db, table='LabProgress', column1="week", column2="scanned", key1="lab", key2="run")
    st.header('Run Info')
    visualizations.visualize(db, table='RunInfo', column1="wall", column2="num_films", key1="run", key2="lab")
    st.header('Summary Run Info')
    visualizations.visualize_SummaryRunInfo(db)