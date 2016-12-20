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

# Get all the ingredients so that we can clean them up
print "[1] Getting and cleaning ingredients..."
selectIngredients = "SELECT Guid, IngredientNameModelled FROM LearnRecipeIngredient"
cur.execute(selectIngredients)

for row in cur:
    modelledname = row['IngredientNameModelled']
    ingredientid = row['Guid']

    # Perform cleaning
    modellednameclean = re.sub(r'(\d+(\.\d+)?)%', "", modelledname)
    modellednameclean = re.sub(r'(\d+(\.\d+)?)litres', "", modellednameclean)
    modellednameclean = re.sub(r'tub ', "", modellednameclean)
    modellednameclean = re.sub(r'tsp ', "", modellednameclean)
    modellednameclean = re.sub(r'pot ', "", modellednameclean)
    modellednameclean = re.sub(r'carton ', "", modellednameclean)
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


    # Update the record
    curupdate.execute("UPDATE LearnRecipeIngredient SET  IngredientNameModelledClean = %s WHERE Guid = %s", (modellednameclean,ingredientid))
    conn.commit()

print "[1] Cleaned ingredients"

# Remove spaces from the ingredients
print "[2] Removing spaces..."
cur.execute("UPDATE LearnRecipeIngredient SET IngredientNameModelledCleanShort = REPLACE( `IngredientNameModelledClean`, ' ', '')")
conn.commit()
print "[2] Spaces removed"



# We are going to try to match them against synonyms to normalise them
print "[3] Matching ingredients..."
selectAllIngredients = "SELECT Guid, IngredientNameModelledCleanShort FROM LearnRecipeIngredient"
cur.execute(selectAllIngredients)

for row in cur:
    modellednameshort = row['IngredientNameModelledCleanShort']
    ingredientid = row['Guid']

    # Get the synonyms that match this
    cursynonyms.execute("SELECT ShortName FROM LearnRecipeIngredientSynonym WHERE ShortNameSynonym = %s", (modellednameshort,))
    for rowsynonym in cursynonyms:

    	# Where we find a match, update the master record
    	matchedName = rowsynonym['ShortName']
    	#print "Found a match to " + matchedName + " adding to record"
    	curupdate.execute("UPDATE LearnRecipeIngredient SET  IngredientNameMatched = %s WHERE Guid = %s", (matchedName,ingredientid))
        conn.commit()

print "[3] Matched ingredients"

print "[4] Marking Recipes complete..."

# Mark all recipes as invalid
curupdate.execute("UPDATE LearnRecipe SET IsReadyForServing = 0")
conn.commit()

# Now update all recipes if they have a full set of matched ingredients
updateAllRecipes = """
UPDATE LearnRecipe INNER JOIN 
(SELECT LearnRecipeIngredient.`RecipeGuid`, (COUNT(LearnRecipeIngredient.`Guid`) - SUM(CASE WHEN LearnRecipeIngredient.`IngredientNameMatched` IS NOT NULL THEN 1 ELSE 0 END)) as MissingIngredients
FROM 
LearnRecipeIngredient
GROUP BY LearnRecipeIngredient.RecipeGuid
HAVING MissingIngredients =0
ORDER BY MissingIngredients ASC) Ings ON LearnRecipe.`Guid` = Ings.RecipeGuid 
SET LearnRecipe.`IsReadyForServing` =1
"""
cur.execute(updateAllRecipes)
conn.commit()

print "[4] Marked recipes complete"


print "[5] Printing stats..."

selectStats = """
SELECT COUNT(LearnRecipe.`Guid`) as Total, SUM(CASE WHEN LearnRecipe.`IsReadyForServing` = 1 THEN 1 ELSE 0 END) Complete, (SUM(CASE WHEN LearnRecipe.`IsReadyForServing` = 1 THEN 1 ELSE 0 END) / COUNT(LearnRecipe.`Guid`) *100) as Percentage
FROM
LearnRecipe
"""
cur.execute(selectStats)

for row in cur:
    statsTotal = row['Total']
    statsComplete = row['Complete']
    statsPercentage = row['Percentage']

    print "[5] Stats - Total: " + str(statsTotal) + " Complete: " + str(statsComplete) + " Percentage: " + str(statsPercentage) + "%"