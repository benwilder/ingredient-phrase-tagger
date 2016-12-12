import pymysql
import uuid
import sys
import os
import tempfile
import re

conn = pymysql.connect(host='localhost', port=3306, user='dev_recipe', passwd='devrecipe', db='dev_recipe', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)


# Show stats for complete recipes
cur.execute("SELECT r.`RecipeName`, i.`RecipeGuid`, sum(case when i.IngredientNameModelledShortMatched is null then 1 else 0 end) not_matched, count(i.IngredientNameModelledShortMatched) matched FROM LearnRecipeIngredient i JOIN LearnRecipe r ON i.`RecipeGuid` = r.`Guid` GROUP BY RecipeGuid ORDER BY not_matched ASC")
conn.commit()
for row in cur:
    print row['RecipeGuid'] + "\t" + str(row['not_matched']) + "\t" + str(row['matched'])
