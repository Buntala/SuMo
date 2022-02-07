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
    stock_num = db.Column(db.Integer, nullable=False, default=0)
    stock_unit = db.Column(db.String(30), nullable=False)
    min_stock = db.Column(db.Integer, nullable=False)
    qr_code = db.Column(db.String(32), nullable=False)
    def __repr__(self):
        return  '<stock %r>' % self.id

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    prod_name = db.Column(db.String(100), nullable = False) 
    date = db.Column(db.DateTime, nullable = False)
    price = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return  '<Task %r>' % self.id

class record_stock_daily(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    prod_name = db.Column(db.String(100), nullable = False) 
    date = db.Column(db.Date, nullable = False)
    stock_num = db.Column(db.Integer, nullable=False)
    stock_unit = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return  '<Recorded_Stock %r>' % self.id

class jumlahBDT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String(30), nullable = False) 
    unit = db.Column(db.Integer, nullable=False)

    def repr(self):
        return  '<Hasil Timbangan %r>' % self.id 