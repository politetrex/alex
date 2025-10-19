# plotting.py
# You may need to install matplotlib and pandas if not already installed:
# (open Terminal and run)
# pip install matplotlib pandas

import matplotlib.pyplot as plt
import pandas as pd

csv_file = "pool_log.csv"

# Read CSV
df = pd.read_csv(csv_file)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['value'] = pd.to_numeric(df['value'], errors='coerce')

print(df)

# Sort just in case
df = df.sort_values('timestamp').reset_index(drop=True)

# Identify gaps (intervals larger than expected)
max_interval = pd.Timedelta(seconds=15)  # for longer requests, eg. mobile phone hotspots
segments = []
gap_segments = []

start_idx = 0
for i in range(1, len(df)):
    if df.loc[i, 'timestamp'] - df.loc[i-1, 'timestamp'] > max_interval:
        segments.append(df.iloc[start_idx:i])       # normal segment
        gap_segments.append(df.iloc[i-1:i+1])      # red segment connecting gap
        start_idx = i
segments.append(df.iloc[start_idx:])             # last segment

# Plotting
plt.figure(figsize=(16,6))

# Normal segments (blue)
for seg in segments:
    plt.plot(seg['timestamp'], seg['value'], marker='o', markersize=3, linewidth=1, color='blue')

# Gaps (red)
for gap in gap_segments:
    plt.plot(gap['timestamp'], gap['value'], marker='o', markersize=3, linewidth=1, color='red')

plt.title("Live CPH Extension Users Over Time")
plt.xlabel("Timestamp")
plt.ylabel("Active Users")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

#'''