# plotting.py
import matplotlib.pyplot as plt
import pandas as pd

csv_file = "pool_log_"+input(">>>")+".csv"

# Read CSV
df = pd.read_csv(csv_file)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['value'] = pd.to_numeric(df['value'], errors='coerce')

print(df)

# Sort just in case
df = df.sort_values('timestamp').reset_index(drop=True)

# Identify gaps (intervals larger than expected)
max_interval = pd.Timedelta(seconds=15)
segments = []
gap_segments = []
error_segments = []

start_idx = 0
for i in range(1, len(df)):
    if df.loc[i, 'timestamp'] - df.loc[i-1, 'timestamp'] > max_interval:
        segments.append(df.iloc[start_idx:i])       # normal segment
        gap_segments.append(df.iloc[i-1:i+1])      # red segment connecting gap
        start_idx = i
segments.append(df.iloc[start_idx:])             # last segment

# IDENTIFY ERROR SEGMENTS (your missing part!)
in_error = False
error_start = 0
for i in range(len(df)):
    if pd.isna(df.loc[i, 'value']) and not in_error:  # ERR becomes NaN
        in_error = True
        error_start = i
    elif not pd.isna(df.loc[i, 'value']) and in_error:
        in_error = False
        error_segments.append(df.iloc[error_start:i])
if in_error:  # Handle errors at the end
    error_segments.append(df.iloc[error_start:])

# Plotting
plt.figure(figsize=(16,6))

# Normal segments (blue)
for seg in segments:
    plt.plot(seg['timestamp'], seg['value'], marker='o', markersize=3, linewidth=1, color='blue')

# Gaps (red)
for gap in gap_segments:
    plt.plot(gap['timestamp'], gap['value'], marker='o', markersize=3, linewidth=1, color='red')

# Errors (yellow) - CONNECTING LINES across error periods
for error in error_segments:
    if len(error) > 0:
        # Get the values before and after the error block
        start_idx = error.index[0]
        end_idx = error.index[-1]
        
        prev_value = None
        next_value = None
        
        # Get value before error
        if start_idx > 0 and not pd.isna(df.loc[start_idx-1, 'value']):
            prev_value = df.loc[start_idx-1, 'value']
        
        # Get value after error  
        if end_idx < len(df)-1 and not pd.isna(df.loc[end_idx+1, 'value']):
            next_value = df.loc[end_idx+1, 'value']
        
        # Draw yellow connecting line if we have both endpoints
        if prev_value is not None and next_value is not None:
            plt.plot([
                df.loc[start_idx-1, 'timestamp'],  # Point before error
                df.loc[start_idx, 'timestamp'],    # Error start
                df.loc[end_idx, 'timestamp'],      # Error end  
                df.loc[end_idx+1, 'timestamp']     # Point after error
            ], [
                prev_value,    # Value before error
                prev_value,    # Hold same value at error start
                next_value,    # Connect to value after error
                next_value     # Value after error
            ], color='yellow', linewidth=3, alpha=0.7, marker='o', markersize=3)

plt.title("Live CPH Extension Users Over Time")
plt.xlabel("Timestamp")
plt.ylabel("Active Users")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()