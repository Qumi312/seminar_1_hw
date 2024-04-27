from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    inventory = db.relationship('Inventory', backref='products')


class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True, index = True)
    name = db.Column(db.String(50), nullable=False)
    inventory = db.relationship('Inventory', backref='locations')


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True, index = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False,autoincrement=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False, autoincrement=False)
    quantity = db.Column(db.Integer, nullable=False)
