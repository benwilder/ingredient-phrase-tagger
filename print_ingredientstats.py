import pymysql
import uuid
import sys
import os
import tempfile
import re

conn = pymysql.connect(host='localhost', port=3306, user='dev_recipe', passwd='devrecipe', db='dev_recipe', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)


# Show stats for the current ingredients
cur.execute("SELECT COUNT(*) as 'count' FROM LearnRecipeIngredient")
conn.commit()
for row in cur:
    total = row['count']
    print "Total Ingredients: " + str(total)

cur.execute("SELECT COUNT(*) as 'count' FROM LearnRecipeIngredient WHERE IngredientNameModelledShort = 'blank'")
conn.commit()
for row in cur:
    total = row['count']
    print "Total Ingredients with blank model match: " + str(total)

cur.execute("SELECT COUNT(*) as 'count' FROM LearnRecipeIngredient WHERE IngredientNameModelledShortMatched IS NULL")
conn.commit()
for row in cur:
    total = row['count']
    print "Total Ingredients with null match: " + str(total)
