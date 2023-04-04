from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Admin permissions is 99
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    phone = db.Column(db.String(14))
    private = db.Column(db.Boolean, nullable=False)

    permission = db.Column(db.Integer, nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.phone = None
        self.private = True
        self.permission = 0

    def __repr__(self):
        return "<User(id='%d', first_name='%s', last_name='%s', email='%s')>" % (
            self.id,
            self.first_name,
            self.last_name,
            self.email
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String, nullable=False)
    contact_email = db.Column(db.String(60))
    contact_phone = db.Column(db.String(60))
    num_reviews = db.Column(db.Integer, nullable=False)
    avg_rating = db.Column(db.Float)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)  # Relational

    def __init__(self, name, address, description, contact_email, contact_phone, category):
        self.name = name
        self.address = address
        self.description = description
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.num_reviews = 0
        self.category = category

    def __repr__(self):
        return "<Location(id='%d', name='%s', avg_rating='%s')>" % (
            self.id,
            self.name,
            self.avg_rating,
        )

class LocationImage(db.Model):
    __tablename__ = "location_images"

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), unique=True, nullable=False)
    name = db.Column(db.String)
    data = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return "<Location(id='%d', loc_id='%d', avg_rating='%d')>" % (
            self.id,
            self.location_id,
            self.name,
        )

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Relational
    user_name = db.Column(db.String(128), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)  # Relational
    location_name = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(256))

    def __repr__(self):
        return "<Review(id='%d', user_id='%d', location_id='%d')>" % (
            self.id,
            self.user_id,
            self.location_id,
        )

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    fa_tag = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return "<Review(id='%d', user_id='%d', location_id='%d')>" % (
            self.id,
            self.user_id,
            self.location_id,
        )

