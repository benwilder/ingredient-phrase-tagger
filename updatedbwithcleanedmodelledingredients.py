import pymysql
import uuid
import sys
import os
import tempfile
import re

conn = pymysql.connect(host='localhost', port=3306, user='dev_recipe', passwd='devrecipe', db='dev_recipe', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)
curupdate = conn.cursor(pymysql.cursors.DictCursor)

# Select all ingredients that we have currently captured
# We are going to try to clean then up
selectIngredients = "SELECT id, scrapedrecipeguid, modelledname, modellednameshort FROM scrapedrecipeingredient_current"
cur.execute(selectIngredients)

# We want to clean the following
# 
# [heaped]tsp
# tbsp
# [d+][k]g
# pack
# 
#
#
#
updatecounter = 0

for row in cur:
    modelledname = row['modelledname']
    ingredientid = row['id']

    # 
    modellednameclean = re.sub(r'(\d+(\.\d+)?)%', "", modelledname)
    modellednameclean = re.sub(r'(\d+(\.\d+)?) litres', "", modellednameclean)
    modellednameclean = re.sub(r'tub ', "", modellednameclean)
    modellednameclean = re.sub(r'(\d+(\.\d+)?)g', "", modellednameclean)
    modellednameclean = re.sub(r'pack ', "", modellednameclean)
    modellednameclean = re.sub(r'packs ', "", modellednameclean)
    modellednameclean = re.sub(r'x ', "", modellednameclean)
    modellednameclean = re.sub(r'(\d+(\.\d+)?)oz', "", modellednameclean)
    modellednameclean = re.sub(r'(\d+(\.\d+)?)kg', "", modellednameclean)
    modellednameclean = re.sub(r'(\d+(\.\d+)?)ml', "", modellednameclean)
    modellednameclean = re.sub(r'(\d+(\.\d+)?)lb', "", modellednameclean)
    modellednameclean = re.sub(r'(\d+(\.\d+)?)lbs', "", modellednameclean)
    modellednameclean = re.sub(r'(\d+(\.\d+)?)cm', "", modellednameclean)
    modellednameclean = re.sub(r'approx ', "", modellednameclean)

    if len(modelledname) !=len(modellednameclean):
        #print modelledname + " - " + modellednameclean
        updatecounter = updatecounter +1


    	# Update the record
    	curupdate.execute("UPDATE scrapedrecipeingredient_current SET  modelledname = %s WHERE id = %s", (modellednameclean,ingredientid))
        conn.commit()

print updatecounter
