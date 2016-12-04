# coding=utf-8
from __future__ import unicode_literals
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

# Select all recipes for import
selectRecipes = """
SELECT 
scrapedrecipe_current.`name`,
scrapedrecipe_current.`scrapedurl`,
`recipeingredientsearchrecord_current`.`ingredientsrequired`,
recipeingredientsearchrecord_current.`ingredientsrequiredcount`
FROM 
scrapedrecipe_current INNER JOIN recipeingredientsearchrecord_current ON scrapedrecipe_current.`scrapedrecipeguid` = `recipeingredientsearchrecord_current`.`scrapedrecipeguid`
ORDER BY scrapedrecipe_current.name ASC
"""

cur.execute(selectRecipes)

i = 1
for row in cur:
	#ingredientList = row['ingredientsrequired'].encode('utf-8')
	#print ingredientList
	#print i, row['ingredientsrequired'].deccode('utf-8')
	doc = {
    'title': row['name'].encode('utf-8'),
    'url': row['scrapedurl'],
    'ingredientsrequired': row['ingredientsrequired'].encode('utf-8'),
    'ingredientsrequiredcount': str(row['ingredientsrequiredcount'])
	}
	i=i+1
	res = es.index(index='recipedb', doc_type='recipe', body=doc)
    #print(row['name'])
#print(res['created'])