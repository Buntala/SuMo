from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, text_pass):
        self.password_hash = bcrypt.generate_password_hash(text_pass).decode('utf-8')

    def check_password_correction(self, submitted_pass):
        return bcrypt.check_password_hash(self.password_hash, submitted_pass)

    def __repr__(self):
        return '<User %r>' % self.id


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    prod_name = db.Column(db.String(100), nullable = False) 
    price = db.Column(db.Integer, nullable=False)
    prod_weight = db.Column(db.Integer,nullable=False)
    stock_num = db.Column(db.Integer, nullable=False)
    stock_unit = db.Column(db.String(30), nullable=False, default=0)
    min_stock = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return  '<Task %r>' % self.id
