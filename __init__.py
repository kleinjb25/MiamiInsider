import os
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
# All of the database related stuff is stored here, we are importing it all
from database.models import *

app = Flask(__name__)

# Connecting the database to the Flask project
project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(project_dir, 'database/database.db'))

db.init_app(app)

# Run ONLY ONCE the first time, what it does is create the tables
#   inside the database.db file.
'''
with app.app_context():
    db.create_all()
'''

# -----------------
# PAGES BELOW
# -----------------

# Simply prints the list of current locations
@app.route('/')
def index():
    return render_template("index.html", locations=Location.query.all())

# Example of adding a location to the table
@app.route('/post_loc', methods=['POST'])
def post_loc():

    new_loc = Location(
        name=request.form['name'], 
        address=request.form['address'], 
        description=request.form['description'], 
        contact_email=request.form['contact_email'], 
        contact_phone=request.form['contact_phone'], 
        num_reviews=0
    )
    
    db.session.add(new_loc)
    db.session.commit()

    # Redirects to the home page
    return redirect('/')

# Example of deleting a location from the table
@app.route('/del_loc/<int:id>', methods=['DELETE'])
def del_loc(id: int):

    del_loc = Location.query.filter_by(id=id).first()
    db.session.delete(del_loc)
    db.session.commit()

    return redirect('/')


# -----------------
# Runs the page, port specified below
# -----------------
if __name__ == '__main__':
    # Port is set to 6969, change to anything you want
    #   Remember, has to be 1024 or above
    port = int(os.environ.get('PORT', 6969))
    app.run(host='0.0.0.0', port=port)