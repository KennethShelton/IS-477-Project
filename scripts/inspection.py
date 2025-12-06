import os
import sys
import csv
import traceback

out_lines = []

files = [r".\data\raw\NYNY_BenMAP.csv", r".\data\raw\air_quality.csv"]
for fn in files:
    out_lines.append(f"File: {fn}")
    if not os.path.exists(fn):
        out_lines.append("  MISSING")
        out_lines.append("-")
        continue
    try:
        # fast header + sample
        with open(fn, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            out_lines.append(f"  Columns: {len(header)}")
            out_lines.append("  First 20 column names: " + ", ".join(header[:20]))
            sample = []
            for i, row in enumerate(reader):
                if i >= 4:
                    break
                sample.append(row)
        out_lines.append("  Sample rows (up to 5):")
        for r in sample:
            out_lines.append("    " + ", ".join(r[:10]) + ("..." if len(r) > 10 else ""))

        # approximate row count (fast, binary read)
        count = 0
        with open(fn, 'rb') as f:
            for chunk in f:
                count += chunk.count(b'\n')
        out_lines.append(f"  Approx rows (including header): {count}")

    except Exception:
        out_lines.append("  ERROR reading file")
        out_lines.append(traceback.format_exc())
    out_lines.append("-")

# write report
rep_dir = os.path.join('.', 'docs')
os.makedirs(rep_dir, exist_ok=True)
rep_path = os.path.join(rep_dir, 'inspect_report.txt')
with open(rep_path, 'w', encoding='utf-8') as out:
    out.write('\n'.join(out_lines))

print(f"Wrote inspection report to {rep_path}")
