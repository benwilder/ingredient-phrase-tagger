import pymysql
import uuid
import sys
import os
import tempfile

conn = pymysql.connect(host='localhost', port=3306, user='dev_recipe', passwd='devrecipe', db='dev_recipe')
cur = conn.cursor(pymysql.cursors.DictCursor)


tmpFilePath = "tmp/model_file"
inFile = "minimalscrapedingredients.txt"
modelFilename = os.path.join(os.path.dirname(__file__), tmpFilePath)
print modelFilename

os.system("crf_test -v 1 -m %s %s" % (modelFilename, inFile))

# Select all ingredients
selectIngredients = "SELECT name FROM scrapedrecipeingredient"
#print insertRecipeString
cur.execute(selectIngredients)
#for row in cur:
    #print(row['name'])
    #os.system("crf_test -v 1 -m %s " % (row['name']))