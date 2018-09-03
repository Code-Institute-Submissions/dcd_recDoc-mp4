import os
from flask import Flask, redirect, render_template, request, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import pymongo
import json
from bson import json_util

app = Flask(__name__)
app.secret_key = 'some_secret'
#configure the application to link to the database
app.config["MONGO_DBNAME"] = 'recipe_book'
app.config["MONGO_URI"] = 'mongodb://recipes:18Recipes18@ds115592.mlab.com:15592/recipe_book'
#create an instance (constructor method) of pymongo
mongo = PyMongo(app)

# Route for handling the login page logic
# login is the default route when app is run
@app.route('/', methods=['GET', 'POST'])
@app.route('/login')
def login():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('login.html')
# route for home page    
@app.route('/index')                                             
def index():
    return render_template("index.html", recipes=mongo.db.recipes.find())
    
# function to locate the categories and display
@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.categories.find()) 
    
# function to display the editing form
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('edit_category.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))

# function to carry out edit on the database (write to the database)
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form['category_name']})
    return redirect(url_for('get_categories'))
    
# function to delete a category  
@app.route('/delete_category/<category_id>')  
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for("get_categories"))
    
#function to display the form view to insert new data into
@app.route('/new_category')
def new_category():
    return render_template('add_category.html')

# function to insert a new category into the DB  
@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form['category_name']}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))
    
# function to locate the recipes and display
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find())
    
#function to display blank form bound to the categories
@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html',
    categories=mongo.db.categories.find())
    
# function to write the data to the DB
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes =  mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))
    #return redirect(url_for('index'))
    
# function to display the editing form
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('edit_recipe.html', recipe=the_recipe, categories=all_categories)
    
# function to remove a recipe from the db
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))
    
#function to update the database once edited
@app.route('/update_recipe/<recipe_id>', methods=["GET", "POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'Recipe_name':request.form['Recipe_name'],
        'category_name':request.form['category_name'],
        'Total_time': request.form['Total_time'],
        'Prep_time': request.form['Prep_time'],
        'Cooking_time': request.form['Cooking_time'],
        'Suitable_for_Vegetarians': request.form['Suitable_for_Vegetarians'],
        'Suitable_for_Vegans': request.form['Suitable_for_Vegans'],
        'Ingredients': request.form['Ingredients'],
        'Instructions': request.form['Instructions'],
        'Servings': request.form['Servings'],
        'Calories_per_serving': request.form['Calories_per_serving'],
        'Protein_per_serving': request.form['Protein_per_serving'],
        'Carbohydrate_per_serving': request.form['Carbohydrate_per_serving'],
        'Allergens': request.form['Allergens'],
        'Source': request.form['Source'],
        'Author': request.form['Author'],
        'Country_of_origin': request.form['Country_of_origin'],
        'Date_added': request.form['Date_added'],
        'Added_by': request.form['Added_by'],
        'Editing_notes':request.form['Editing_notes'],
        #'upvotes':request.form['upvotes']
    })
    return redirect(url_for('get_recipes'))
    
#update the upvotes on button click using the $inc method    
@app.route('/update_upvote/<recipe_id>', methods=["GET", "POST"]) 
def update_upvote(recipe_id):
    recipes = mongo.db.recipes
    recipes.update_one( {'_id': ObjectId(recipe_id)}, {'$inc' : { 'upvotes' : 1 }}, False,
    { 'upvotes':request.form['upvotes']
    })
    return redirect(url_for('index'))    
    
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('view_recipe.html', recipe=the_recipe, categories=all_categories)
    
# function to display summary vegetarian recipe list
@app.route('/vegetarian', methods=["GET", "POST"])
def vegetarian():
    recipes=mongo.db.recipes.find({"Suitable_for_Vegetarians": "yes"},{ "_id": 1, "Recipe_name": 1, "category_name": 1, "upvotes": 1, "Country_of_origin": 1, "Date_added": 1, "Allergens": 1, "Total_time": 1, "Ingredients": 1 } ).sort('Recipe_name', pymongo.ASCENDING)
    for recipe in recipes:
        count = recipes.count()
        return render_template('vege.html', recipe=recipe, recipes=recipes, count=count)
        
#retrieve attributes from the db to be used in chart construction
@app.route("/recipe_book/recipes")
def recipe_book():
    recipes=mongo.db.recipes.find({}, { "category_name": 1, "Total_time": 1, "Date_added": 1, "Allergens": 1, "Suitable_for_Vegans": 1, "Suitable_for_Vegetarians": 1, "Recipe_name": 1, "Country_of_origin": 1, "_id": 0 })
#output as a string list  for use in dc js charting
    json_recipes = []
    for attribute in recipes:
        json_recipes.append(attribute)
    json_recipes = json.dumps(json_recipes, default=json_util.default)
    return json_recipes
    
@app.route("/draw_chart")
def draw_chart():
    return render_template("chart.html")    
      
        
if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'), port=int(os.environ.get('PORT', 0)), debug=True)