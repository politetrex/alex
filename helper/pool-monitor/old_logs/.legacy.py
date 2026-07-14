import pandas as pd
import csv
csv_file = "./old_logs/pool_log_20250817.csv"
df = pd.read_csv(csv_file, on_bad_lines='skip')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['value'] = pd.to_numeric(df['value'], errors='coerce').astype('Int64')
df = df.sort_values('timestamp').reset_index(drop=True)
print(df)

prev_rd="__FIRST__"
with open("fixed_log_20250817.csv", "w", newline="") as f:
    writer=csv.writer(f)
    writer.writerow(["timestamp","value"])
    batch=[]
    for i in range(0, len(df)):
        rd=str(df.loc[i, 'timestamp'])
        if (prev_rd!=rd and prev_rd!="__FIRST__"):
            itv=60//len(batch)
            ird=0
            for j in batch:
                writer.writerow([j[0][:len(rd)-2]+f"{ird:02d}",j[1]])
                ird+=itv
            batch=[[rd, str(df.loc[i, 'value'])]]
        else:
            batch.append([rd, str(df.loc[i, 'value'])])
        prev_rd=rd
    itv=60//len(batch)
    ird=0
    for j in batch:
        writer.writerow([j[0][:len(rd)-2]+f"{ird:02d}",j[1]])
        ird+=itv