import json
from pprint import pprint

with open('out.json') as data_file:    
    data = json.load(data_file)

for i in data['results']:
    if 'name' in i:
        print(i['name'])
    else:
    	print("blank")