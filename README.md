# MiamiInsider

## Description
This project is a web application developed using the Flask framework. It is a review site for locations in Oxford, Ohio, made for members of the Miami University community. In this site, users can browse the website for locations in Oxford. They can view information about locations such as contact information and description. They can also create an account if they are a member of the Miami University community and leave reviews on locations to better guide others.


## Project dependencies
The project uses Python version 3.11.2 and several pip dependencies. It is recommended to use a virtual environment with this project.


### Pip dependencies
Run the following command in the home page of the project to install the necessary dependencies

```pip3 install -r requirements.txt```


## Data Modelling

The data model of the project is provided in `models.py` file in the */database* directory. It contains the following tables: User, Location, LocationImage, Review and Category. 
- The User table contains all of the information about the users
- The Location table contains all of the information about the locations
- The LocationImage table contains the images for the locations. The location images are stored in a separate table for simplicity because SQL stores images as binary
- The Review table stores informatio about the reviews
- The Category table stores all of the different categories that locations are sorted by. 


## Database setup
The */database* directory contains the database.db file, which is the sqlite3 database that the project utilizes. The subdirectory */sample_data* contains a .sql file that can be run to upload sample data to the database.

```sqlite3 database.db < sample_data/add_values.sql```

### SQLite installation
Since the database file is SQLite3, you need to have it installed if you want to run SQL commands directly in the database. If you want to install SQLite on Windows 10/11, [this](https://www.youtube.com/watch?v=XA3w8tQnYCA) video is really helpful.

## Permissions
This app has a very rudimentary permissions system. A user can have two permission - regular user or admin. In the User table, there is a column called *permission*. By default, when a new user is created this value is 0. An admin user will have a permission value of 99. A user with admin permissions will be able to add locations, delete any user review and location, and update location information and images.

## Running the server
To run the server, navigate to the home directory of the project and simply run:

```python __init__.py```
