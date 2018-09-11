#-*- coding: utf-8 -*-
import os
from flask import Flask, redirect, render_template, request, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import pymongo
import json
from bson import json_util
from flask_paginate import Pagination, get_page_parameter
from flask_paginate import Pagination, get_page_args
from mongo_datatables import DataTables

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
    recipes=mongo.db.recipes.find().sort('Recipe_name', pymongo.ASCENDING ))
    
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
        'upvotes':request.form['upvotes']
    })
    return redirect(url_for('get_recipes'))
    
#update the upvotes on button click using the $inc method    
@app.route('/update_upvote/<recipe_id>', methods=["GET", "POST"]) 
def update_upvote(recipe_id):
    recipes = mongo.db.recipes
    mongo.db.recipes.update_many(
    {"upvotes": "0"},
    {"$set": {"upvotes": 0},
    "$currentDate": {"lastModified": True}})
    recipes.update_one( {'_id': ObjectId(recipe_id)}, {'$inc' : { 'upvotes' : 1 }}, False,
    { 'upvotes':request.form['upvotes']
    })
    if request.method == "POST":
        flash("You have successfully upvoted a recipe! Thank you", "alert alert-success")
    return redirect(url_for('index'))    
    
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('view_recipe.html', recipe=the_recipe, categories=all_categories)
    
"""GET RECIPES BY GROUP"""

#function to view summary of all recipes
# use flask paginate in conjunction with mongodb cursor.skip(offset) method for pagination
@app.route('/allrecipes', methods=["GET", "POST"])
def allrecipes():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args()
    recipes=mongo.db.recipes.find().sort('Recipe_name', pymongo.ASCENDING)
    recipes_to_render = recipes.limit(per_page).skip(offset)
    pagination = Pagination(page=page, total=recipes.count(), per_page=per_page, offset=offset) 
    return render_template('allRecipes.html', recipes=recipes_to_render, search=search, pagination=pagination)   
    
# function to display summary vegetarian recipe list
@app.route('/vegetarian', methods=["GET", "POST"])
def vegetarian():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args()
    recipes=mongo.db.recipes.find({"Suitable_for_Vegetarians": "Yes"},{ "_id": 1, "Recipe_name": 1, "category_name": 1, "upvotes": 1, "Country_of_origin": 1, "Date_added": 1, "Allergens": 1, "Total_time": 1, "Ingredients": 1 } ).sort('Recipe_name', pymongo.ASCENDING)
    recipes_to_render = recipes.limit(per_page).skip(offset)
    pagination = Pagination(page=page, total=recipes.count(), per_page=per_page, offset=offset)
    return render_template('vege.html', recipes=recipes_to_render, search=search, pagination=pagination)
        
# function to display summary vegan recipe list
@app.route('/vegan', methods=["GET", "POST"])
def vegan():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args()
    recipes=mongo.db.recipes.find({"Suitable_for_Vegans": "Yes" } ).sort('Recipe_name', pymongo.ASCENDING)
    recipes_to_render = recipes.limit(per_page).skip(offset)
    pagination = Pagination(page=page, total=recipes.count(), per_page=per_page, offset=offset)
    return render_template('vegan.html', recipes=recipes_to_render, search=search, pagination=pagination)
        
# function to display summary other recipe list
@app.route('/other', methods=["GET", "POST"])
def other():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args()
    recipes=mongo.db.recipes.find({"Suitable_for_Vegetarians": "No" }).sort('Recipe_name', pymongo.ASCENDING)
    recipes_to_render = recipes.limit(per_page).skip(offset)
    pagination = Pagination(page=page, total=recipes.count(), per_page=per_page, offset=offset)
    return render_template('other.html', recipes=recipes_to_render, search=search, pagination=pagination)
    
# function to display summary starters recipe list
@app.route('/starters', methods=["GET", "POST"])
def starters():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args()
    recipes=mongo.db.recipes.find({"category_name": "Starter" }).sort('Recipe_name', pymongo.ASCENDING)
    recipes_to_render = recipes.limit(per_page).skip(offset)
    pagination = Pagination(page=page, total=recipes.count(), per_page=per_page, offset=offset)
    return render_template('starters.html', recipes=recipes_to_render, search=search, pagination=pagination)

# function to display summary Main Dish recipe list
@app.route('/mainDishes', methods=["GET", "POST"])
def mainDishes():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args()
    recipes=mongo.db.recipes.find({"category_name": "Main Course" }).sort('Recipe_name', pymongo.ASCENDING)
    recipes_to_render = recipes.limit(per_page).skip(offset)
    pagination = Pagination(page=page, total=recipes.count(), per_page=per_page, offset=offset)
    return render_template('mainDishes.html', recipes=recipes_to_render, search=search, pagination=pagination)

# function to display summary desserts recipe list
@app.route('/desserts', methods=["GET", "POST"])
def desserts():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args()
    recipes=mongo.db.recipes.find({"category_name": "Dessert" }).sort('Recipe_name', pymongo.ASCENDING)
    recipes_to_render = recipes.limit(per_page).skip(offset)
    pagination = Pagination(page=page, total=recipes.count(), per_page=per_page, offset=offset)
    return render_template('desserts.html', recipes=recipes_to_render, search=search, pagination=pagination)     

# function to display summary side dish recipe list
@app.route('/sideDishes', methods=["GET", "POST"])
def sideDishes():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args()
    recipes=mongo.db.recipes.find({"category_name": "Side Course" }).sort('Recipe_name', pymongo.ASCENDING)
    recipes_to_render = recipes.limit(per_page).skip(offset)
    pagination = Pagination(page=page, total=recipes.count(), per_page=per_page, offset=offset)
    return render_template('sideDishes.html', recipes=recipes_to_render, search=search, pagination=pagination) 
# function to display summary breads and cakes recipe list   
@app.route('/breadsCakes', methods=["GET", "POST"])
def breadsCakes():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args()
    recipes=mongo.db.recipes.find({"category_name": "Breads and Cakes" }).sort('Recipe_name', pymongo.ASCENDING)
    recipes_to_render = recipes.limit(per_page).skip(offset)
    pagination = Pagination(page=page, total=recipes.count(), per_page=per_page, offset=offset)
    return render_template('breadsCakes.html', recipes=recipes_to_render, search=search, pagination=pagination) 
    
""" FILTER BY CRITERIA """

# get the top 5 by upvote
@app.route('/topfive', methods=["GET", "POST"])
def topfive():
    recipes=mongo.db.recipes.find({"upvotes": { '$gt': 0 } } ).sort('upvotes', pymongo.DESCENDING).limit(5)
    return render_template('topfive.html', recipes=recipes)
    
# get allergen free recipes    
@app.route('/noAllergens', methods=["GET", "POST"])
def noAllergens():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args()
    recipes=mongo.db.recipes.find({"Allergens": "None Known" } ).sort('Recipe_name', pymongo.ASCENDING)
    recipes_to_render = recipes.limit(per_page).skip(offset)
    pagination = Pagination(page=page, total=recipes.count(), per_page=per_page, offset=offset)
    return render_template('noAllergens.html',  recipes=recipes_to_render, search=search, pagination=pagination)

# search for quick recipes
@app.route('/quickRec', methods=["GET", "POST"])
def quickRec():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args()
    recipes=mongo.db.recipes.find({"Total_time": { '$lte': 30 } } ).sort('Total_time', pymongo.ASCENDING)
    recipes_to_render = recipes.limit(per_page).skip(offset)
    pagination = Pagination(page=page, total=recipes.count(), per_page=per_page, offset=offset)
    return render_template('quickRec.html', recipes=recipes_to_render, search=search, pagination=pagination)     

# search for recent recipes
@app.route('/recentlyAdded', methods=["GET", "POST"])
def recentlyAdded():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args()
    recipes=mongo.db.recipes.find({"Date_added": {"$gte": 'Tuesday, 21, August, 2018'}}).sort('Date_added', pymongo.DESCENDING)
    recipes_to_render = recipes.limit(per_page).skip(offset)
    pagination = Pagination(page=page, total=recipes.count(), per_page=per_page, offset=offset)
    return render_template('recentlyAdded.html', recipes=recipes_to_render, search=search, pagination=pagination)

    
# retrieve attributes from the db to be used in chart construction
@app.route("/recipe_book/recipes")
def recipe_book():
    recipes=mongo.db.recipes.find({}, { "category_name": 1, "Total_time": 1, "Date_added": 1, "Allergens": 1, "Suitable_for_Vegans": 1, "Suitable_for_Vegetarians": 1, "Recipe_name": 1, "Country_of_origin": 1, "_id": 0 })
# return as a string list 
    json_recipes = []
    for attribute in recipes:
        json_recipes.append(attribute)
    json_recipes = json.dumps(json_recipes, default=json_util.default)
    return json_recipes

# show the chart   
@app.route("/draw_chart")
def draw_chart():
    return render_template("chart.html")    

# show the table
@app.route('/table-view')
def table_view():
    return render_template("table_view.html",
    recipes=mongo.db.recipes.find())     
        
if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'), port=int(os.environ.get('PORT', 0)), debug=True)