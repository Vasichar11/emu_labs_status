import sqlite3

def aggregate_lab_progress(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Fetch data from the LabProgress table and aggregate values for each lab
    cursor.execute("""
        SELECT lab,
               SUM(assigned) AS total_assigned,
               SUM(scanned) AS total_scanned,
               SUM(linked) AS total_linked,
               SUM(aligned) AS total_aligned
        FROM LabProgress
        GROUP BY lab
    """)
    aggregated_data = cursor.fetchall()

    # Insert or update aggregated values into the SummaryLabProgress table
    for lab_data in aggregated_data:
        lab, assigned, scanned, linked, aligned = lab_data
        cursor.execute("""
            INSERT OR REPLACE INTO SummaryLabProgress (lab, assigned, scanned, linked, aligned)
            VALUES (?, ?, ?, ?, ?)
        """, (lab, assigned, scanned, linked, aligned))

    # Calculate sum for 'TOT' row
    cursor.execute("""
        INSERT OR REPLACE INTO SummaryLabProgress (lab, assigned, scanned, linked, aligned)
        SELECT 'TOT', SUM(assigned), SUM(scanned), SUM(linked), SUM(aligned)
        FROM LabProgress
    """)
    
    conn.commit()
    conn.close()

def aggregate_runs_weekly(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Select distinct combinations of year, week, and run from LabProgress table
    cursor.execute("SELECT DISTINCT year, week, run FROM LabProgress")
    rows = cursor.fetchall()

    for row in rows:
        year, week, run = row

        # Calculate cumulative assigned, scanned, linked, and aligned for each year, week and run
        cursor.execute("""
            SELECT 
                SUM(assigned), 
                SUM(scanned), 
                SUM(linked), 
                SUM(aligned) 
            FROM 
                LabProgress 
            WHERE 
                year = ? AND week = ? AND run = ?
        """, (year, week, run))

        aggregated_data = cursor.fetchone()

        # Update SummaryWeekly table with calculated aggregated_data
        cursor.execute("""
            UPDATE SummaryWeekly 
            SET 
                assigned = ?, 
                scanned = ?, 
                linked = ?, 
                aligned = ? 
            WHERE 
                year = ? AND week = ? AND run = ?
        """, (aggregated_data[0], aggregated_data[1], aggregated_data[2], aggregated_data[3], year, week, run))

    conn.commit()
    conn.close()

    
def aggregate_runs(db):

    aggregate_runs_weekly(db) # Ensure that weekly summary is updated since the aggregation is from there 
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Select distinct runs from SummaryWeekly table
    cursor.execute("SELECT DISTINCT run FROM SummaryWeekly")
    runs = cursor.fetchall()

    for run in runs:
        run_id = run[0]

        # Calculate aggregates for assigned, scanned, linked, and aligned
        cursor.execute("""
            SELECT 
                SUM(assigned), 
                SUM(scanned), 
                SUM(linked), 
                SUM(aligned) 
            FROM 
                SummaryWeekly 
            WHERE 
                run = ?
        """, (run_id,))

        aggregates = cursor.fetchone()

        # Update SummaryRunInfo table with calculated aggregates
        cursor.execute("""
            UPDATE SummaryRunInfo 
            SET 
                assigned = ?, 
                scanned = ?, 
                linked = ?, 
                aligned = ? 
            WHERE 
                run = ?
        """, (aggregates[0], aggregates[1], aggregates[2], aggregates[3], run_id))
    
    conn.commit()
    conn.close()
