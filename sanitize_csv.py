#!/usr/bin/env python3
import csv
import sys

inp = sys.argv[1]
out = sys.argv[2] if len(sys.argv) == 3 else inp


with open(inp, 'r') as f:
    reader = csv.reader(f)
    data = [row for row in reader]

with open(out, 'w') as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    for row in data:
        writer.writerow(row)
