import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

def main():
    st.title('Enter Table Information')
    
    # Sample data
    data = pd.DataFrame({
        'WALL': [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5],
        'BRICK': [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4],
        'NUM_FILMS': [60, 60, 60, 60, 57, 57, 57, 57, 60, 60, 60, 60, 57, 57, 57, 57, 57, 60, 60, 60],
        'EMU_TYPE': ['S', 'S', 'S', 'S', 'N', 'N', 'N', 'N', 'S', 'S', 'S', 'S', 'N', 'N', 'N', 'N', 'N', 'S', 'S', 'S'],
        'LAB': ['LB', 'LB', 'LB', 'LB', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'CR', 'CR', 'CR', 'CR', 'BO', 'BO', 'BO', 'BO']
    })

    # Grid options
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_default_column(groupable=True, value=True, editable=True)
    
    # Define dropdown options for the 'EMU_TYPE' column
    gb.configure_column("EMU_TYPE", editable=True, 
                        cellEditor="agSelectCellEditor",
                        cellEditorParams={
                            "values": ["S", "N"]
                        })

    # Define dropdown options for the 'LAB' column
    labs = ["LB", "CR", "NA", "BO"]
    gb.configure_column("LAB", editable=True, 
                        cellEditor="agSelectCellEditor",
                        cellEditorParams={
                            "values": labs
                        })
    
    # Define dropdown options for the 'WALL' and 'BRICK' columns
    gb.configure_column("WALL", editable=True, 
                        cellEditor="agSelectCellEditor",
                        cellEditorParams={
                            "values": list(range(1, 6))
                        })
    gb.configure_column("BRICK", editable=True, 
                        cellEditor="agSelectCellEditor",
                        cellEditorParams={
                            "values": list(range(1, 5))
                        })
    
    grid_options = gb.build()

    # Display the grid
    grid_response = AgGrid(data, gridOptions=grid_options, editable=True)

    # Button to get edited data
    if st.button("Get Edited Data"):
        st.write(grid_response["data"])

if __name__ == "__main__":
    main()
