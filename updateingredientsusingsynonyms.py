import pymysql
import uuid
import sys
import os
import tempfile

conn = pymysql.connect(host='localhost', port=3306, user='dev_recipe', passwd='devrecipe', db='dev_recipe', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)
cursynonyms = conn.cursor(pymysql.cursors.DictCursor)
curupdate = conn.cursor(pymysql.cursors.DictCursor)

# Select all ingredients that we have currently captured
# We are going to try to match them against synonyms to normalise them
selectIngredients = "SELECT id, scrapedrecipeguid, modellednameshort FROM scrapedrecipeingredient_current"
cur.execute(selectIngredients)

for row in cur:
    print("Checking for Synonyms for " + row['modellednameshort'])
    modellednameshort = row['modellednameshort']
    ingredientid = row['id']

    # Get the synonyms that match this
    cursynonyms.execute("SELECT name FROM ingredientsynonym WHERE synonym = %s", (modellednameshort,))
    for rowsynonym in cursynonyms:
    	matchedName = rowsynonym['name']
    	print "Found a match to " + matchedName + " adding to record"
    	curupdate.execute("UPDATE scrapedrecipeingredient_current SET  modellednameshortnormalised = %s WHERE id = %s", (matchedName,ingredientid))
        conn.commit()


