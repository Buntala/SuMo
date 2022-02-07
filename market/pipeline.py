import sqlite3
from datetime import datetime
from statistics import mean
import numpy as np 

#import schedule
def update_record_data():
    conn = sqlite3.connect('market/market.db')

    c = conn.cursor()
    c.execute("SELECT prod_name, stock_num, stock_unit FROM stock")
    data = c.fetchall()
    date_stamp = datetime.now().date() 
    for row in data:
        c.execute("INSERT INTO record_stock_daily (prod_name,date,stock_num,stock_unit) VALUES ('{}', '{}', {}, '{}')".format(row[0],date_stamp ,row[1],row[2]))
    conn.commit()
    conn.close()

def best_fit_slope(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)**2) - mean(xs**2)))
    return m

def min_value_update():
    conn = sqlite3.connect('market/market.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT prod_name FROM record_stock_daily")
    names = c.fetchall()
    for name in names:
        c.execute("SELECT stock_num FROM record_stock_daily WHERE prod_name='{}' ORDER BY date ".format(name[0]))
        temp = c.fetchall()
        if len(temp) > 1:
            for slicer in range(len(temp)-1):
                if temp[-slicer-2]<temp[-slicer-1]:
                    break
            print(temp[:slicer+2])
            x = np.array([x+1 for x in range(len(temp))], dtype=np.float64)
            data = np.array([d[0] for d in temp], dtype=np.float64)
            m = best_fit_slope(x,data)
            min_stock = abs(round(m*7))
            c.execute("UPDATE stock SET min_stock = {} WHERE prod_name='{}' ".format(min_stock,name[0]))
    conn.commit()
    conn.close()

def update_min_stock_data():
    if datetime.date.today().day == 1:
        min_value_update()
    
while True:
    schedule.every().day.at("00:00").do(update_record_data) #Runs daily
    schedule.every().day.at("00:00").do(update_min_stock_data) #Runs monthly