import os
from flask import Flask, render_template, request, redirect, url_for, abort
# All of the database related stuff is stored here, we are importing it all
from database.models import *
#from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '89&Y4pQ^$3nV'

# Connecting the database to the Flask project
project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(project_dir, 'database/database.db'))

db.init_app(app)

# Usually you only run the code below ONCE to add the tables to the db.
# I have already done this and the database.db file is updated and contains the necessary stuff.
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
    return render_template("sample.html", 
        locations=Location.query.all(),
        categories=Category.query.all())

# LOGIN STUFF
'''
@app.route('/')
def login():
    return render_template('login.html', title='Register', form=LoginForm())

@app.route('/register')
def signup():
    return render_template('register.html', title='Login', form=RegistrationForm())
'''

@app.route('/category/<int:id>', methods=['GET', 'POST'])
def view_category(id: int):
    sort_by = request.form['order']
    locs = Location.query.filter_by(category_id=id)
    if sort_by == "name":
        locs.order_by(Location.name)
    elif sort_by == "reviews":
        locs.order_by(Location.avg_rating)
    else:
        abort(404)

    return render_template("category.html", locations=locs)

# Example of adding a location to the table
@app.route('/post_loc', methods=['POST'])
def post_loc():

    new_loc = Location(
        name=request.form['name'], 
        address=request.form['address'], 
        description=request.form['description'], 
        contact_email=request.form['contact_email'], 
        contact_phone=request.form['contact_phone'], 
        num_reviews=0,
        category=request.form['category_id']
    )
    
    db.session.add(new_loc)
    db.session.commit()

    # Redirects to the home page
    return redirect('/')

'''  SAMPLE LOCATION
"name": "Fiesta Charra",
"address": "25 W High St, Oxford, OH 45056",
"description": "Roomy, booth-lined Mexican restaurant with a low-key vibe, a full bar & lunch specials.",
"contact_email": "N/A",
"contact_phone": "(513) 524-3114"
'''

# Example of deleting a location from the table
@app.route('/del_loc/<int:id>', methods=['POST', 'DELETE'])
def del_loc(id: int):
    # NOTE: Currently POST is included as a method for this funciton because
    # HTML forms do not recognize DELETE

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