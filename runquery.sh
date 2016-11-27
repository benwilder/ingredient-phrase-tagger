curl -X GET 'http://localhost:9200/recipedb/_search?pretty' -d '
{
    "query": {
      "function_score": {
        "query": {
          "match": {
            "ingredientsrequired": "spaghetti freshbasil garlic lemon prawns beef lamb"
          }
        },
        "boost_mode": "replace",
        "score_mode": "sum",
        "functions": [
          {
            "filter": {
              "term": {
                "ingredientsrequired": "spaghetti"
              }
            },
            "weight": 1
          },
          {
           "filter": {
              "term": {
                "ingredientsrequired": "freshbasil"
              }
            },
            "weight": 1
          },
          {
            "filter": {
             "term": {
                "ingredientsrequired": "garlic"
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
               "ingredientsrequired": "prawns"
             }
            },
            "weight": 1
          },
          {
            "filter": {
              "term": {
                "ingredientsrequired": "beef"
              }
           },
            "weight": 1
          },
          {
            "filter": {
              "term": {
                "ingredientsrequired": "lamb"
              }
            },
            "weight": 1
         }
       ]
      }
   }
}'
