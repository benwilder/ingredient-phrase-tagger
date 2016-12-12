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

print "[1] Creating Ingredient records in ES..."

# Select all ingredients for import
selectIngredients = """
SELECT DisplayName, ShortName FROM ServeRecipeIngredient
"""

cur.execute(selectIngredients)
for row in cur:
	doc = {
    'ingredient': row['ShortName'].encode('utf-8'),
    'ingredientdisplayname': row['DisplayName'].encode('utf-8'),
    'ingredientautocompletename': row['DisplayName'].encode('utf-8')
	}
	res = es.index(index='ingredientdb', doc_type='ingredient', body=doc)

print "[1] Created Ingredient records in ES"