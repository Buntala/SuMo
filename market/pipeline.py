import sqlite3
from datetime import datetime

def update_record_data():
    conn = sqlite3.connect('market.db')

    c = conn.cursor()
    c.execute("SELECT prod_name, date, stock_num, stock_unit FROM stock")
    data = c.fetchall()
    date_stamp = datetime.now().date()
    for row in data:
        c.execute("""INSERT INTO record_stock_daily 
                     VALUES {}, {}, {}, {}""".format(row[0],date_stamp ,row[1],row[2]))
    
    conn.commit()

while True:
    #if time == 00 00
    if datetime.now() == datetime(year, month, day):
        update_record_data()