import sys

print("Slicer Activated!")
files = []
fname=None
if (len(sys.argv)<2):
    print("No arguments passed, default /old_logs.")
    fname="/old_logs"
else:
    pargv=sys.argv[2:]
    fname=sys.argv[0]
    