import sqlite3

conn = sqlite3.connect('./data/emu_test.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE LabProgress (
        year     INTEGER,
        week     INTEGER,
        date     TEXT,
        run      TEXT,
        wall     INTEGER,
        lab      TEXT,
        assigned INTEGER,
        scanned  INTEGER,
        linked   INTEGER,
        aligned  INTEGER,
        PRIMARY KEY (
            date,
            run,
            wall,
            lab
        ),
        CONSTRAINT [lab constraint] FOREIGN KEY (
            lab
        )
        REFERENCES SummaryLabProgress (lab),
        CONSTRAINT [date constraint] FOREIGN KEY (
            year,
            week,
            date
        )
        REFERENCES SummaryWeekly (year,
        week,
        date),
        CONSTRAINT [run_wall constraint] FOREIGN KEY (
            run,
            wall
        )
        REFERENCES RunInfo (run,
        wall) 
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS RunInfo (
        run       TEXT,
        wall      INTEGER,
        brick     INTEGER,
        num_films INTEGER,
        emu_type  TEXT,
        lab       TEXT,
        PRIMARY KEY (
            run,
            wall,
            brick,
            num_films,
            emu_type,
            lab
        ),
        CONSTRAINT [lab constraint] FOREIGN KEY (
            lab
        )
        REFERENCES SummaryLabProgress (lab),
        CONSTRAINT [run constraint] FOREIGN KEY (
            run
        )
        REFERENCES SummaryRunInfo (run) 
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS SummaryLabProgress (
        lab      TEXT    PRIMARY KEY,
        assigned INTEGER,
        scanned  INTEGER,
        linked   INTEGER,
        aligned  INTEGER
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS SummaryRunInfo (
        run                 TEXT    PRIMARY KEY,
        start               TEXT,
        end                 TEXT,
        [mass_kg]           REAL,
        [luminosity_inv_fb] REAL,
        [emu_tot]          INTEGER,
        [emu_ntype]        INTEGER,
        [emu_stype]        INTEGER,
        [emu_to_na]         INTEGER,
        [emu_to_bo]         INTEGER,
        [emu_to_cr]         INTEGER,
        [emu_to_le]         INTEGER,
        assigned            INTEGER,
        scanned             INTEGER,
        linked              INTEGER,
        aligned             INTEGER
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS SummaryMonthly (
    month    TEXT    PRIMARY KEY,
    assigned INTEGER,
    scanned  INTEGER,
    linked   INTEGER,
    aligned  INTEGER
    );
""")

cursor.execute("""
    CREATE TABLE SummaryWeekly (
        year     INTEGER,
        week     INTEGER,
        date     TEXT,
        run      INTEGER,
        assigned INTEGER,
        scanned  INTEGER,
        linked   INTEGER,
        aligned  INTEGER,
        PRIMARY KEY (
            date,
            run
        )
    );
""")





# Commit changes and close connection
conn.commit()
conn.close()

print("Database schema created successfully.")
