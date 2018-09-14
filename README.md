This data-driven web application  allows a user to access a recipe database to Create, Read, Update and 
Delete recipes accordingly. The backend functionality is handled with a flask pymongo framework and the 
front end is handled by the materialize and bootstrap frameworks.  As the logic is driven by python, 
jinja is incorporated as the templating language for python.  A dashboard is also created to present 
summary statistics around various groups and criteria within the database. DC js charting using bootstrap 
and the associated crossfilter javascript files, is used to provide interactive charts. A simple mongo 
datatable (again using bootstrap) is also provided, allowing a summary view of the data. It provides 
simple sort (ascending/descending) and search functionality and allows access to view the full recipe 
page through a link.
Template inheritance is used to cut down on duplication of code. A base html page is used as a parent 
containing library files, nav links and scripts used across child elements. Child elements then inherit 
from the base, while also rendering the block specific to itself. There however three other stand alone 
pages that are not linked to the parent; a sign in page, a dashboard page and datatable page. 
Initial access to the web application is via a sign in page which directs you to the home page on successful 
sign in. There is some front end validation in that some special characters are not allowed. This is the only 
way to access the application. At this point in time, user details are not stored or incorporated into the 
database to track upvoting or associate a particular user  with a particular recipe. This is something to 
consider with future development of the application where greater security and validation would be necessary 
to ensure that users do not delete recipes uploaded by others. Materialize is added to the page to give a 
color theme to the submt button but this is not a child template as nav bar elements giving acess to all 
elements are not desired.
The nav bar provides users with the necessary links to navigate the application and to perform any CRUD 
operations. It provides links to the home page  where you can search recipes by groups or criteria, the 
add recipe page, edit recipe page (where edits and deletions are carried out), the categories page where 
additions, deletions and edits can be done on categories. There are also links to the dashboard and a 
datatable. 
The home page hosts a slide show of images along with select option drop down links to search recipes by 
group or filtered criteria. These links redirect to the respective urls, rendering summary pages which in 
turn link to a full view of the recipe or back to the home page. A simple jQuery function triggers each link. 
The full recipe view contains an upvote button allowing a user to upvote the recipe.  Once upvoted the user 
is redirected back to the home page rather than back to the full recipe page. This is done to prevent 
continual revoting as functionality to only allow one vote per user is not yet present. However a flash 
message confirms that the upvote has been successful providing feedback, for a positive user experience.
The add recipe link presents a materialize styled html form with the various input fields.  All fields are 
required and contain other front end validation measures specific to the field. This is necessary as 
accurate calculations and graphs depend on consistency per field.  A datepicker is used to select dates 
which, ensures all dates  entered by users are uniform. Other fields only allow specific characters and 
some format as capitalized. For example Ireland and ireland will produce separate sets of data for a given 
circumstance. Thus it is necessary to ensure that only Ireland is returned, rather than both formats. 
Placeholders contain text giving direction/instructuions on input.The upvote field is presented as a read 
only field and set to 0 for the first edition of a recipe. This field is incorporated into the form, as the 
other fields and gets incremented on upvote using the $inc operator. There is no user interaction while 
adding or editing the upvote field.  A submit button at the end of this form calls a function to add the 
data to the database in dictionary format, before redirecting back to the edit recipes. page. There is also 
an option (button) to cancel the addition if so desired. Note: that form validation on the server side is 
not covered but is something  to be covered in future development of this application as a robust belt and 
braces exercise. 
The edit recipe link presents  a list of the recipes with button functions to either edit a recipe or delete 
a recipe. Clicking on the edit button presents an edit form exactly as the add form, except that existing 
values are rendered and can be overwritten with an edit. A submit button at the end of this form calls a 
function to update the document fields to the database, before redirecting back to the edit recipes page. 
There is also an option (button) to cancel the edit if so desired. The delete button will raise an alert 
asking if recipe should be deleted. Click ok or cancel as appropriate.
The view categories page presents a list of categories with buttons to edit, add or delete a category.
(This functionality is a clone of the CRUD functionality provided for the recipes).
All html templates dealing with the recipes and categories are rendered in the materialize standard version 
front-end  development framework. It is simple to use, is supported across devices, is responsive and 
presents functionality intuitively for a positive user experience. The accordion collapsible component is 
used for displaying document data, disabled where not required. Data is bound to this in the template by 
dynamically creating a list item for each document returned. However any pages using flask pagination may 
not be fully responsive and some scrolling may be necessary. The pagination info bar has been aligned to 
the left of its div to enhance full responsiveness, but full responsiveness on all small screen devices 
is not guranteed.
The dashboard presents several number boxes and charts giving a visual representation of the recipes based 
on various criteria. DC.js charting was the preferred method to presenting summary data over the mongo 
db.aggregation pipeline method used in conjunction with matplotlib.  While not responsive on smaller 
screen sizes dc.js is an effective way to display interactive information visually on larger screen sizes. 
The data can be viewed on smaller screen sizes by scrolling. A bootstrap roundabout theme is used to style 
the page with styles overwtitten by materialize formats to give consistency throughout all pages.
The mongo datatable styled by bootstrap,  (with some elements overwritten to the materialize formats) 
presents a summary list of the recipes by criteria such as category, date added, country etc. It allows 
quick search and view of the summary data and each row also has a link button to view the full recipe. 
Note: that the standard bootstrap datatable theme is used and these libraries do not support responsive 
design.However the datatable can be viewed on smaller screens by scrolling.
Flask pagination (as per the flask documentation) is used for all search return views that will render more 
than 10 documents in the browser window. In general documents are sorted ascending by recipe name for 
convenience except where specifically filtered under a criterion (example number of upvotes or quick 
recipes, etc).
A separate script file has been written for the chart elements but the other script (30 odd lines in total) 
has been kept within the html documents. The base html contains a script section with jQuery scripts to 
initialise the various elements of materialize, to enforce text formats within the html forms and to trigger 
the drop down search links in the home page. The index page contains some jQuery script to drive the 
slideshow. The edit page contains some jQuery (due to a bug) to bind the date associated with the task to 
the field. Thus script is required in the parent and child. The view_table template contains a few lines of 
jQuery for the datatable (bootstrap library).
The additional-info folder contains some additional files deatailing background information relating to the 
project.
Sources:
Code Institute Module 8 Data Driven Development Module
https://stackoverflow.com/questions/21331576/restrict-special-characters-using-jquery
https://stackoverflow.com/questions/48126101/javascript-to-auto-capitalize-first-letter-of-every-word-in-input-fields
http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/
https://github.com/dc-js/dc.js/issues/731 (rotate x-axis text)
https://www.w3schools.com/howto/howto_js_slideshow.asp
Images:
https://www.pexels.com/photo/food-on-white-background-256318/
https://burst.shopify.com/photos/breakfast-from-above
Recipes:
https://www.nhlbi.nih.gov/health-topics/publications-and-resources
http://www.eat-vegan.rocks
https://damndelicious.net/2014/10/13/easy-homemade-ramen/