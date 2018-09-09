This data-driven web application  allows a user to access a recipe database to Create, Read, Update and 
Delete recipes accordingly. The backend functionality is handled with a flask pymongo framework and the 
front end is handled by the materialize and bootstrap frameworks.  As the logic is driven by python, 
jinja is incorporated as the templating language for python.  A dashboard is also created to present 
summary statistics around various groups and criteria within the database. DC js charting using bootstrap 
and the associated crossfilter javascript files, is used to provide interactive charts. A simple mongo 
datatable (again using bootstrap) is also provided, allowing a summary view of the data. It provides 
simple sort (ascending/descending) and search functionality and allows access to view the full recipe 
page through a link.