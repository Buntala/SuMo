import sqlite3
from datetime import datetime
import schedule
def update_record_data():
    conn = sqlite3.connect('market/market.db')

    c = conn.cursor()
    c.execute("SELECT prod_name, stock_num, stock_unit FROM stock")
    data = c.fetchall()
    date_stamp = datetime.now().date() 
    for row in data:
        c.execute("INSERT INTO record_stock_daily (prod_name,date,stock_num,stock_unit) VALUES ('{}', '{}', {}, '{}')".format(row[0],date_stamp ,row[1],row[2]))
    conn.commit()
    
while True:
    schedule.every().day.at("00:00").do(update_record_data)