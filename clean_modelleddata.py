import pymysql
import uuid
import sys
import os
import tempfile
import re

conn = pymysql.connect(host='localhost', port=3306, user='dev_recipe', passwd='devrecipe', db='dev_recipe', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)
cursynonyms = conn.cursor(pymysql.cursors.DictCursor)
curupdate = conn.cursor(pymysql.cursors.DictCursor)

# Update the Ingredients by removing the spaces
print "[1] Removing spaces..."
cur.execute("UPDATE LearnRecipeIngredient SET IngredientNameModelledShort = REPLACE( `IngredientNameModelled`, ' ', '')")
conn.commit()
print "[1] Spaces removed..."

# Get all ingredients
print "[2] Cleaning ingredients..."
selectIngredients = "SELECT Guid, IngredientNameModelledShort FROM LearnRecipeIngredient"
cur.execute(selectIngredients)

# We want to clean the following
updatecounter = 0

for row in cur:
    modelledname = row['IngredientNameModelledShort']
    ingredientid = row['Guid']

    # Perform cleaning
    modellednameclean = re.sub(r'(\d+(\.\d+)?)%', "", modelledname)
    modellednameclean = re.sub(r'(\d+(\.\d+)?)litres', "", modellednameclean)
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
        updatecounter = updatecounter +1
        # Update the record
        curupdate.execute("UPDATE LearnRecipeIngredient SET  IngredientNameModelledShort = %s WHERE Guid = %s", (modellednameclean,ingredientid))
        conn.commit()

print "[2] Cleaned ingredients (" + str(updatecounter) + ")..."


# We are going to try to match them against synonyms to normalise them
print "[3] Matching ingredients..."
selectAllIngredients = "SELECT Guid, IngredientNameModelledShort FROM LearnRecipeIngredient"
cur.execute(selectAllIngredients)

for row in cur:
    modellednameshort = row['IngredientNameModelledShort']
    ingredientid = row['Guid']

    # Get the synonyms that match this
    cursynonyms.execute("SELECT name FROM ingredientsynonym WHERE synonym = %s", (modellednameshort,))
    for rowsynonym in cursynonyms:

    	# Where we find a match, update the master record
    	matchedName = rowsynonym['name']
    	#print "Found a match to " + matchedName + " adding to record"
    	curupdate.execute("UPDATE LearnRecipeIngredient SET  IngredientNameModelledShortMatched = %s WHERE Guid = %s", (matchedName,ingredientid))
        conn.commit()

print "[3] Matched ingredients..."