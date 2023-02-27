from flask_sqlalchemy import SQLAlchemy#, Model, Column, Integer, String, Float, Date

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String, nullable=False)
    num_reviews = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<User(id='%d', first_name='%s', last_name='%s', email='%s')>" % (
            self.id,
            self.first_name,
            self.last_name,
            self.email
        )

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

    def __repr__(self):
        return "<Location(id='%d', name='%s', avg_rating='%s')>" % (
            self.id,
            self.name,
            self.avg_rating,
        )

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Relational
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)  # Relational
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(1024))

    def __repr__(self):
        return "<Review(id='%d', user_id='%d', location_id='%d')>" % (
            self.id,
            self.user_id,
            self.location_id,
        )

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        return "<Review(id='%d', user_id='%d', location_id='%d')>" % (
            self.id,
            self.user_id,
            self.location_id,
        )

