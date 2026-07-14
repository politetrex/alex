import os

csv_file = "pool_log_"+input("Compress file: _________\b\b\b\b\b\b\b\b\b")+".csv"
file_exists = os.path.exists(csv_file)
if file_exists:
    level = int(input("Compress level: __\b"))
    