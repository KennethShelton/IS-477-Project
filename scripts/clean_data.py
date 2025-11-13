import os
import csv
import re
from datetime import datetime

raw_dir = os.path.join('.', 'data', 'raw')
out_dir = os.path.join('.', 'data', 'processed')
os.makedirs(out_dir, exist_ok=True)

print('Starting basic cleaning: time normalization and negative PM2.5 check')

# 1) Clean air_quality.csv -> normalize time_period/start_date -> add year column
aq_in = os.path.join(raw_dir, 'air_quality.csv')
aq_out = os.path.join(out_dir, 'air_quality_clean.csv')
if os.path.exists(aq_in):
    with open(aq_in, newline='', encoding='utf-8') as inf, open(aq_out, 'w', newline='', encoding='utf-8') as outf:
        reader = csv.DictReader(inf)
        fieldnames = list(reader.fieldnames) + ['year']
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            tp = row.get('Time Period', '') or row.get('time_period', '')
            year = ''
            # try to extract a 4-digit year
            m = re.search(r'(20\d{2})', tp)
            if m:
                year = m.group(1)
            else:
                # fallback: try Start_Date
                sd = row.get('Start_Date', '') or row.get('start_date', '')
                try:
                    year = datetime.strptime(sd, '%m/%d/%Y').year if sd else ''
                except Exception:
                    try:
                        year = datetime.strptime(sd, '%Y-%m-%d').year if sd else ''
                    except Exception:
                        year = ''
            row['year'] = year
            writer.writerow(row)
    print('Wrote', aq_out)
else:
    print('air_quality.csv not found, skipping')

# 2) Basic checks for NYNY_BenMAP.csv -> flag negative PM25-related values and write a subset
ben_in = os.path.join(raw_dir, 'NYNY_BenMAP.csv')
ben_out = os.path.join(out_dir, 'NYNY_BenMAP_clean.csv')
if os.path.exists(ben_in):
    with open(ben_in, newline='', encoding='utf-8') as inf, open(ben_out, 'w', newline='', encoding='utf-8') as outf:
        reader = csv.DictReader(inf)
        fieldnames = reader.fieldnames + ['pm25_negative_flag']
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()
        pm25_cols = [c for c in reader.fieldnames if 'PM25' in c or 'PM2.5' in c]
        for row in reader:
            neg_found = 0
            for c in pm25_cols:
                try:
                    v = float(row.get(c, '') or 0)
                    if v < 0:
                        neg_found += 1
                except Exception:
                    continue
            row['pm25_negative_flag'] = str(neg_found)
            writer.writerow(row)
    print('Wrote', ben_out, '(pm25 negative counts added)')
else:
    print('NYNY_BenMAP.csv not found, skipping')

print('Cleaning completed (basic). Review files in data/processed.')
