from AllRecipes.save import Save_db

db = Save_db()
db.save_to_db(debug=True)

del db
