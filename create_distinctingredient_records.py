import pymysql
import uuid
import sys
import os
import tempfile
import re

conn = pymysql.connect(host='localhost', port=3306, user='dev_recipe', passwd='devrecipe', db='dev_recipe', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)

print "[1] Truncating distinct ingredient tables..."
cur.execute("TRUNCATE TABLE ServeRecipeIngredient")
conn.commit()
print "[1] Tables truncated"

print "[2] Populating distinct ingredient tables..."
cur.execute("INSERT INTO ServeRecipeIngredient (DisplayName,ShortName) SELECT DISTINCT(DisplayName), ShortName FROM LearnRecipeIngredientSynonym ORDER BY DisplayName ASC")
conn.commit()
print "[2] Tables populated"