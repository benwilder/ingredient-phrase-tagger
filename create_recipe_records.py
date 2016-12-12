import pymysql
import uuid
import sys
import os
import tempfile
import re

conn = pymysql.connect(host='localhost', port=3306, user='dev_recipe', passwd='devrecipe', db='dev_recipe', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)

print "[1] Populating recipe table..."
insertRecipes="""
INSERT INTO ServeRecipe (RecipeName,IngredientNameModelledShortMatched,IngredientNameModelledShortMatchedCount,RecipeUrl)
SELECT LearnRecipe.RecipeName, GROUP_CONCAT(LearnRecipeIngredient.`IngredientNameModelledShortMatched` SEPARATOR ' ') as IngredientsRequired, COUNT(LearnRecipeIngredient.`IngredientNameModelledShortMatched`) as IngredientsCount, LearnRecipe.CrawlUrl
FROM LearnRecipeIngredient INNER JOIN LearnRecipe ON LearnRecipeIngredient.`RecipeGuid` = LearnRecipe.`Guid`
GROUP BY LearnRecipeIngredient.`RecipeGuid`
"""
cur.execute(insertRecipes)
conn.commit()
print "[1] Table populated"