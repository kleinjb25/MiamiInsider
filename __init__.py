# For specifying the app's port
import os
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
# All of the database related stuff is stored here, we are importing it all
from database.models import *

app = Flask(__name__)

# Conneceting the database to the Flask project
db_filename = 'database.db'
project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(project_dir, db_filename))

db.init_app(app)

# -----------------
# PAGES BELOW
# -----------------
@app.route('/')
def index():
    return "hello, world"


# -----------------
# Runs the page, port specified below
# -----------------
if __name__ == '__main__':
    # Port is set to 6969, change to anything you want
    #   Remember, has to be 1024 or above
    port = int(os.environ.get('PORT', 6969))
    app.run(host='0.0.0.0', port=port)