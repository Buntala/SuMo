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
from market.model import Stock, User, Sales, record_stock_daily
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
            prod.stock_num -= int(amount)
            db.session.commit()
        session.clear()
        #return redirect(url_for('index'))

    products = Stock.query.filter(Stock.id.in_(session)).all()
    return render_template('scan.html',products=products)

#Admin page only accessible by admin user
@app.route('/admin')#, methods=['GET','POST'])
@login_required
def admin():
    if not current_user.is_admin:
        flash("You don't have the authorization",'error')
        return redirect(url_for('index'))
    else:
        products = Stock.query.all()
        return render_template('admin.html',products=products)

#Test page, only for debugging
@app.route('/test', methods=['GET','POST'])
@login_required
def test():
    return redirect(url_for('index'))


#Saving plot to routes
@app.route('/plot.png/<prod_name>')
@login_required
def plot_png(prod_name):
    if not current_user.is_admin:
        flash("You don't have the authorization",'error')
        return redirect(url_for('index'))
    else:
        fig = create_figure(prod_name)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

#Creating plot from data
def create_figure(prod_name):
    xs,ys= get_data(prod_name)
    title_graph = prod_name.capitalize() + " Stock Graph"
    if xs and ys: 
        fig = Figure(figsize=[10,6])
        axis = fig.add_subplot(1, 1, 1)
        fig.patch.set_alpha(0)
        axis.patch.set_alpha(0)
        #change spine color  
        axis.spines['bottom'].set_color('white')
        axis.spines['top'].set_color('white') 
        axis.spines['right'].set_color('white')
        axis.spines['left'].set_color('white')
        #set tick rotation and color
        #saxis.set_xticklabels(xs,rotation=30)
        axis.tick_params(axis='x', colors='white')
        axis.tick_params(axis='y', colors='white')
        #set title andlabel color
        axis.title.set_color('white')
        fig.patch.set_alpha(0)
        axis.patch.set_alpha(0)
        axis.yaxis.label.set_color('white')
        #graph plotting
        axis.plot(xs, ys, color='#A507FF')
        axis.set_title(title_graph, fontsize=20)
        axis.set_ylabel('Total Stock', fontsize=16)
        axis.tick_params(axis='x', labelrotation=30)
        return fig

def get_data(prod_name):
    xs,ys=[],[]
    query_data = record_stock_daily.query.filter(record_stock_daily.prod_name == prod_name).order_by(record_stock_daily.date).all()
    for row in query_data:
        xs.append(str(row.date)[:10])
        ys.append(row.stock_num)
    return(xs,ys)


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
            flash("You are logged in!",'success')
            if current_user.is_admin:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            flash("Username and password no match found!",'error')
            return redirect(url_for('login'))
            #raise ValidationError('Username and password does not match')
    #if form.errors != {}:
    #    for msg in forms.errors.values():
    #        print(f'Login Error: {msg}')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out", 'info')
    return redirect(url_for("login"))