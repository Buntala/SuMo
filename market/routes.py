import io
import cv2 #QR code detection
import numpy as np #storing matrices
import pandas as pd #Accessing csv files
import matplotlib.pyplot as plt #Plot graphs
from matplotlib.figure import Figure 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pyzbar.pyzbar import decode
from market import app, db
from flask import render_template ,request, url_for, redirect, flash, get_flashed_messages, Response #Web Framework
from market.model import Stock, User, Sales
from market.forms import LoginForm
from wtforms import ValidationError
from flask_login import login_user,logout_user,login_required,current_user 
from market import session
from datetime import datetime

#Homepage after Login
@app.route('/index', methods=['GET','POST'])
@login_required
def index():
    if request.method=="POST":
        time_sales = datetime.now().replace(microsecond=0)
        for i in session:
            col_id = "amount_"+str(i) 
            amount = request.form[col_id]
            prod = Stock.query.filter(Stock.id==str(i)).first()
            total = int(amount)*int(prod.price)
            hist = Sales(prod_name = prod.prod_name, date = time_sales, price = prod.price, amount=amount, total_price = total)
            db.session.add(hist)
            #prod.stock_num -= int(amount)
            db.session.commit()
            print(prod.stock_num)
        session.clear()
        #return redirect(url_for('index'))

    products = Stock.query.filter(Stock.id.in_(session)).all()
    return render_template('scan.html',products=products)

#Admin page only accessible by admin user
@app.route('/admin')#, methods=['GET','POST'])
@login_required
def admin():
    if not current_user.is_admin:
        flash("You don't have the authorization")
        return redirect(url_for('index'))
    else:
        products = Stock.query.all()
        return render_template('admin.html',products=products)

#Test page, only for debugging
@app.route('/test', methods=['GET','POST'])
@login_required
def test():
    return redirect(url_for('index'))

#Test page, only for debugging
@app.route('/plot')
@login_required
def plot():
    if not current_user.is_admin:
        flash("You don't have the authorization")
        return redirect(url_for('index'))
    else:
        df = pd.read_csv("market/static/test.csv")
        if request.method=="POST": 
            pass
        prod = df['product_name'].unique()
        return render_template('plot.html',products=prod)

def pict(df):
    pic= df[df['product_name'] == request.form['plot-btn']]
    #plt.figure(figsize=[12,6])
    plt.plot(pic['date'],pic['stock'])
    nameProd = pic['product_name'].iloc[0]
    plt.title(nameProd)
    plt.xlabel('Date')
    plt.ylabel('Total num of Stock')
    plt.savefig('market/static/images/new_plot.png')

#Saving plot to routes
@app.route('/plot.png/<prod_name>')
def plot_png(prod_name):

    fig = create_figure(prod_name)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

#Creating plot from data
def create_figure(prod_name):
    df = pd.read_csv("market/static/test.csv")
    pic= df[df['product_name'] == prod_name]
    fig = Figure(figsize=[12,6])
    nameProd = pic['product_name'].iloc[0]
    axis = fig.add_subplot(1, 1, 1)
    xs = pic['date']
    ys = pic['stock']
    axis.plot(xs, ys)
    axis.set_title(nameProd)
    axis.set_xlabel('Date')
    axis.set_ylabel('Total num of Stock')
    return fig

#Openning camera and scan QR code
@app.route('/scan')
@login_required
def scan():
    #qr_scan()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 640)
    while True:
        success, img = cap.read()
        if decode(img):
            myData = decode(img)[-1].data.decode('utf-8')
            cap.release()
            cv2.destroyAllWindows()
            break
        cv2.waitKey(1)
    product = Stock.query.filter(Stock.prod_name == myData).first().id
    session.append(product)
    return redirect(url_for('index'))

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_exist = User.query.filter(User.username == form.username.data).first()
        if user_exist and user_exist.check_password_correction(submitted_pass=form.password.data):
            login_user(user_exist)
            #flash("You are logged in!")
            if current_user.is_admin:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            print("no")
            return redirect(url_for('login'))
            #raise ValidationError('Username and password does not match')
    #if form.errors != {}:
    #    for msg in forms.errors.values():
    #        print(f'Login Error: {msg}')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out", category='info')
    return redirect(url_for("login"))