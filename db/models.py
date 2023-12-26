from . import db
from flask_login import UserMixin

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'id:{self.id}, username:{self.username}, password:{self.password}'

class products(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sku = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(255), nullable = False)
    cost = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f'id:{self.id}, sku:{self.sku}, name:{self.name}, cost:{self.cost}'

class cart_items(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Integer)
    product = db.relationship('products', backref=db.backref('carts', lazy=True))
        
    def __repr__(self):
        return f'id:{self.id}, product_id:{self.product_id}, id:{self.id}, quantity:{self.quantity}'



