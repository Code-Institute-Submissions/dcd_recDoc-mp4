# Project Name #
dcd_recipes
## Overview ##
This data-driven web application  allows a user to access a recipe database to Create, Read, Update and 
Delete recipes accordingly. In addition upvote and pagination functionality is also provided. A user can 
search for recipes based on a particular group, for example, vegetarian, or by a filter, for example the 
top 5 based on upvotes. Summary data is returned with an option to view full recipes.  
The backend functionality is handled with a flask pymongo framework and the front end is handled by the 
materialize and bootstrap frameworks.  As the logic is driven by python, jinja is incorporated as the 
templating language for python.  A dashboard is also created to present summary statistics around various 
groups and criteria within the database. DC js charting using bootstrap and the associated crossfilter 
javascript files, is used to provide interactive charts. A simple mongo datatable (again using bootstrap) is 
provided, allowing a summary view of the data. It provides simple sort (ascending/descending) and search 
functionality and allows access to view the full recipe page through a link.
## UX ##
### Problem Definition ###
In order to fulfill brief requirements the issues to be sorted were defined as:
* Provide CRUD Functionality 
* Build an adequate database with sufficient fields to facilitate grouping and filtering of recipes 
* Provide the backend code and front-end forms to allow users to interact with the site 
* Create visualisation to the user of summary data derived from the various criteria 
* Provide the user with upvote and optional pagination functionality 
* Optionally provide basic user registration

User profiles would typically be cooking enthusiasts (amateur and professional) who are interested in local
and international cuisine. A user could also be a busy individual who may want to find quick recipes. Other 
users may have special dietry needs as a result of allergens and be keen to locate allergen free recipes. 
Other users include vegans and vegetarians.  

### User Stories ###
User stories include:
* As a cooking enthusiast who lives in (Country), I want to share and view recipes from my Country/other Countries
* As a cooking enthusiast  who lives in (Country), I want the ability to edit/develop recipes from my Country/other countries
* As a disciplined foodie  who lives in(Country), I want to access recipe groups such as vegan recipes from my Country/other countries.
* As a busy mom I want the ability to source quick recipes from my country/othercountries
* As an allergen sufferer I want the ability to find allergen free recipes from around the world
* As an intrepid traveller visiting (country) I want to learn about indigeneous cuisines

### Wireframing ###
Pencil was used to draw up wireframes of how the different pages of the application might appear, to satisfy 
the requirements of the brief. They can be viewed in the milestone4Pencil.pdf file in the additional_info 
folder in the static dir.

### Design ###
#### Database management system: ####
Mongodb was chosen as the database management system for this application. It was felt that a recipe based 
application would not necessarily handle a lot of complicated querying, but would be prone to an unstructured
format as different users inteact with the application. Mongodb uses the json structure format (bson) which 
is useful for storing large amounts of unstructured data. JSON  format lets you nest records one within the 
other and also allows for different records to have different fields which is inevitable with different 
users manipulating data in a web application.   
The Database was created first and the application then built around it.  A basic DB was set up using the 
mLab Mongo cloud based application. 2 collections were established, one for the courses(categories) and one 
for the actual recipes. The category key value pair is added to the recipes collection linking the recipes 
collection to the  category collection akin to a foreign key. The categories is also used to group similar 
or related recipes for example main dishes, desserts, etc. Several records were added to start off the 
database.  
#### Front end ####
It was decided to use simple colors that would be consistent across all elements and pages. Icons would also
be incorporated into the forms to supplement field titles and placeholder text. Headings would be bold and
simple, but direct to mitigate any ambiguity.  
Template inheritance is used to cut down on duplication of code. A base html page is used as a parent 
containing library files, nav links and scripts used across child elements. Child elements then inherit 
from the base, while also rendering the block specific to itself. There are however three other stand alone 
pages that are not linked to the parent; a sign in page, a dashboard page and datatable page.  
The nav bar is provided across all pages (except the sigin page) and provides users with the necessary links 
to navigate the application and to perform any CRUD operations. It provides links to the home page where you 
can search recipes by groups or criteria, the add recipe page, edit recipe page (where edits and deletions 
are carried out), the categories page where additions, deletions and edits can be done on categories. There 
are also links to the dashboard and a datatable.
DC.js charting was the preferred method to presenting summary data over the mongo db.aggregation pipeline 
method used in conjunction with matplotlib.  While not responsive on smaller screen sizes dc.js is an 
effective way to display interactive information visually on larger screen sizes. The level of interactivity
on a dc crossfilter chart is always a strong consideration despite the loss of responsiveness on smaller
screens. The data can be viewed on smaller screen sizes by scrolling.  
Semantic elements are used within the html documents (section, img, form, input, textarea, etc).  
The coding pages also contain comments providing information on the various sections and functions.
The materialize classes center-align, responsive-img, input-field, collapsible and btn btn_small 
(in conjunction with jQuery where necessary) are used extensively to add styling and provide functionality.   
The material-icons class is used to provide visual intuitiveness in the forms.
Where bootstrap is used classes such as text-center, text-primary, table-responsive, table-striped are used 
to add styling and provide functionality. A separate style sheet provides styling for custom elements and 
to override bootstrap styles where the materialize theme is continued throughout all pages in relation to 
the nav-bar and buttons.

## Features ##
The features are described below.
### Existing Features ###
*Feature 1* Initial sign-in page to ensure only those interested enter the site. Initial access to the web 
application is via a sign in page which directs you to the home page on successful sign in. There is some 
front end validation in that some special characters are not allowed. This is the only way to access the 
application. Materialize is added to the page to give a color theme to the submit button but this is not 
a child template as nav bar elements giving acess to all elements are not desired.  
*Feature 2* Slideshow with recipe images on the home page. Some jQuery is used to drive the slideshow.  
*Feature 3* Select option drop down links on the home page to search recipes by group or filtered criteria. 
These links redirect to the respective urls, rendering summary pages which in turn link to a full view of 
the recipe or back to the home page. A simple jQuery function triggers each link. Recipes are listed alphabetically
except in cases were they are returned by filtered criteria such as top 5 by upvote or by recently added. 
Summary recipes returned by a group search, also contain a link to the dashboard at the top of each page.  
*Feature 4* Add a recipe form with submit and cancel buttons. The add recipe link presents a materialize 
styled html form with the various input fields.  All fields are required and contain other front end 
validation measures specific to the field. This is necessary as accurate calculations and graphs depend on 
consistency per field.  A datepicker is used to select dates which, ensures all dates  entered by users are 
uniform. Other fields only allow specific characters and some format as capitalized. For example Ireland 
and ireland will produce separate sets of data for a given circumstance. Thus it is necessary to ensure 
that only Ireland is returned, rather than both formats. Placeholders contain text giving direction/instructions 
on input. A submit button at the end of this form calls a function to add the data to the database in 
dictionary format, before redirecting back to the edit recipes page.  
*Feature 5* Edit recipe form with delete and edit buttons. This page lists all recipes alphabetically by name 
and category. Clicking on the edit button presents an edit form exactly as the add form, except that existing 
values are rendered and can be overwritten with an edit. A submit button at the end of this form calls a 
function to update the document fields to the database, before redirecting back to the edit recipes page. 
There is also an option (button) to cancel the edit if so desired. The delete button will raise an alert 
asking if recipe should be deleted. Click ok or cancel as appropriate.  
*Feature 6* The view categories page presents a list of categories with buttons to edit, add or delete a 
category. (This functionality is a clone of the CRUD functionality provided for the recipes).  
*Feature 7* Full view recipe format. The full view page allows a user to view the complete recipe with all 
fields. The page presents the field name with dropdown, which can then be clicked to reveal the info. There 
is a button for upvoting and a button to return to the home page. Upvoting can only occur in full page view.  
*Feature 8* Upvote functionality. The upvote field is presented as a read only field and set to 0 for the first 
edition of a recipe. This field is incorporated into the form, as the other fields and gets incremented on 
upvote using the $inc operator. There is no user interaction while adding or editing the upvote field.  Once 
upvoted the user is redirected back to the home page rather than back to the full recipe page. This is done 
to prevent continual revoting as functionality to only allow one vote per user is not yet present. On successful 
upvote a flash message confirms that the upvote has been successful providing user-feedback, for a positive 
user experience.  
*Feature 9* Flask pagination (as per the flask documentation) is used for all search return views that will 
render more than 10 documents in the browser window. In general documents are sorted ascending by recipe 
name for convenience except where specifically filtered under a criterion (example number of upvotes or quick 
recipes, etc). Having an ordered sort mode in conjunction with pagination enables a user to quickly cycle 
through the pages to get to the desired location.   
*Feature 10* The interactive dashboard presents several number boxes and charts giving a visual representation 
of the recipes based on various criteria. Number boxes list the total recipes currently in the application 
along with the numbers of vegan and vegetarian recipes. One pie chart reveals the total number of recipes per
category (course). Another shows the total number of allergens by type and includes the number of recipes with
no known allergens. A bar chart shows the number of recipes by country of origin. One stacked bar chart shows 
the number of recipes by type (vegan, etc) and course. Another shows the number of recipes by type (vegan, etc)
and allergens.  
*Feature 11* A mongo datatable styled by bootstrap, (with some elements overwritten to the materialize 
formats) presents a summary list of the recipes by criteria such as category, date added, country etc. It 
allows quick search and view of the summary data and each row also has a link button to view the full recipe. 
Note: that the standard bootstrap datatable theme is used and these libraries do not support responsive 
design. However the datatable can be viewed on smaller screens by scrolling.  
### Features left to implement ###
At this point in time, user details are not stored or incorporated into the database to track upvoting or 
associate a particular user  with a particular recipe. This is something to consider with future development 
of the application where greater security and validation would be necessary to ensure that users do not 
delete recipes uploaded by others.  
Form validation on the server side is not covered but is something  to be covered in future development of 
this application as a standard and robust belt and braces exercise.  
There is also potential to add other charts depending on user preferences.
## Technologies used ##
[Materialize](https://materializecss.com/):     
All html templates dealing with the recipes and categories are rendered in the materialize standard version 
front-end  development framework. It is simple to use, is supported across devices, is responsive and 
presents functionality intuitively for a positive user experience. The accordion collapsible component is 
used for displaying document data, disabled where not required. Data is bound to this in the template by 
dynamically creating a list item for each document returned. However any pages using flask pagination may 
not be fully responsive and some scrolling may be necessary. The pagination info bar has been aligned to 
the left of its div to enhance full responsiveness, but full responsiveness on all small screen devices 
is not guranteed.  
[Bootstrap](https://startbootstrap.com/):   
A bootstrap roundabout theme is used to style the dashboard and datatable page with styles overwtitten by 
the materialize formats to give consistency throughout all pages.  
[Bootstrap datatable](https://datatables.net/examples/styling/bootstrap.html):  
Provides styles , pagination and search function to the data table.  
[jQuery](https://jquery.com/):  
A separate script file has been written for the chart elements but the other script (30 odd lines in total) 
has been kept within the html documents. The base html contains a script section with jQuery scripts to 
initialise the various elements of materialize, to enforce text formats within the html forms and to trigger 
the drop down search links in the home page. The index page contains some jQuery script to drive the 
slideshow. The edit page contains some jQuery (due to a bug) to bind the date associated with the task to 
the field. Thus script is required in the parent and child. The view_table template contains a few lines of 
jQuery for the datatable (bootstrap library).

## Testing ##
Testing was mainly done by writing code and producing output and analysing issues found. The approach.pdf 
located in the additional_info folder, outlines the methodology used to derive routes and views and issues 
encountered. Some testing of mongodb methods was done in the cloud9 ide to see what output was produced. They
are outlined in the methodsTest.py.pdf file in the additional_info folder. The developer tool was used to 
pinpoint styles in bootstrap to be changed to the materialize format.  
A lot of work was focused on ensuring that data in the forms is validated in such a way as to be consistent 
across all users. For example dates will alway be the same format, integers will always be integers, country 
of origin will always begin with a capital, suitable for vegans will always be either "Yes" or "No" and so on.
Consistent input of data is essential, particularly when data is being computed for output in the dashboard.  
The app was run on chrome, firefox and microsoft edge and performed similarly across all 3 apps.  
The additional-info folder contains some additional files detailing background information relating to the 
project. Links also shown in acknowledgements below.  
*approach.pdf* Outlines the approach used with the python end and issues encountered.    
*methodsTest.pdf* This file outlines some tests run in the ide to view output from the methods illustrated
within the mongodb and pymongo documentation.    
*additional-infoMP4.pdf* Lists other code sources consulted in completing this application. Also lists information 
sources and any references to licenses.  
## Deployment ##
The repository for this site is located at https://github.com/vmcggh18/dcd_recDoc-mp4  
The repo can be downloaded as a zip file for installation into a local ide. When installed locally, check 
for any dependencies that need to be installed to run it, by checking the requirements.txt file. Then just 
select the app.py file and click run to view in the browser.      
Alternatively the working application can be viewed at https://dcd-online-rec.herokuapp.com/  
## Credits ##
### Content ###
Recipes used in this application are sourced from:  
Source: National Heart, Lung, and Blood Institute; National Institutes of Health; U.S.
Department of Health and Human Services https://www.nhlbi.nih.gov/health-topics/publications-and-resources    
http://www.eat-vegan.rocks    
https://damndelicious.net/2014/10/13/easy-homemade-ramen/  
### Media ###
The images used in this application are sourced from:  
https://www.pexels.com/photo/food-on-white-background-256318/  
https://burst.shopify.com/photos/breakfast-from-above  
### Acknowledgments ###
The sources below provided inspiration for this application:
#### Code Institute ####
Code Institute Module 8 Data Driven Development Module 
#### Other Documentation Consulted ####
[Mongodb documentation:](https://docs.mongodb.com/)    
Overview of mongodb methods  
[pymongo docs:](https://api.mongodb.com/python/current/)  
Overview of pymongo methods  
[flask:](http://flask.pocoo.org/)    
Overview of flask  
[flask pagination:](http://flask.pocoo.org/snippets/44/)    
Syntax for using flask pagination  
[Restrict special characters with jQuery](https://stackoverflow.com/questions/21331576/restrict-special-characters-using-jquery)  
Using jQuery to restrict characters allowed  
[Auto-capitalize-first-letter-of-every-word-in-input-fields](https://stackoverflow.com/questions/48126101/javascript-to-auto-capitalize-first-letter-of-every-word-in-input-fields)    
Using javascript to capitalise the first letter of each word in a form. Used in this application to customise
text across all users.  
[Interactive Data Visualisation with mongodb and d3-dc charting](http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/)  
Tutorial example on integrating d3-dc charting with mongodb  
[Rotate x-axis chart text](https://github.com/dc-js/dc.js/issues/731 (rotate x-axis text)    
Rotating x-axis text on a dc chart to fit within its allocated width.  
[Slideshow](https://www.w3schools.com/howto/howto_js_slideshow.asp)  
Tutorial on how to incorporate a slideshow into a html document  

