import os
from flask import Flask, redirect, render_template, request, flash, url_for
from flask_pymongo import PyMongo

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
        
if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'), port=int(os.environ.get('PORT', 0)), debug=True)