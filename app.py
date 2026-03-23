from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import sqlite3
import hashlib

def database_setup():
    user_setup()
    bidders_setup()
    sellers_setup()
    local_vendors_setup()
    helpdesk_setup()

def user_setup():
    columns = ['email', 'password']
    data = pd.read_csv('data/Users.csv',
                       names=columns, header=0)
    col1 = data['email'].values
    col2 = data['password'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    # create tables
    # Users
    cursor.execute('CREATE TABLE IF NOT EXISTS Users (email VARCHAR(50), password VARCHAR(40), PRIMARY KEY(email))')

    for i in range(len(col1)):
        email = col1[i]
        password = col2[i]
        # hash password to MD5 (32-bit Hex)
        password = hashlib.sha256(password.encode()).hexdigest()
        sql = "INSERT OR IGNORE INTO Users(email,password) VALUES (?,?)"
        val = (email, password)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

def bidders_setup():
    columns = ['email', 'first_name', 'last_name', 'age', 'home_address_id', 'major']
    data = pd.read_csv('data/Bidders.csv',
                       names=columns, header=0)
    col1 = data['email'].values
    col2 = data['first_name'].values
    col3 = data['last_name'].values
    col4 = data['age'].values
    col5 = data['home_address_id'].values
    col6 = data['major'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    # create tables
    # Bidders
    cursor.execute("CREATE TABLE IF NOT EXISTS Bidders(email VARCHAR(50), first_name VARCHAR(25), last_name VARCHAR(25), age INT, home_address_id VARCHAR(40), major VARCHAR(40), PRIMARY KEY(email), FOREIGN KEY (email) REFERENCES Users(email))")

    for i in range(len(col1)):
        email = col1[i]
        first_name = col2[i]
        last_name = col3[i]
        age = int(str(col4[i]))
        home_address_id = col5[i]
        major = col6[i]
        sql = "INSERT OR IGNORE INTO Bidders(email, first_name, last_name, age, home_address_id, major) VALUES (?,?,?,?,?,?)"
        val = (email, first_name, last_name, age, home_address_id, major)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

def sellers_setup():
    columns = ['email', 'bank_routing_number', 'bank_account_number', 'balance']
    data = pd.read_csv('data/Sellers.csv',
                       names=columns, header=0)
    col1 = data['email'].values
    col2 = data['bank_routing_number'].values
    col3 = data['bank_account_number'].values
    col4 = data['balance'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    # create tables
    # Sellers
    cursor.execute('CREATE TABLE IF NOT EXISTS Sellers (email VARCHAR(50), bank_routing_number VARCHAR(20), bank_account_number VARCHAR(10), balance REAL, PRIMARY KEY (email), FOREIGN KEY (email) REFERENCES Users(email))')

    for i in range(len(col1)):
        email = col1[i]
        bank_routing_number = col2[i]
        bank_account_number = int(str(col3[i]))
        balance = float(str(col4[i]))
        sql = "INSERT OR IGNORE INTO Sellers(email, bank_routing_number, bank_account_number, balance) VALUES (?,?,?,?)"
        val = (email, bank_routing_number, bank_account_number, balance)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

def local_vendors_setup():
    columns = ['email', 'business_name', 'business_address_id', 'customer_service_phone_number']
    data = pd.read_csv('data/Local_Vendors.csv',
                       names=columns, header=0)
    col1 = data['email'].values
    col2 = data['business_name'].values
    col3 = data['business_address_id'].values
    col4 = data['customer_service_phone_number'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    # create tables
    # Local_Vendors
    cursor.execute('CREATE TABLE IF NOT EXISTS Local_Vendors (email VARCHAR(50), business_name VARCHAR(50), business_address_id VARCHAR(40), customer_service_phone_number VARCHAR(20), PRIMARY KEY(email), FOREIGN KEY (email) REFERENCES Sellers(email) ON DELETE CASCADE)')

    for i in range(len(col1)):
        email = col1[i]
        business_name = col2[i]
        business_address_id = col3[i]
        customer_service_phone_number = col4[i]
        sql = "INSERT OR IGNORE INTO Local_Vendors(email, business_name, business_address_id, customer_service_phone_number) VALUES (?,?,?,?)"
        val = (email, business_name, business_address_id, customer_service_phone_number)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

def helpdesk_setup():
    columns = ['email', 'position']
    data = pd.read_csv('data/Helpdesk.csv',
                       names=columns,header=0)
    col1 = data['email'].values
    col2 = data['position'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    # create tables
    # Helpdesk
    cursor.execute('CREATE TABLE IF NOT EXISTS Helpdesk(email VARCHAR(50), position VARCHAR(40), PRIMARY KEY(email), FOREIGN KEY (email) REFERENCES USERS(email))')

    for i in range(len(col1)):
        email = col1[i]
        position = col2[i]
        sql = "INSERT OR IGNORE INTO Helpdesk(email,position) VALUES (?,?)"
        val = (email, position)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

database_setup()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login.html', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email'] #gets inputted email
        password = request.form['password'] #gets inputted password
        role = request.form['role'] #gets the role button clicked
        hash_pswrd = hashlib.sha256(password.encode()).hexdigest() #hash password in sha256
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE email= ? AND password=?", (email,hash_pswrd)) #sees if user exists in Users table
        user=cursor.fetchone()

        if user:#if the user exists, check they are in that role
            if role == "bidder": #BIDDER ROLE CHECK
                cursor.execute("SELECT * FROM Bidders WHERE email=?", (email,))
                if cursor.fetchone():
                    conn.close()
                    return redirect(url_for('bidder'))
                else: error = "Invalid username or password for bidder"
            elif role == "seller": #SELLER ROLE CHECK
                cursor.execute("SELECT * FROM Sellers WHERE email=?", (email,))
                if cursor.fetchone():
                    conn.close()
                    return redirect(url_for('seller'))
                else: error = "Invalid username or password for seller"
            elif role == "helpdesk": #HELPDESK ROLE CHECK
                cursor.execute("SELECT * FROM Helpdesk WHERE email=?", (email,))
                if cursor.fetchone():
                    conn.close()
                    return redirect(url_for('helpdesk'))
                else: error = "Invalid username or password for helpdesk"
            else:
                conn.close()
                error = "user does not have that role"
        else:#login attempt failed. No user matches found
            error = "Invalid username or password"
    return render_template('login.html', error=error)

'''def add_name(email, password):
    # hash the password using sha256
    password = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE email= ? AND password= ?", (email, password))
    result = cursor.fetchall()
    if result:
        return 1
    else:
        return 0'''

@app.route('/bidder.html')
def bidder():
    return render_template('bidder.html')

@app.route('/seller.html')
def seller():
    return render_template('seller.html')

@app.route('/helpdesk.html')
def helpdesk():
    return render_template('helpdesk.html')

if __name__ == '__main__':
    app.run()
