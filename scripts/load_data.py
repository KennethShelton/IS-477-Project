import os
import sqlite3
import sys
import traceback
import csv

# Simple, top-level import script that prefers pandas but falls back to csv+sqlite for small files.
db_path = os.path.join('.', 'data', 'nyc_air_health.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

print('Creating/opening database at', db_path)
conn = sqlite3.connect(db_path)

# try pandas first (faster for large CSVs)
try:
    import pandas as pd
    print('Using pandas to import CSVs (fast).')
    # import air_quality
    aq_path = os.path.join('.', 'data', 'raw', 'air_quality.csv')
    if os.path.exists(aq_path):
        print('Loading', aq_path)
        for chunk in pd.read_csv(aq_path, chunksize=200000):
            chunk.to_sql('air_quality', conn, if_exists='append', index=False)
        print('Imported air_quality')
    else:
        print('air_quality.csv not found at', aq_path)

    # import benmap
    ben_path = os.path.join('.', 'data', 'raw', 'NYNY_BenMAP.csv')
    if os.path.exists(ben_path):
        print('Loading', ben_path)
        for chunk in pd.read_csv(ben_path, chunksize=200000):
            chunk.to_sql('benmap', conn, if_exists='append', index=False)
        print('Imported benmap')
    else:
        print('NYNY_BenMAP.csv not found at', ben_path)

except Exception:
    print('pandas import failed or not available, falling back to CSV reader')
    try:
        cur = conn.cursor()
        # create simple air_quality table if not exists
        cur.execute('''
        CREATE TABLE IF NOT EXISTS air_quality (
          unique_id INTEGER,
          indicator_id INTEGER,
          name TEXT,
          measure TEXT,
          measure_info TEXT,
          geo_type_name TEXT,
          geo_join_id TEXT,
          geo_place_name TEXT,
          time_period TEXT,
          start_date TEXT,
          data_value REAL,
          message TEXT
        )
        ''')
        conn.commit()

        aq_path = os.path.join('.', 'data', 'raw', 'air_quality.csv')
        if os.path.exists(aq_path):
            with open(aq_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                ins_q = 'INSERT INTO air_quality VALUES (%s)' % ','.join(['?'] * len(header))
                batch = []
                for i, row in enumerate(reader, 1):
                    batch.append(row)
                    if i % 10000 == 0:
                        cur.executemany(ins_q, batch)
                        conn.commit()
                        batch = []
                if batch:
                    cur.executemany(ins_q, batch)
                    conn.commit()
            print('Imported air_quality via csv reader')

        ben_path = os.path.join('.', 'data', 'raw', 'NYNY_BenMAP.csv')
        if os.path.exists(ben_path):
            with open(ben_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                # create table with dynamic columns
                cols = [f'"{c}" TEXT' for c in header]
                cur.execute('DROP TABLE IF EXISTS benmap')
                cur.execute('CREATE TABLE benmap (' + ','.join(cols) + ')')
                conn.commit()
                ins_q = 'INSERT INTO benmap VALUES (%s)' % ','.join(['?'] * len(header))
                batch = []
                for i, row in enumerate(reader, 1):
                    batch.append(row)
                    if i % 5000 == 0:
                        cur.executemany(ins_q, batch)
                        conn.commit()
                        batch = []
                if batch:
                    cur.executemany(ins_q, batch)
                    conn.commit()
            print('Imported benmap via csv reader')

    except Exception:
        print('Fallback import failed')
        print(traceback.format_exc())

conn.close()
print('Done.')
