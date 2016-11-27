import json
from pprint import pprint

with open('bbcgoodfood_1000_export_results.json') as data_file:    
    data = json.load(data_file)

for i in data['results']:
    if 'name' in i:
        print(i['name'])
    else:
    	print("blank")