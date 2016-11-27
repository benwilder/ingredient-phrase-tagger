curl -X GET 'http://localhost:9200/recipedb/_search?pretty' -d '
{
    "query": {
      "function_score": {
        "query": {
          "match": {
            "ingredientsrequired": "avocado lemon chicken thyme"
          }
        },
        "boost_mode": "replace",
        "score_mode": "sum",
        "functions": [
          {
            "filter": {
              "term": {
                "ingredientsrequired": "avocado"
              }
            },
            "weight": 1
          },
          {
           "filter": {
              "term": {
                "ingredientsrequired": "lemon"
              }
            },
            "weight": 1
          },
          {
            "filter": {
             "term": {
                "ingredientsrequired": "chicken"
              }
            },
            "weight": 1
          },
          {
            "filter": {
             "term": {
                "ingredientsrequired": "thyme"
             }
            },
           "weight": 1
          },
          {
            "script_score": {
              "script": "_score - doc[\"ingredientsrequiredcount\"].value"
           }
          }
       ]
      }
   }
}'
