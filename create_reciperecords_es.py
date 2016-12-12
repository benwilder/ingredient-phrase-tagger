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

print "[1] Creating Recipe records in ES..."

# Select all recipes for import
selectRecipes = """
SELECT 
RecipeName,
IngredientNameModelledShortMatched,
IngredientNameModelledShortMatchedCount,
RecipeUrl
FROM 
ServeRecipe
WHERE IngredientNameModelledShortMatched IS NOT NULL
ORDER BY RecipeName ASC
"""

cur.execute(selectRecipes)

i = 1
for row in cur:
	#ingredientList = row['ingredientsrequired'].encode('utf-8')
	#print ingredientList
	#print i, row['ingredientsrequired'].deccode('utf-8')
	doc = {
    'title': row['RecipeName'].encode('utf-8'),
    'url': row['RecipeUrl'],
    'ingredientsrequired': row['IngredientNameModelledShortMatched'].encode('utf-8'),
    'ingredientsrequiredcount': str(row['IngredientNameModelledShortMatchedCount'])
	}
	i=i+1
	res = es.index(index='recipedb', doc_type='recipe', body=doc)
    #print(row['name'])
#print(res['created'])

print "[1] Created Recipe records in ES"