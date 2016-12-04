import pymysql
import uuid
import sys
import os
import tempfile
from ingredient_phrase_tagger.training import utils
import subprocess
from datetime import datetime
from elasticsearch import Elasticsearch


es = Elasticsearch()
conn = pymysql.connect(host='localhost', port=3306, user='dev_recipe', passwd='devrecipe', db='dev_recipe',charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)

print 'Importing into elastic search'

# Select all ingredients for import
selectIngredients = """
SELECT 
name,displayname,autocompletename
FROM 
recipeingredient_current
"""

cur.execute(selectIngredients)
for row in cur:
	doc = {
    'ingredient': row['name'].encode('utf-8'),
    'ingredientdisplayname': row['displayname'].encode('utf-8'),
    'ingredientautocompletename': row['autocompletename'].encode('utf-8')
	}
	res = es.index(index='ingredientdb', doc_type='ingredient', body=doc)