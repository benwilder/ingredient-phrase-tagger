import pymysql
import uuid
import sys
import os
import tempfile
from ingredient_phrase_tagger.training import utils
import subprocess

conn = pymysql.connect(host='localhost', port=3306, user='dev_recipe', passwd='devrecipe', db='dev_recipe')
cur = conn.cursor(pymysql.cursors.DictCursor)




# Create temp file and put the ingredients in it 
fd, path = tempfile.mkstemp()
inPhrase = utils.export_data_line("16 juniper berry, chopped")
try:
    with os.fdopen(fd, 'w') as tmp:
        # do stuff with temp file
        tmp.write(inPhrase)

	# Specify the model file
	modelFilePath = "tmp/model_file"
	modelFilename = os.path.join(os.path.dirname(__file__), modelFilePath)
	print modelFilename
	print path
	os.system("crf_test -v 1 -m %s %s" % (modelFilename, path))
	#print "crf_test -v 1 -m " + modelFilename + " " + path

finally:
    #os.remove(path)
    print "done"






# Select all ingredients
selectIngredients = "SELECT name FROM scrapedrecipeingredient"
#print insertRecipeString
cur.execute(selectIngredients)
#for row in cur:
    #print(row['name'])
    #os.system("crf_test -v 1 -m %s " % (row['name']))