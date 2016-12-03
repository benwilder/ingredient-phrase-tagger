import json
import sys
import os
from pprint import pprint

if len(sys.argv) < 2:
    sys.stderr.write('Usage: jsonreader.py FILENAME')
    sys.exit(1)

FILENAME = str(sys.argv[1])

with open(FILENAME) as data_file:    
    data = json.load(data_file)

for i in data['results']:
    if 'name' in i:
        print(i['name'].encode('utf-8'))
    else:
    	print("blank")