import os
from flask import Flask, redirect, render_template, request, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

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
    return render_template("index.html")
    
#function to locate the categories and display
@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.categories.find()) 
    
#function to display the editing form
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('edit_category.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))

#function to carry out edit on the database (write to the database)
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form['category_name']})
    return redirect(url_for('get_categories'))
    
#function to delete a category  
@app.route('/delete_category/<category_id>')  
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for("get_categories"))
    
#function to display the form view to insert new data into
@app.route('/new_category')
def new_category():
    return render_template('add_category.html')

#function to insert a new category into the DB  
@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form['category_name']}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))
    
#function to locate the recipes and display
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find())
    
#function to display blank form bound to the categories
@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html',
    categories=mongo.db.categories.find())
    
#function to write the data to the DB
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes =  mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))
    #return redirect(url_for('index'))
    
        
if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'), port=int(os.environ.get('PORT', 0)), debug=True)