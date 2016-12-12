import pymysql
import uuid
import sys
import os
import tempfile
import re

conn = pymysql.connect(host='localhost', port=3306, user='dev_recipe', passwd='devrecipe', db='dev_recipe', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)


# Show stats for the current ingredients missing matches
cur.execute("SELECT IngredientNameModelledShort FROM LearnRecipeIngredient WHERE IngredientNameModelledShortMatched IS NULL")
conn.commit()
for row in cur:
    ingredient = row['IngredientNameModelledShort']
    print ingredient
