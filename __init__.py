import os
import Levenshtein
from flask import Flask, render_template, request, redirect, url_for, abort, flash, session, make_response
from sqlalchemy.exc import IntegrityError
from wtforms.validators import ValidationError
from database.models import *
from forms import *

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

# Only displays locations with rating above 4
CUTOFF_RATING = 4

@app.route('/')
def index():
    return render_template("index.html", 
        locations=Location.query.filter(Location.avg_rating >= CUTOFF_RATING).all(),
        location_images=LocationImage.query.all(),
        categories=Category.query.all(),

        search_form=SearchForm()
    )

@app.route('/location_image/<int:id>')
def location_image(id: int):
    image = LocationImage.query.filter_by(location_id=id).first()
    response = make_response(image.data)
    response.headers.set('Content-Type', 'image/jpeg')
    return response


# LOGIN/REGISTER STUFF BEGIN -------------------------

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
            session['user_permission'] = user.permission
            session['logged_in'] = True

            flash(f'Successfully logged in. Welcome back!', 'success')
            return redirect(url_for('index'))
        
        # Unsuccessful login (password didn't match)
        else:
            flash(f'Login unsuccessful. Check your email and password.', 'danger')
    
    return render_template(
        'login.html', form=form, 
        
        search_form=SearchForm()
    )

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
        
        session['user_id'] = new_user.id
        session['user_permission'] = new_user.permission
        session['logged_in'] = True

        # If everything goes fine and account is created:
        flash(f'Account created. Welcome aboard, {form.first_name.data}!', 'success')
        flash(f'Navigate to your account and set up your profile!', 'info')

        return redirect(url_for('index'))

    return render_template(
        'register.html', form=form, 
        
        search_form=SearchForm()
    )

# Route to log user out
@app.route('/logout')
def logout():
    clear_login_session()

    flash(f'You have been successfully logged out.', 'success')
    return redirect(url_for('login'))

# Route to view a user's profile
@app.route('/profile/<int:id>')
def profile(id: int):
    user = User.query.filter_by(id=id).first()
    reviews = Review.query.filter_by(user_id=id).all()
    return render_template('profile.html', user=user, reviews=reviews, search_form=SearchForm())

# Route to view and update account information
@app.route('/account', methods=['GET', 'POST'])
def account():
    if session['logged_in']:
        user = User.query.filter_by(id=session['user_id']).first()
        if user == None:
            clear_login_session()
            flash('There was an error validating your login.', 'danger')
            return redirect(url_for('login'))
        else:
            form = UpdateForm()

            if form.validate_on_submit():
                user = User.query.filter_by(id=session['user_id']).first()
                if user != None:
                    user.first_name =form.first_name.data
                    user.last_name = form.last_name.data
                    user.phone = form.phone.data
                    user.private = form.private.data
                    db.session.commit()
                    flash('Your information was successfully updated.', 'success')
                else:
                    flash('We were unable to validate your user.', 'danger')
            else:
                for error in form.errors:
                    flash(f'Error with {error} field', 'danger')

            return render_template('account.html', user=user, form=UpdateForm())
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('login'))

# Route to delete your account
@app.route('/account/delete', methods=['POST'])
def account_delete():
    if session['logged_in']:
        user = User.query.filter_by(id=session['user_id']).one_or_none()
        if user == None:
            flash('Your user id was not successfully validated.', 'danger')
            return redirect(url_for('account'))
        else:
            user_reviews = Review.query.filter_by(user_id=session['user_id']).all()
            db.session.delete(user_reviews)
            db.session.delete(user)
            db.session.commit()
            clear_login_session()
            return redirect(url_for('register'))
        
    else:
        flash('You are not logged in', 'danger')
        return redirect(url_for('login'))

def clear_login_session():
    session.pop('user_id', None)
    session.pop('user_permission', None)
    session['logged_in'] = False

# LOGIN/REGISTER STUFF END ---------------------------


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query = str(form.query.data).lower()
        sort = str(form.sort.data)

        # sort options: Name, Description, Rating

        query_words = query.split()
        loc_list = []
        similarity_min = 0.65

        for loc in Location.query.all():
            loc_name = loc.name.lower()
            loc_desc = loc.description.lower()

            for word in query_words:
                for loc_word in loc_name.split() + loc_desc.split():
                    similarity = 1 - Levenshtein.distance(word.lower(), loc_word.lower()) / max(len(word), len(loc_word))
                    if similarity > similarity_min and word not in stop_words:
                        if loc not in loc_list:
                            loc_list.append(loc)
                            break  # move to the next loc in the outer loop
                else:
                    continue  # executed if the inner loop did not break
                break  # move to the next loc in the outer loop

        if sort == 'Name':
            loc_list.sort(key=lambda x: x.name)
        elif sort == 'Description':
            loc_list.sort(key=lambda x: x.description)
        elif sort == 'Rating':
            loc_list.sort(key=lambda x: x.avg_rating, reverse=True)

        return render_template('search.html', locations=loc_list, query=query, search_form=SearchForm())
    else:
        flash('Error with form validation - check your search query.', 'danger')  
        return redirect(url_for('index'))

        

@app.route('/location/<int:id>')
def location(id: int):
    loc = Location.query.filter_by(id=id).first()
    ctg = Category.query.filter_by(id=loc.category).first()
    reviews = Review.query.filter_by(location_id=id).all()

    if loc != None and ctg != None:
        return render_template(
            'location.html', 
            location=loc, 
            category=ctg, 
            reviews=reviews, 
            form=ReviewForm(), 

            search_form=SearchForm()
        )
    else:
        abort(404)

@app.route('/location/<int:id>/favorite')
def favorite():
    # TODO: If user id and location id not in table, add to table.
    #   Otherwise, remove from table
    pass

# REVIEW STUFF ------------------------------

@app.route('/post_review/<int:loc_id>', methods=['POST'])
def post_review(loc_id: int):
    form = ReviewForm()

    if session['logged_in']:
        if form.validate_on_submit():
            user = User.query.filter_by(id=session['user_id']).first()
            loc = Location.query.filter_by(id=loc_id).first()
            username = user.first_name + " " + user.last_name

            new_review = Review(
                    user_id = user.id,
                    user_name = username,
                    location_id = loc.id,
                    location_name = loc.name,
                    rating = form.rating.data,
                    text = form.text.data
                )

            db.session.add(new_review)
            if loc.avg_rating == None:
                loc.avg_rating = new_review.rating
            else:
                loc.avg_rating = round(((float(loc.avg_rating) * float(loc.num_reviews)) + float(new_review.rating)) / float(loc.num_reviews+1), 1)
            loc.num_reviews+=1
            db.session.commit()
            flash('Review posted successfully!', 'success')
        else:
            db.session.rollback()
            print(form.errors)
            flash('Error posting review.', 'danger')
            
    else:
        flash('You have to be logged in to post a review.', 'danger')
    return redirect(url_for('location', id=loc_id))

@app.route('/del_review/<int:id>', methods=['POST'])
def del_review(id: int):
    review = Review.query.filter_by(id=id).first()
    loc_id = review.location_id
    if review != None:
        if session['user_id'] == review.user_id or session['user_permission'] == 99:
            loc = Location.query.filter_by(id=review.location_id).first()
            loc.avg_rating = round(((float(loc.avg_rating) * float(loc.num_reviews)) - float(review.rating)) / float(loc.num_reviews-1), 1)
            loc.num_reviews-=1
            db.session.delete(review)
            db.session.commit()
            flash('Your review has been successfully deleted!', 'success')
        else:
            flash("You cannot delete someone else's review.", 'danger')
    else:
        abort(404)
    return redirect(url_for('location', id=loc_id))

# REVIEW STUFF END ---------------------------


# ADMIN STUFF ---------------------------

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session['user_permission'] == 99:
        from werkzeug.exceptions import BadRequest
        
        try:
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

            img = request.files['image']

            loc_image = LocationImage(
                location_id=new_loc.id,
                name=new_loc.name,
                data=img.read()
            )
            db.session.add(loc_image)
            db.session.commit()
        except BadRequest:
            print('form submisison failed')
        
        return render_template('admin.html', 
            categories=Category.query.all(), 
            locations=Location.query.all(),
            users=User.query.all())
    else:
        flash("You do not have the necessary permissions", 'danger')
        return redirect(url_for('index'))

@app.route('/update_permission', methods=['POST'])
def update_permission():
    if request:
        for user_id, value in request.form.items():
            user_id = user_id.split('-')[0]
            user = User.query.filter_by(id=user_id).one_or_none()
            if user != None:
                if value == "True":
                    print('admin')
                    user.permission = 99
                elif value == "False":
                    print('not admin')
                    user.permission = 0
                    if user_id == session['user_id']:
                        session['user_permission'] = 0
                db.session.commit()
            else:
                print(f"Unable to find user with id {user_id}")
        
        flash("Permissions updated successfully!", 'success')
        return redirect(url_for('admin'))
    else:
        print(request)
        flash("Form had issues submitting", 'danger')

# Adding location image
@app.route('/post_loc_img', methods=['POST'])
def post_loc_img():
    img = request.files['image']

    old_img = LocationImage.query.filter_by(location_id=request.form['location_id']).first()
    if old_img != None:
        db.session.delete(old_img)
        db.session.commit()

    new_img = LocationImage(
        location_id=request.form['location_id'],
        name=request.form['location_name'],
        data=img.read()
    )
    db.session.add(new_img)
    db.session.commit()

    flash("Location image posted!", 'success')
    return redirect(url_for('admin'))

@app.route('/post_category', methods=['POST'])
def post_category():
    new_ctg = Category(
        name=request.form['name'],
        fa_tag=request.form['fa-tag']
    )

    db.session.add(new_ctg)
    db.session.commit()

    flash("Category added!", 'success')
    return redirect(url_for('admin'))

@app.route('/del_category/<int:id>', methods=['POST'])
def del_category(id: int):
    ctg = Category.query.filter_by(id=id).one_or_none()
    if ctg != None:
        locs = Location.query.filter_by(category=id).all()
        for loc in locs: loc.category = None

        db.session.delete(ctg)
        db.session.commit()
        flash("Category deleted!", 'success')
    else:
        flash("Category ID not found", 'danger')

    return redirect(url_for('admin'))

# Deleting location from database
@app.route('/del_loc/<int:id>', methods=['POST'])
def del_loc(id: int):

    del_loc = Location.query.filter_by(id=id).first()
    loc_image = LocationImage.query.filter_by(location_id=id).first()
    loc_reviews = Review.query.filter_by(location_id=id).all()
    for review in loc_reviews: db.session.delete(review)

    db.session.delete(del_loc)
    db.session.delete(loc_image)
    db.session.commit()

    flash("Location deleted!", 'success')
    return redirect(url_for('admin'))

# ADMIN STUFF END ---------------------------



# -----------------
# Runs the page, port specified below
# -----------------
if __name__ == '__main__':
    # Port is set to 8080, change to anything you want
    #   Remember, has to be 1024 or above
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
