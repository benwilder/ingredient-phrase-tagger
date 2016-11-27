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

# Select all recipes for import
selectRecipes = """
SELECT 
scrapedrecipe.`name`,
scrapedrecipe.`scrapedurl`,
`recipeingredientsearchrecord`.`ingredientsrequired`,
recipeingredientsearchrecord.`ingredientsrequiredcount`
FROM 
scrapedrecipe INNER JOIN recipeingredientsearchrecord ON scrapedrecipe.`scrapedrecipeguid` = `recipeingredientsearchrecord`.`scrapedrecipeguid`
ORDER BY scrapedrecipe.name ASC
"""

cur.execute(selectRecipes)
for row in cur:
	doc = {
    'title': row['scrapedurl'],
    'url': row['scrapedurl'],
    'ingredientsrequired': row['ingredientsrequired'],
    'ingredientsrequiredcount': str(row['ingredientsrequiredcount'])
	}
	res = es.index(index='recipedb', doc_type='recipe', body=doc)
    #print(row['name'])
#print(res['created'])