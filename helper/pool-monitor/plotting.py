# plotting.py
import matplotlib.pyplot as plt
import pandas as pd
import time

csv_file = "pool_log_"+input(">>>")+".csv"

while True:
    plt.close('all')
    
    try:
        df = pd.read_csv(csv_file, on_bad_lines='skip')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.sort_values('timestamp').reset_index(drop=True)
    except Exception as e:
        print(f"⚠️ 读取CSV失败: {e}，等待重试...")
        time.sleep(60)
        continue

    print(f"✅ 最新数据: {df['timestamp'].iloc[-1]} -> {df['value'].iloc[-1]}")

    # --- 分段逻辑（与之前相同） ---
    max_interval = pd.Timedelta(seconds=15)
    segments = []
    gap_segments = []
    error_segments = []

    start_idx = 0
    for i in range(1, len(df)):
        if df.loc[i, 'timestamp'] - df.loc[i-1, 'timestamp'] > max_interval:
            segments.append(df.iloc[start_idx:i])
            gap_segments.append(df.iloc[i-1:i+1])
            start_idx = i
    segments.append(df.iloc[start_idx:])

    in_error = False
    error_start = 0
    for i in range(len(df)):
        if pd.isna(df.loc[i, 'value']) and not in_error:
            in_error = True
            error_start = i
        elif not pd.isna(df.loc[i, 'value']) and in_error:
            in_error = False
            error_segments.append(df.iloc[error_start:i])
    if in_error:
        error_segments.append(df.iloc[error_start:])

    # --- 绘图 ---
    plt.figure(figsize=(16, 6))

    for seg in segments:
        plt.plot(seg['timestamp'], seg['value'], marker='o', markersize=3, linewidth=1, color='blue')
    for gap in gap_segments:
        plt.plot(gap['timestamp'], gap['value'], marker='o', markersize=3, linewidth=1, color='red')
    for error in error_segments:
        if len(error) > 0:
            start_idx = error.index[0]
            end_idx = error.index[-1]
            prev_value = None
            next_value = None
            if start_idx > 0 and not pd.isna(df.loc[start_idx-1, 'value']):
                prev_value = df.loc[start_idx-1, 'value']
            if end_idx < len(df)-1 and not pd.isna(df.loc[end_idx+1, 'value']):
                next_value = df.loc[end_idx+1, 'value']
            if prev_value is not None and next_value is not None:
                plt.plot([
                    df.loc[start_idx-1, 'timestamp'],
                    df.loc[start_idx, 'timestamp'],
                    df.loc[end_idx, 'timestamp'],
                    df.loc[end_idx+1, 'timestamp']
                ], [
                    prev_value,
                    prev_value,
                    next_value,
                    next_value
                ], color='yellow', linewidth=3, alpha=0.7, marker='o', markersize=3)

    # --- 增强元素 ---
    # plt.axhline(y=1000, color='orange', linestyle='--', linewidth=2, label='Alert Threshold (1000)')
    
    total_points = len(df)
    error_count = df['value'].isna().sum()
    gap_count = len(gap_segments)
    latest_val = df['value'].iloc[-1] if not pd.isna(df['value'].iloc[-1]) else "ERR"
    latest_time = df['timestamp'].iloc[-1]
    plt.text(0.02, 0.98, 
             f"📊 Points: {total_points} | ERR: {error_count} | Gaps: {gap_count} | Latest: {latest_val} @ {latest_time.strftime('%H:%M:%S')}",
             transform=plt.gca().transAxes, 
             verticalalignment='top',
             fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.title("Live CPH Extension Users Over Time (Auto-Refresh)")
    plt.xlabel("Timestamp")
    plt.ylabel("Active Users")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # --- 刷新并等待 ---
    plt.draw()
    plt.pause(60)