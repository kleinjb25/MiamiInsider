import os
from flask import Flask, render_template, request, redirect, url_for, abort, flash, session
from sqlalchemy.exc import IntegrityError
from wtforms.validators import ValidationError
# All of the database related stuff is stored here, we are importing it all
from database.models import *
from forms import RegistrationForm, LoginForm

# -----------------
# SETTING UP THE FLASK APP
# -----------------
app = Flask(__name__)
app.config['SECRET_KEY'] = '89&Y4pQ^$3nV'

# Connecting the database to the Flask project
project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(project_dir, 'database/database.db'))

db.init_app(app)

''' Code below will delete all current tables. Run this if you made changes to the tables and want to recreate them.
    NOTE: Dropping a table will delete all sample data inside it, be warned.

with app.app_context():
    db.drop_all()
'''

with app.app_context():
    db.create_all()





# -----------------
# PAGES BELOW
# -----------------

# Simply prints the list of current locations for now
@app.route('/')
def index():
    return render_template("sample.html", 
        locations=Location.query.all(),
        categories=Category.query.all())


# LOGIN/REGISTER STUFF BEGIN -------------------------

# TODO: Login form warning that email is invalid before form is submitted

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Initializes the form
    form = LoginForm()

    # Makes sure the form is valid
    if form.validate_on_submit():
        # Gets the correct user
        user = User.query.filter_by(email=form.email.data).first()

        # Successful login
        if user and user.check_password(form.password.data):
            # Sets the session data so that we can check if user is logged in 
            # in other pages
            session['user_id'] = user.id
            session['username'] = user.first_name
            session['logged_in'] = True

            flash(f'Successfully logged in. Welcome back!', 'success')
            return redirect(url_for('index'))
        
        # Unsuccessful login (password didn't match)
        else:
            flash(f'Login unsuccessful. Check your email and password.', 'danger')
    else:
        flash(f'Login unsuccessful. Make sure your email is valid.', 'danger')
    
    return render_template('login.html', form=form)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Initializes the form
    form = RegistrationForm()

    # Makes sure the form is valid
    if form.validate_on_submit():
        # Creates a new user
        new_user = User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            email = form.email.data,
            password = form.password.data,
        )
        db.session.add(new_user)
        try:
            db.session.commit()
        
        # If the email is already taken:
        except IntegrityError:
            db.session.rollback()
            flash(f'Email already taken, please choose a different one.', 'danger')
            return redirect(url_for('register'))
        
        # If the email is not @miamioh.edu domain
        except ValidationError:
            db.session.rollback()
            flash(f'Email has to be from the @miamioh.edu domain.', 'danger')
            return redirect(url_for('register'))
        
        # If everything goes fine and account is created:
        flash(f'Account created. Welcome aboard, {form.first_name.data}!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

# Route to log user out
@app.route('/logout')
def logout():
    # Clears session
    session.pop('user_id', None)
    session.pop('username', None)
    session['logged_in'] = False

    flash(f'You have been successfully logged out.', 'success')
    return redirect(url_for('login'))

# Route to view a user's profile
@app.route('/profile/<int:id>')
def profile(id: int):
    user = User.query.filter_by(id=id).first()
    return render_template('profile.html', user=user)

# Will show a list of a certain user's reviews
@app.route('/reviews/<int:id>')
def review_list(id: int):
    reviews = Review.query.filter_by(user_id=id).first()
    return render_template('reviews.html', reviews=reviews)

# Route to view and update account information
@app.route('/account', methods=['GET', 'POST'])
def account():
    if session['logged_in']:
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('account.html', user=user)
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('login'))

@app.route('/account_update', methods=['POST'])
def account_update():
    user = User.query.filter_by(id=request.form["id"]).first()
    print(user == None)

    # TODO: Make sure user exists
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    # TODO: Implement privacy setting here as well

    db.session.commit()
    flash('Your information was successfully updated.', 'success')
    return redirect(url_for('account'))

# Route to delete your account
@app.route('/account/delete', methods=['POST'])
def account_delete():
    if session['logged_in']:
        user = User.query.filter_by(id=session['user_id'])
        db.session.delete(user)

        # TODO: Error catching here if user not found
        db.session.commit()
        flash('Your account was successfully deleted', 'success')
        return redirect(url_for('login'))
    else:
        flash('You are not logged in', 'danger')
        return redirect(url_for('login'))

# LOGIN/REGISTER STUFF END ---------------------------


# Sample route to print all locations of a certain category.
@app.route('/category/<int:id>', methods=['GET', 'POST'])
def view_category(id: int):
    # Gets input from a form to choose how they will be ordered.
    sort_by = request.form['order']

    # Locations of the same category are found
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

    # Creates the location based on form data
    new_loc = Location(
        name=request.form['name'], 
        address=request.form['address'], 
        description=request.form['description'], 
        contact_email=request.form['contact_email'], 
        contact_phone=request.form['contact_phone'],
        category=request.form['category_id']
    )
    
    db.session.add(new_loc)
    db.session.commit()

    # Redirects to the home page
    return redirect(url_for('index'))

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

    return redirect(url_for('index'))





# -----------------
# Runs the page, port specified below
# -----------------
if __name__ == '__main__':
    # Port is set to 6969, change to anything you want
    #   Remember, has to be 1024 or above
    port = int(os.environ.get('PORT', 6969))
    app.run(host='0.0.0.0', port=port)