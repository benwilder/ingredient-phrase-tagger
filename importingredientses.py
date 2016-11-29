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
conn = pymysql.connect(host='localhost', port=3306, user='dev_recipe', passwd='devrecipe', db='dev_recipe')
cur = conn.cursor(pymysql.cursors.DictCursor)

print 'Importing into elastic search'

# Select all ingredients for import
selectIngredients = """
SELECT 
name,displayname,autocompletename
FROM 
recipeingredient
"""

cur.execute(selectIngredients)
for row in cur:
	doc = {
    'ingredient': row['name'],
    'ingredientdisplayname': row['displayname'],
    'ingredientautocompletename': row['autocompletename']
	}
	res = es.index(index='recipedb', doc_type='ingredient', body=doc)