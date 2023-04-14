# MiamiInsider

## Description
This project is a web application developed using the Flask framework. It is a review site for locations in Oxford, Ohio, made for members of the Miami University community. In this site, users can browse the website for locations in Oxford. They can view information about locations such as contact information and description. They can also create an account if they are a member of the Miami University community and leave reviews on locations to better guide others.

If you want the detailed installation instructions for the project, click [here](https://github.com/kleinjb25/MiamiInsider#detailed-installation-and-setup-instructions).


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

## Detailed installation and setup instructions
You can get the details of this project's dependencies below. This section details how to set up and run the project from this GitHub repository. 

### Step 1
Navigate to [this link](https://www.python.org/downloads/release/python-3112/) to download Python v3.11.2, using the appropriate installer for your operating system. Once you have downloaded and installed Python, you can clone this GitHub repository onto your local machine.

### Step 2
In a terminal, navigate to the home directory of this repository where you have cloned it onto your computer. Making sure that you are using Python version 3.11.2, run the following command:

```pip install -r requirements.txt```

This command will download all of the necessary Python dependencies the project needs to run.

### Step 3
Once the requirements have all been downloaded, run the command ```python __init__.py```. Make sure you are still in the home directory of the project. If this doesn't work, try ```python3 __init__.py```. This command should start running the web application in your terminal.

### Step 4
In the terminal, you should see the following output:
~~~
$ python __init__.py 
 * Serving Flask app '__init__'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:6969
 * Running on http://172.25.253.29:6969
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 678-438-076
~~~
Click on one of the addresses provided.