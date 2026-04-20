from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import pandas as pd
import sqlite3
import hashlib # To hash passwords
import re # to check to see if text input matches a particular format

def database_setup():
    ''' This function calls other functions
        to setup the NittanyAuction database
        one csv file at a time. This involves reading the csv files,
        calling a CREATE TABLE SQL statement to create the table,
        then using a for loop to call an INSERT SQL statement to
        insert each row into the table
    '''
    user_setup()
    bidders_setup()
    sellers_setup()
    local_vendors_setup()
    helpdesk_setup()
    auction_listings_setup()
    bids_setup()
    address_setup()
    category_setup()
    credit_card_setup()
    rating_setup()
    request_setup()
    transaction_setup()
    zipcode_setup()

def user_setup():
    ''' This function sets up the Users
        table based on the csv file
        called Users.csv
    '''
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
    ''' This function sets up the Bidders
        table based on the csv file
        called Bidders.csv
    '''
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
    cursor.execute("CREATE TABLE IF NOT EXISTS Bidders(email VARCHAR(50), first_name VARCHAR(25), last_name VARCHAR(25), age INT, home_address_id VARCHAR(40), major VARCHAR(40), PRIMARY KEY(email), FOREIGN KEY (email) REFERENCES Users(email), FOREIGN KEY (home_address_id) REFERENCES Address(address_ID))")

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
    ''' This function sets up the Sellers
        table based on the csv file
        Sellers.csv
    '''
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
    ''' This table sets up the local
        vendors table using the csv file
        Local_Vendors.csv
    '''
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
    cursor.execute('CREATE TABLE IF NOT EXISTS Local_Vendors (email VARCHAR(50), business_name VARCHAR(50), business_address_id VARCHAR(40), customer_service_phone_number VARCHAR(20), PRIMARY KEY(email), FOREIGN KEY (email) REFERENCES Sellers(email) ON DELETE CASCADE, FOREIGN KEY (business_address_id) REFERENCES Address(address_ID))')

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
    '''This function sets up the helpdesk
       table based on the csv file
       Helpdesk.csv
    '''
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

def auction_listings_setup():
    '''This table sets up the auction
       listings table using the csv file
       Auction_Listings.csv
    '''
    columns = ['seller_email', 'listing_ID', 'category', 'auction_title', 'product_name', 'product_description', 'quantity', 'reserve_price', 'max_bids', 'status']
    data = pd.read_csv('data/Auction_Listings.csv', names=columns, header=0)
    col1 = data['seller_email'].values
    col2 = data['listing_ID'].values
    col3 = data['category'].values
    col4 = data['auction_title'].values
    col5 = data['product_name'].values
    col6 = data['product_description'].values
    col7 = data['quantity'].values
    col8 = data['reserve_price'].values
    col9 = data['max_bids'].values
    col10 = data['status'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Auction_Listings(seller_email VARCHAR(50), listing_ID INTEGER UNIQUE, category VARCHAR(200), auction_title VARCHAR(200), product_name VARCHAR(200), product_description VARCHAR(1000), quantity INTEGER, reserve_price VARCHAR(50), max_bids INTEGER, status INTEGER, PRIMARY KEY(seller_email, listing_ID), FOREIGN KEY (seller_email) REFERENCES Sellers(email), FOREIGN KEY (category) REFERENCES Categories(category_name))')

    for i in range(len(col1)):
        seller_email = col1[i]
        listing_ID = int(str(col2[i]))
        category = col3[i]
        auction_title = col4[i]
        product_name = col5[i]
        product_description = col6[i]
        quantity = int(str(col7[i]))
        reserve_price = col8[i]
        max_bids = int(str(col9[i]))
        status = int(str(col10[i]))
        sql = "INSERT OR IGNORE INTO Auction_Listings(seller_email, listing_ID, category, auction_title, product_name, product_description, quantity, reserve_price, max_bids, status) VALUES (?,?,?,?,?,?,?,?,?,?)"
        val = (seller_email, listing_ID, category, auction_title, product_name, product_description, quantity, reserve_price, max_bids, status)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

def bids_setup():
    '''This function sets up the bids
       table using the csv file
       Bids.csv
    '''
    columns = ['bid_ID', 'seller_email', 'listing_ID', 'bidder_email', 'bid_price']
    data = pd.read_csv('data/Bids.csv', names=columns, header=0)
    col1 = data['bid_ID'].values
    col2 = data['seller_email'].values
    col3 = data['listing_ID'].values
    col4 = data['bidder_email'].values
    col5 = data['bid_price'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Bids(bid_ID INTEGER, seller_email VARCHAR(50), listing_ID INTEGER, bidder_email VARCHAR(50), bid_price REAL, PRIMARY KEY(bid_ID), FOREIGN KEY (seller_email) REFERENCES Sellers(email), FOREIGN KEY (listing_ID) REFERENCES Auction_Listings(listing_ID), FOREIGN KEY (bidder_email) REFERENCES Bidders(email))')

    for i in range(len(col1)):
        bid_ID = int(str(col1[i]))
        seller_email = col2[i]
        listing_ID = int(str(col3[i]))
        bidder_email = col4[i]
        bid_price = float(str(col5[i]))
        sql = "INSERT OR IGNORE INTO Bids(bid_ID, seller_email, listing_ID, bidder_email, bid_price) VALUES (?,?,?,?,?)"
        val = (bid_ID, seller_email, listing_ID, bidder_email, bid_price)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

def address_setup():
    '''This function sets up the address
       table using the csv file Address.csv
    '''
    columns = ['address_ID', 'zipcode', 'street_number', 'street_name']
    data = pd.read_csv('data/Address.csv', names=columns, header=0)
    col1 = data['address_ID'].values
    col2 = data['zipcode'].values
    col3 = data['street_number'].values
    col4 = data['street_name'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Address(address_ID VARCHAR(40), zipcode INTEGER, street_number INTEGER, street_name VARCHAR(100), PRIMARY KEY (address_ID), FOREIGN KEY (zipcode) REFERENCES Zipcodes(zipcode))')

    for i in range(len(col1)):
        address_ID = str(col1[i])
        zipcode = int(str(col2[i]))
        street_number = int(str(col3[i]))
        street_name = col4[i]
        sql = "INSERT OR IGNORE INTO Address(address_ID, zipcode, street_number, street_name) VALUES (?,?,?,?)"
        val = (address_ID, zipcode, street_number, street_name)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

def category_setup():
    '''This function sets up the categories
       table using the csv file
       Categories.csv
    '''
    columns = ['parent_category', 'category_name']
    data = pd.read_csv('data/Categories.csv', names=columns, header=0)
    col1 = data['parent_category'].values
    col2 = data['category_name'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Categories(parent_category VARCHAR(100), category_name VARCHAR(100), PRIMARY KEY (category_name))')

    for i in range(len(col1)):
        parent_category = str(col1[i])
        category_name = str(col2[i])
        sql = "INSERT OR IGNORE INTO Categories(parent_category, category_name) VALUES (?,?)"
        val = (parent_category, category_name)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

def credit_card_setup():
    '''This function sets up the credit
       card table using the csv file
       Credit_Cards.csv
    '''
    columns = ['credit_card_num', 'card_type', 'expire_month', 'expire_year', 'security_code', 'owner_email']
    data = pd.read_csv('data/Credit_Cards.csv', names=columns, header=0)
    col1 = data['credit_card_num'].values
    col2 = data['card_type'].values
    col3 = data['expire_month'].values
    col4 = data['expire_year'].values
    col5 = data['security_code'].values
    col6 = data['owner_email'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Credit_Cards(credit_card_num VARCHAR(20), card_type VARCHAR(50), expire_month INTEGER, expire_year INTEGER, security_code INTEGER, owner_email VARCHAR(50), PRIMARY KEY (credit_card_num), FOREIGN KEY (owner_email) REFERENCES Bidders(email))')

    for i in range(len(col1)):
        credit_card_num = col1[i]
        card_type = col2[i]
        expire_month = int(str(col3[i]))
        expire_year = int(str(col4[i]))
        security_code = int(str(col5[i]))
        owner_email = col6[i]
        sql = "INSERT OR IGNORE INTO Credit_CARDS(credit_card_num, card_type, expire_month, expire_year, security_code, owner_email) VALUES (?,?,?,?,?,?)"
        val = (credit_card_num, card_type, expire_month, expire_year, security_code, owner_email)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

def rating_setup():
    '''This function sets up the ratings
       table using the csv file
       Ratings.csv
    '''
    columns = ['bidder_email', 'seller_email', 'date', 'rating', 'rating_description']
    data = pd.read_csv('data/Ratings.csv', names=columns, header=0)
    col1 = data['bidder_email'].values
    col2 = data['seller_email'].values
    col3 = data['date'].values
    col4 = data['rating'].values
    col5 = data['rating_description'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Ratings(bidder_email VARCHAR(50), seller_email VARCHAR(50), rating_date VARCHAR(50), rating INTEGER, rating_description VARCHAR(500), PRIMARY KEY (bidder_email, seller_email, rating_date), FOREIGN KEY (bidder_email) REFERENCES Bidders(email), FOREIGN KEY (seller_email) REFERENCES Sellers(email))')

    for i in range(len(col1)):
        bidder_email = col1[i]
        seller_email = col2[i]
        rating_date = col3[i]
        rating = int(str(col4[i]))
        rating_description = col5[i]
        sql = "INSERT OR IGNORE INTO Ratings(bidder_email, seller_email, rating_date, rating, rating_description) VALUES (?,?,?,?,?)"
        val = (bidder_email, seller_email, rating_date, rating, rating_description)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

def request_setup():
    '''This function sets up the requests
       table using the csv file Requests.csv
    '''
    columns = ['request_ID', 'sender_email', 'helpdesk_staff_email', 'request_type', 'request_description', 'request_status']
    data = pd.read_csv('data/Requests.csv', names=columns, header=0)
    col1 = data['request_ID'].values
    col2 = data['sender_email'].values
    col3 = data['helpdesk_staff_email'].values
    col4 = data['request_type'].values
    col5 = data['request_description'].values
    col6 = data['request_status'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Requests(request_ID INTEGER, sender_email VARCHAR(50), helpdesk_staff_email VARCHAR(50), request_type VARCHAR(50), request_description VARCHAR(200), request_status INTEGER, PRIMARY KEY (request_ID), FOREIGN KEY (sender_email) REFERENCES Users(email), FOREIGN KEY (helpdesk_staff_email) REFERENCES Helpdesk(email))')

    for i in range(len(col1)):
        request_ID = int(str(col1[i]))
        sender_email = col2[i]
        helpdesk_staff_email = col3[i]
        request_type = col4[i]
        request_description = col5[i]
        request_status = int(str(col6[i]))
        sql = "INSERT OR IGNORE INTO Requests(request_ID, sender_email, helpdesk_staff_email, request_type, request_description, request_status) VALUES (?,?,?,?,?,?)"
        val = (request_ID, sender_email, helpdesk_staff_email, request_type, request_description, request_status)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

def transaction_setup():
    '''This function sets up the
       transaction table using the csv file
       Transactions.csv
    '''
    columns = ['transaction_ID', 'seller_email', 'listing_ID', 'bidder_email', 'date', 'payment']
    data = pd.read_csv('data/Transactions.csv', names=columns, header=0)
    col1 = data['transaction_ID'].values
    col2 = data['seller_email'].values
    col3 = data['listing_ID'].values
    col4 = data['bidder_email'].values
    col5 = data['date'].values
    col6 = data['payment'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Transactions(transaction_ID INTEGER, seller_email VARCHAR(50), listing_ID INTEGER, bidder_email VARCHAR(50), transaction_date VARCHAR(50), payment REAL, PRIMARY KEY (transaction_ID), FOREIGN KEY (seller_email) REFERENCES Sellers(email), FOREIGN KEY (listing_ID) REFERENCES Auction_Listings(listing_ID), FOREIGN KEY (bidder_email) REFERENCES Bidders(email))')

    for i in range(len(col1)):
        transaction_ID = int(str(col1[i]))
        seller_email = col2[i]
        listing_ID = int(str(col3[i]))
        bidder_email = col4[i]
        transaction_date = col5[i]
        payment = float(str(col6[i]))
        sql = "INSERT OR IGNORE INTO Transactions(transaction_ID, seller_email, listing_ID, bidder_email, transaction_date, payment) VALUES (?,?,?,?,?,?)"
        val = (transaction_ID, seller_email, listing_ID, bidder_email, transaction_date, payment)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

def zipcode_setup():
    '''This function sets up the zipcode
       table using the csv file
       Zipcode_Info.csv
    '''
    columns = ['zipcode', 'city', 'state']
    data = pd.read_csv('data/Zipcode_Info.csv', names=columns, header=0)
    col1 = data['zipcode'].values
    col2 = data['city'].values
    col3 = data['state'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Zipcodes(zipcode INTEGER, city VARCHAR(50), zipcode_state VARCHAR(50), PRIMARY KEY(zipcode))')

    for i in range(len(col1)):
        zipcode = int(str(col1[i]))
        city = col2[i]
        zipcode_state = col3[i]
        sql = "INSERT OR IGNORE INTO Zipcodes(zipcode, city, zipcode_state) VALUES (?,?,?)"
        val = (zipcode, city, zipcode_state)
        cursor.execute(sql, val)
        conn.commit()
    return cursor.fetchall()

database_setup() # Call the database_setup function to setup the database before launching NittanyAuction
app = Flask(__name__)
''' These next three lines setup the sessions
    that will be used to store state information
    needed for other functionalities.
'''
app.config["SESSION_PERMANENT"] = False     # Sessions expire when browser closes
app.config["SESSION_TYPE"] = "filesystem"     # Store session data on the filesystem
Session(app)

@app.route('/')
def index():
    '''This function displays the main homepage
       index.html
    '''
    session['webpage'] = 'index'
    return render_template('index.html')

@app.route('/login.html', methods=['POST', 'GET'])
def login():
    '''This function displays the login page
       and handles the user input. Based on
       the input the function will determine
       if the user has an invalid username/
       password, or the user is trying to
       login into a role they don't have
    '''
    error = None
    session['webpage'] = 'login'
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
                    session['email'] = email
                    session['password'] = password
                    return redirect(url_for('bidder', email=email))
                else: error = "Invalid username or password for bidder"
            elif role == "seller": #SELLER ROLE CHECK
                cursor.execute("SELECT * FROM Sellers WHERE email=?", (email,))
                if cursor.fetchone():
                    conn.close()
                    session['email'] = email
                    return redirect(url_for('seller', email=email))
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

@app.route('/registration.html', methods=['POST', 'GET'])
def user_registration():
    '''This function displays the registration
       page and handles the user input. Based
       on the input, the function will check
       to see if the email address is already
       in the system. If not, then the newly
       created user will be directed to the login
       page where they can log in. If the user
       selects the sellers role, then they
       will need to determine if their role
       is just a regular seller or a local
       vendor before proceeding to the login
       page.
    '''
    error = None
    session['webpage'] = 'registration'
    if request.method == "POST":
        user_role = request.form['role']
        user_email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE email= ?",
                       (user_email,))  # sees if user exists in Users table
        user = cursor.fetchone()

        if user:
            error = "User email already exists! try a different email."
        else:
            if user_role == "buyer":
                cursor.execute("INSERT OR IGNORE INTO Users(email, password) VALUES (?,?)", (user_email, hashed_password,))
                home_address_id = hashlib.md5(user_email.encode()).hexdigest()
                cursor.execute("INSERT OR IGNORE INTO Bidders(email, first_name, last_name, age, home_address_id, major) VALUES (?, NULL, NULL, NULL, ?, NULL)", (user_email,home_address_id,))
                cursor.execute("INSERT OR IGNORE INTO Address(address_ID, zipcode, street_number, street_name) VALUES (?,0, NULL, NULL)", (home_address_id,))
                cursor.execute("INSERT OR IGNORE INTO Zipcodes(zipcode, city, zipcode_state) VALUES (0, NULL, NULL)")
            elif user_role == "seller":
                session['email'] = user_email
                session['password'] = hashed_password
                return redirect(url_for('seller_or_vendor', error=error))
            elif user_role == "helpdesk":
                cursor.execute("INSERT OR IGNORE INTO Users(email, password) VALUES (?,?)", (user_email, hashed_password,))
                cursor.execute("INSERT OR IGNORE INTO Helpdesk(email, position) VALUES (?, NULL)", (user_email,))
            else:
                error = "User role not recognized! Select one of the user roles displayed"
            conn.commit()
            conn.close()
            return redirect(url_for('login'))

    return render_template('/registration.html', error=error)

@app.route('/seller_or_vendor.html', methods=['POST', 'GET'])
def seller_or_vendor():
    '''This function displays the seller or
       local vendors webpage and handles
       the user input. Based on the user
       input, the function will then
       assign the newly created user into
       the proper role specific table.
    '''
    error=None
    if request.method == "POST":
        seller_role = request.form['seller_role']
        user_email = session.get('email')
        user_password = session.get('password')
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        if seller_role == "seller":
            cursor.execute("INSERT INTO Users(email, password) VALUES (?,?)", (user_email, user_password,))
            cursor.execute("INSERT INTO Sellers(email, bank_routing_number, bank_account_number, balance) VALUES (?, NULL, NULL, 0)", (user_email,))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        else:
            business_address_id = hashlib.md5(user_email.encode()).hexdigest()
            cursor.execute("INSERT INTO Users(email, password) VALUES (?,?)", (user_email, user_password,))
            cursor.execute("INSERT INTO Sellers(email, bank_routing_number, bank_account_number, balance) VALUES (?, NULL, NULL, 0)",(user_email,))
            cursor.execute("INSERT INTO Local_Vendors(email, business_name, business_address_id, customer_service_phone_number) VALUES (?,NULL,?,NULL)", (user_email,business_address_id,))
            cursor.execute("INSERT INTO Address(address_ID, zipcode, street_number, street_name) VALUES (?,0,NULL,NULL)", (business_address_id,))
            cursor.execute("INSERT OR IGNORE INTO Zipcodes(zipcode, city, zipcode_state) VALUES (0, NULL, NULL)")
            conn.commit()
            conn.close()
            return redirect(url_for('login'))

    return render_template('seller_or_vendor.html', error=error)
@app.route('/change_password.html', methods=['POST', 'GET'])
def change_password():
    '''This function displays the change
       password webpage and handles the
       user input. Based on the user
       input, the function will then
       check to see if the user email
       address doesn't exist, if the
       new password field is empty, if the
       confirm new password field is empty,
       if the new password field and the
       confirm new password field are not
       equal to each other, and if the
       new password is equal to the current
       password. If the user input is valid,
       then the new password is then hashed
       using SHA256 and stored in the proper
       row of the Users table.
    '''
    error = None
    previous_webpage = session.get('webpage')
    if request.method == "POST":
        user_email = request.form['email']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE email = ?", (user_email,))
        user = cursor.fetchone()
        if user:
            old_password = user[1]
            if old_password == hashlib.sha256(new_password.encode()).hexdigest():
                error = "New password equals old password, enter a different password"
            else:
                if new_password != confirm_new_password:
                    error = "New Password and Confirm New Password do not match! Check both fields again."
                else:
                    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                    cursor.execute("UPDATE Users Set password = ? WHERE email LIKE ?", (hashed_password,user_email,))
                    conn.commit()
                    conn.close()
                    if previous_webpage == 'bidder_settings':
                        return redirect(url_for('bidder_settings'))
                    elif previous_webpage == 'seller_settings':
                        return redirect(url_for('seller_settings'))
                    else:
                        return redirect(url_for('login'))
        else:
            error = "User with that email address does not exist! type in a valid email address or register a new account."

    return render_template('/change_password.html', error=error, previous_webpage=previous_webpage)
@app.route('/bidder.html')
def bidder():
    '''This function displays the bidder homepage
       and handles the user input that will
       direct them to different ares of
       NittanyAuction.
    '''
    email = session.get('email')
    session['role'] = 'bidder'
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()
    cursor.execute("SELECT B.home_address_id FROM Bidders B, Users U WHERE U.email = ? AND U.email = B.email", (email,))
    home_address = str(cursor.fetchone()[0])
    session['webpage'] = 'bidder'
    session['address_id'] = home_address
    return render_template('bidder.html', email=email)

@app.route('/bidder_settings.html')
def bidder_settings():
    '''This function displays the bidder
       settings webpage and handles the
       user input that will take them
       to different webpages to change
       any user settings available to
       their role.
    '''
    session['webpage'] = 'bidder_settings'
    email = session.get('email')
    password = session.get('password')
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bidders WHERE email = ?", (email,))
    user = cursor.fetchone()
    firstname = user[1]
    lastname = user[2]
    age = user[3]
    major = user[5]
    return render_template('bidder_settings.html', email=email, firstname=firstname, lastname=lastname, age=age, major=major)

@app.route('/seller.html')
def seller():
    '''This function displays the seller
       homepage and handles the user input
       that will direct the user to different
       areas of NittanyAuction.
    '''
    session['webpage'] = 'seller'
    user_email = session.get('email')
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sellers WHERE email = ?", (user_email,))
    seller = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM Local_Vendors WHERE email = ?", (user_email,))
    local_vendor = cursor.fetchone()
    if local_vendor == None:
        session['role'] = 'seller'
    elif local_vendor[0] == seller:
        session['role'] = 'local_vendor'
        cursor.execute("SELECT L.business_address_id FROM Local_Vendors L, Users U WHERE U.email = ? AND U.email = L.email",(user_email,))
        business_address = str(cursor.fetchone()[0])
        session['address_id'] = business_address

    return render_template('seller.html', email=user_email)

@app.route('/seller_settings.html', methods=["GET", "POST"])
def seller_settings():
    '''This function displays the seller
       settings webpage and handles the
       user input that will take them to
       different webpages to change
       any user settings available for
       their role.
    '''
    email = session.get('email')
    user_role = session.get('role')
    session['webpage'] = 'seller_settings'
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sellers WHERE email = ?", (email,))
    seller_info = cursor.fetchone()
    bank_routing_number = str(seller_info[1])
    bank_account_number = str(seller_info[2])
    balance = float(str(seller_info[3]))
    return render_template('seller_settings.html', email=email, bank_routing_number=bank_routing_number, bank_account_number=bank_account_number, balance=balance, role=user_role)

@app.route('/change_bank_routing_number.html', methods=['POST', 'GET'])
def change_bank_routing_number():
    '''This function displays the change
       bank routing number portal and
       handles the user input. Based on the
       user input, the function will check
       to see if the new routing number is
       the same as the current routing number,
       if the new routing number field is
       empty, and if the new routing number
       is in an incorrect format. If the user
       input is valid, the function will update
       the proper row in the sellers table with
       the new routing number.
    '''
    error=None
    if request.method == "POST":
        new_bank_routing_number = str(request.form['new_bank_routing_number'])
        user_email = session.get('email')
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sellers WHERE email = ?", (user_email,))
        current_bank_routing_number = cursor.fetchone()[1]
        bank_routing_number_format = r'[0-9]{4}-[0-9]{4}-[0-9]'
        match = re.search(bank_routing_number_format, new_bank_routing_number)
        if match == None:
            error = "New Bank Routing Number is in the incorrect format: Enter a valid bank routing number using the format above!"
        elif match and len(new_bank_routing_number) > 11:
            error = "New Bank Routing Number is in the incorrect format: Enter a valid bank routing number using the format above!"
        elif new_bank_routing_number == current_bank_routing_number:
            error = "New Bank Routing Number is the same as the current Bank Routing Number! Enter a different Bank Routing Number!"
        elif new_bank_routing_number == "":
            error = "New Bank Routing Number field is empty! Enter a valid Bank Routing Number using the format above!"
        else:
            cursor.execute("UPDATE Sellers SET bank_routing_number = ? WHERE email = ?", (new_bank_routing_number, user_email))
            conn.commit()
            conn.close()
            return redirect(url_for('seller_settings'))

    return render_template('change_bank_routing_number.html', error=error)

@app.route("/change_bank_account_number.html", methods=['POST', 'GET'])
def change_bank_account_number():
    '''This function displays the change
       bank account number portal and handles
       the user input. Based on the user input,
       the function will check to see if the
       new bank account number is in an incorrect
       format, if the new bank account number
       is the same as the current bank account
       number, and if the new bank account number
       field is empty. If the user input is valid,
       then the function will update the proper
       row in the sellers table with the new
       bank account number.
    '''
    error=None
    if request.method == "POST":
        new_bank_account_number = str(request.form['change_bank_account_number'])
        user_email = session.get('email')
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sellers WHERE email = ?", (user_email,))
        current_bank_account_number = cursor.fetchone()[2]
        bank_account_number_format = r'[0-9]{8}'
        match = re.search(bank_account_number_format, new_bank_account_number)
        if match == None:
            error = "Inputted Bank Account Number is in the incorrect format! Enter a valid Bank Account Number using the format above!"
        elif match and len(new_bank_account_number) > 8:
            error = "Inputted Bank Account Number is in the incorrect format! Enter a valid Bank Account Number using the format above!"
        elif new_bank_account_number == current_bank_account_number:
            error = "New Bank Account Number is the same as the Current Bank Account Number! Enter a different Bank Account Number!"
        elif new_bank_account_number == "":
            error = "New Bank Account Number field is empty! Enter a valid Bank Account Number using the format above!"
        else:
            cursor.execute("UPDATE Sellers SET bank_account_number = ? WHERE email = ?", (new_bank_account_number, user_email))
            conn.commit()
            conn.close()
            return redirect(url_for('seller_settings'))

    return render_template('change_bank_account_number.html', error=error)
@app.route('/local_vendor_settings.html')
def local_vendor_settings():
    '''This function displays the local vendor
       settings webpage and handles the user
       input that will take them to different
       webpages that will allow the user to
       change settings that are available to
       their role.
    '''
    email = session.get('email')
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Local_Vendors WHERE email = ?", (email,))
    local_vendor_info = cursor.fetchone()
    business_name = local_vendor_info[1]
    customer_service_phone_number = local_vendor_info[3]
    return render_template('local_vendor_settings.html', business_name=business_name, customer_service_phone_number=customer_service_phone_number)

@app.route('/change_business_name.html', methods=['POST', 'GET'])
def change_business_name():
    '''This function displays the change
       business name portal and handles the
       user input. Based on the user input,
       the function will check to see if the
       new business name field is empty, and if
       the new business name is the same as
       the current business name. If the
       user input is valid, then the function
       will update the proper row in the
       local vendors table with the new
       business name.
    '''
    error=None
    if request.method == "POST":
        email = session.get('email')
        new_business_name = str(request.form['new_business_name'])
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Local_Vendors WHERE email = ?", (email,))
        current_business_name = cursor.fetchone()
        if current_business_name == None:
            current_business_name = ""
        else:
            current_business_name = str(current_business_name[1])

        if new_business_name == "":
            error = "New Business Name field is empty! Type in a new Business Name!"
        elif new_business_name == current_business_name:
            error = "New Business Name is the same as the Current Business Name! Type in a different Business Name!"
        else:
            cursor.execute("UPDATE Local_Vendors SET business_name = ? WHERE email = ?", (new_business_name, email,))
            conn.commit()
            conn.close()
            return redirect(url_for('local_vendor_settings'))

    return render_template("change_business_name.html", error=error)

@app.route('/change_customer_service_phone_number.html', methods=['POST', 'GET'])
def change_customer_service_phone_number():
    '''This function displays the change
       customer service phone number portal
       and handles the user input. Based on
       the user input, the function will
       check to see if the new phone number
       is in an incorrect format, if the new
       phone number field is empty, and if the
       new phone number is the same as the
       current phone number. If the user
       input is valid, the function will
       update the proper row in the local
       vendors table with the new customer
       service phone number.
    '''
    error=None
    if request.method == "POST":
        email = session.get('email')
        new_service_phone_number = str(request.form['new_customer_service_phone_number'])
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Local_Vendors")
        current_service_phone_number = cursor.fetchall()
        phone_number_format = r'[0-9]{3}-[0-9]{3}-[0-9]{4}'
        match = re.search(phone_number_format, new_service_phone_number)
        if match == None:
            error = "Inputted Phone Number is in an invalid format! Type in a phone number based on the format above!"
        elif match and len(new_service_phone_number) > 12:
            error = "Inputted Phone Number is in an invalid format! Type in a phone number based on the format above!"
        elif new_service_phone_number == "":
            error = "Phone Number field is empty! Type in a phone number based on the format above!"
        elif new_service_phone_number == current_service_phone_number:
            error = "New Phone Number is the same as the Current Phone Number! Type in a different phone number!"
        else:
            for iterator in range(len(current_service_phone_number)):
                if new_service_phone_number == str(current_service_phone_number[iterator][3]) and str(current_service_phone_number[iterator][0]) != email:
                    error = "Inputted Phone Number already exists with another vendor! Type in a different Phone Number based on the format above!"
                elif new_service_phone_number == str(current_service_phone_number[iterator][3]) and str(current_service_phone_number[iterator][0]) == email:
                    error = "New Phone Number is the same as the Current Phone Number! Type in a different phone number!"
                else:
                    pass

            if error == "Inputted Phone Number already exists with another vendor! Type in a different Phone Number based on the format above!":
                error = "Inputted Phone Number already exists with another vendor! Type in a different Phone Number based on the format above!"
            elif error == "New Phone Number is the same as the Current Phone Number! Type in a different phone number!":
                error = "New Phone Number is the same as the Current Phone Number! Type in a different phone number!"
            else:
                cursor.execute("UPDATE Local_Vendors SET customer_service_phone_number = ? WHERE email = ?", (new_service_phone_number, email,))
                conn.commit()
                conn.close()
                return redirect(url_for('local_vendor_settings'))

    return render_template("change_customer_service_phone_number.html", error=error)
@app.route('/helpdesk.html')
def helpdesk():
    '''This function displays the helpdesk
       homepage.
    '''
    session['webpage'] = 'helpdesk'
    return render_template('helpdesk.html')

@app.route('/change_firstname.html', methods=['POST', 'GET'])
def change_firstname():
    '''This function displays the change
       first name portal and handles the
       user input. Based on the user input,
       the function will check to see if
       the new firstname is the same as the
       current firstname, and if the new
       firstname field is empty. If the user
       input is valid, the function will
       update proper row in the bidders table
       with the new firstname.
    '''
    error = None
    session['webpage'] = 'change_firstname'
    if request.method == "POST":
        new_firstname = str(request.form['new_firstname'])
        user_email = session.get('email')
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bidders WHERE email = ?", (user_email,))
        current_firstname = cursor.fetchone()[1]
        if current_firstname == None:
            current_firstname = ""
        else:
            current_firstname = str(current_firstname)

        if new_firstname == "":
            error = "First Name field cannot be empty! enter a new first name again!"
        elif new_firstname == current_firstname:
            error = "New First Name is the Same as the Old First Name! Type in a different first name!"
        else:
            cursor.execute("UPDATE Bidders SET first_name = ? WHERE email LIKE ?", (new_firstname,user_email,))
            conn.commit()
            conn.close()
            return redirect(url_for('bidder_settings'))

    return render_template('change_firstname.html', error=error)

@app.route('/change_lastname.html', methods=['POST', 'GET'])
def change_lastname():
    '''This function displays the change
       last name portal and handles the
       user input. Based on the user input,
       the function will check to see if the
       new lastname field is empty, and if
       the new lastname is the same as the
       current lastname. If the user input
       is valid, the function will update
       the proper row in the bidders table
       with the new lastname.
    '''
    error = None
    session['webpage'] = 'change_lastname'
    if request.method == "POST":
        new_lastname = str(request.form['new_lastname'])
        user_email = session.get('email')
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bidders WHERE email = ?", (user_email,))
        current_lastname = cursor.fetchone()[2]
        if current_lastname == None:
            current_lastname = ""
        else:
            current_lastname = str(current_lastname)
        if new_lastname == "":
            error = "Last Name field cannot be empty! enter a new last name again!"
        elif new_lastname == current_lastname:
            error = "New Last Name is the same as the Old Last Name! Type in a different last name!"
        else:
            cursor.execute("UPDATE Bidders SET last_name = ? WHERE email LIKE ?", (new_lastname, user_email,))
            conn.commit()
            conn.close()
            return redirect(url_for('bidder_settings'))
    return render_template('change_lastname.html', error=error)

@app.route('/change_age.html', methods=['POST', 'GET'])
def change_age():
    '''This function displays the change age
       portal and handles the user input.
       Based on the user input, the function
       will check to see if the new age field
       is empty, if the new age is a non-positive
       number, and if the new age is the same
       as the current age. If the user input is
       valid, the function will update the proper
       row in the bidders table with the new age.
    '''
    error = None
    session['webpage'] = 'change_age'
    if request.method == "POST":
        new_age = int(str(request.form['new_age']))
        user_email = session.get('email')
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bidders WHERE email = ?", (user_email,))
        current_age = cursor.fetchone()[3]
        if current_age == None:
            current_age = 0
        else:
            current_age = int(str(current_age))

        if new_age == None:
            error = "Age field cannot be empty! Select an age using the number selector!"
        elif new_age == current_age:
            error = "New Age is the same as the Old Age! Select or Type in a different Age!"
        elif new_age <= 0:
            error = "Age must be a positive number! Select or type in a positive age!"
        else:
            cursor.execute("UPDATE Bidders SET age = ? WHERE email Like ?", (new_age, user_email,))
            conn.commit()
            conn.close()
            return redirect(url_for('bidder_settings'))
    return render_template('change_age.html', error=error)

@app.route("/change_major.html", methods=['POST', 'GET'])
def change_major():
    '''This function displays the change
       major portal and handles the user
       input. Based on the user input, the
       function will check to see if the
       new major field is empty, and if
       the new major is the same as the
       current major. If the user input is
       valid, the function will update the
       proper row in the bidders table with
       the new major.
    '''
    error = None
    session['webpage'] = 'change_major'
    if request.method == "POST":
        new_major = str(request.form['new_major'])
        user_email = session.get('email')
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Bidders WHERE email = ?", (user_email,))
        current_major = cursor.fetchone()[5]
        if current_major == None:
            current_major = ""
        else:
            current_major = str(current_major)

        if new_major == "":
            error = "Major field cannot be empty! Type in a major again!"
        elif new_major == current_major:
            error = "New Major is the same as the Old Major! Type in a different major again!"
        else:
            cursor.execute("UPDATE Bidders SET major = ? WHERE email LIKE ?", (new_major, user_email,))
            conn.commit()
            conn.close()
            return redirect(url_for('bidder_settings'))

    return render_template('change_major.html', error=error)

@app.route("/change_address.html")
def change_address_settings():
    '''This function displays the change address
        settings webpage and handles the user
        input that will take them to different
        webpages that will allow the user to
        change settings that are available to
        their role (bidder or local vendors).
    '''
    email = session.get('email')
    session['webpage'] = 'change_address'
    role = session.get('role')
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()
    if role == 'bidder':
        cursor.execute("SELECT A.address_ID, A.zipcode, A.street_number, A.street_name FROM Bidders B, Address A WHERE B.email = ? AND B.home_address_id = A.address_ID", (email,))
        previous_webpage = "/bidder_settings.html"
    else:
        cursor.execute("SELECT A.address_ID, A.zipcode, A.street_number, A.street_name FROM Local_Vendors L, Address A WHERE L.email = ? AND L.business_address_id = A.address_ID", (email,))
        previous_webpage = "/local_vendor_settings.html"
    address = cursor.fetchone()
    zipcode = address[1]
    street_number = address[2]
    street_name = address[3]
    return render_template('change_address.html', zipcode=zipcode, street_number=street_number, street_name=street_name, previous_webpage=previous_webpage)

@app.route("/change_zipcode_settings.html", methods=['POST', 'GET'])
def change_zipcode():
    '''This function displays the change zipcode
       settings webpage and handles the user
       input that will take them to different
       webpages that will allow the user to
       change settings that are available to
       their role.
    '''
    email = session.get('email')
    session['webpage'] = 'change_zipcode_settings'
    role = session.get('role')
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()
    if role == 'bidder':
        cursor.execute("SELECT Z.zipcode, Z.city, Z.zipcode_state FROM Zipcodes Z, Address A, Bidders B WHERE B.email = ? AND B.home_address_id = A.address_ID AND A.zipcode = Z.zipcode", (email,))
    else:
        cursor.execute(
            "SELECT Z.zipcode, Z.city, Z.zipcode_state FROM Zipcodes Z, Address A, Local_Vendors L WHERE L.email = ? AND L.business_address_id = A.address_ID AND A.zipcode = Z.zipcode",(email,))
    zipcode = cursor.fetchone()
    zipcode_number = int(str(zipcode[0]))
    city = zipcode[1]
    zipcode_state = zipcode[2]

    return render_template('change_zipcode_settings.html', zipcode_number=zipcode_number, city=city, zipcode_state=zipcode_state)

@app.route("/change_zipcode_number.html", methods=['POST', 'GET'])
def change_zipcode_number():
    '''This function displays the change
       zipcode number portal and handles
       the user input. Based on the user
       input, the function will check to
       see if the new zipcode number is 0 (
       0 is the default zipcode number upon
       creation. The user will need to change
       this zipcode number to a positive
       zipcode number.), if the new zipcode
       number field is empty, and if the
       new zipcode number is the same as the
       current zipcode number. If the user
       input is valid, then the function
       will check to see if the user inputted
       a new zipcode number or an existing
       zipcode number in the zipcodes table.
       If the user inputted a new zipcode number,
       the user will be taken to another portal
       to input the city and state associated
       with the new zipcode number. Otherwise,
       the function will update the proper
       row in the address table with the new
       zipcode number.
    '''
    error=""
    session['webpage'] = 'change_zipcode_number'
    if request.method == "POST":
        new_zipcode_number = int(str(request.form['new_zipcode_number']))
        print(new_zipcode_number)
        user_email = session.get('email')
        user_address_id = session.get('address_id')
        role = session.get('role')
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        if role == 'bidder':
            cursor.execute("SELECT Z.zipcode, Z.city, Z.zipcode_state FROM Zipcodes Z, Address A, Bidders B WHERE B.email = ? AND B.home_address_id = A.address_ID AND A.zipcode = Z.zipcode",(user_email,))
        else:
            cursor.execute("SELECT Z.zipcode, Z.city, Z.zipcode_state FROM Zipcodes Z, Address A, Local_Vendors L WHERE L.email = ? AND L.business_address_id = A.address_ID AND A.zipcode = Z.zipcode",(user_email,))
        current_zipcode_number = int(str(cursor.fetchone()[0]))
        if new_zipcode_number == 0:
            error = "Zipcode cannot be 0. Select or type in a positive Zipcode!"
        elif new_zipcode_number == None:
            error = "Zipcode field cannot be empty! enter a new zipcode again!"
        elif new_zipcode_number < 0:
            error = "Zipcode cannot be negative. Select or type in a positive Zipcode!"
        else:
            cursor.execute("SELECT * FROM Zipcodes WHERE zipcode = ?", (new_zipcode_number,))
            current_zipcode_number = cursor.fetchall()
            if len(current_zipcode_number) == 1:
                cursor.execute("UPDATE Address SET zipcode = ? WHERE address_ID = ?",
                               (new_zipcode_number, user_address_id,))
                conn.commit()
                conn.close()
                city = str(current_zipcode_number[0][1])
                zipcode_state = str(current_zipcode_number[0][2])
                return render_template('change_zipcode_settings.html', zipcode_number=new_zipcode_number, city=city, zipcode_state=zipcode_state)
            else:
                session['zipcode'] = str(new_zipcode_number)
                return redirect(url_for('change_city_state', error=error))
    return render_template('change_zipcode_number.html', error=error)

@app.route("/change_city_state.html", methods=['POST', 'GET'])
def change_city_state():
    '''This function handles the change
       city and state portal and handles the
       user input. Based on the user input,
       the function will check to see if the
       new city or new state fields are empty,
       and if the new city/state pair already exist
       for another zipcode number. If the user
       input is valid, then the function will
       update the proper row in the address table
       with the new zipcode number. Then, the
       function will insert the new zipcode number,
       the new city name, and the new state into
       a new row.
    '''
    error=None
    if request.method == "POST":
        zipcode_number = int(session.get('zipcode'))
        user_address_id = session.get('address_id')
        new_city_name = str(request.form['new_city'])
        new_state_name = str(request.form['new_state'])
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Zipcodes WHERE city = ? AND zipcode_state = ?", (new_city_name, new_state_name,))
        city_state_name_check = cursor.fetchall()
        if(len(city_state_name_check) >= 1):
            error = "Zipcode with the inputted city name and state already exists! input a new city name or a new state name!"
        else:
            cursor.execute("UPDATE Address SET zipcode = ? WHERE address_ID = ?",
                           (zipcode_number, user_address_id,))
            cursor.execute("INSERT OR IGNORE INTO Zipcodes(zipcode, city, zipcode_state) VALUES (?,?,?)", (zipcode_number, new_city_name, new_state_name,))
            conn.commit()
            conn.close()
            return render_template('change_zipcode_settings.html', zipcode_number=zipcode_number, city=new_city_name, zipcode_state=new_state_name)

    return render_template('change_city_state.html', error=error)

@app.route("/change_street_number.html", methods=['POST', 'GET'])
def change_street_number():
    '''This function displays the change
       street number portal and handles the
       user input. Based on the user input,
       the function will check to see if the
       new street number is a non-positive
       number, and if the new street number
       is the same as the current street
       number. If the user input is valid,
       then the function will update the
       proper row in the address table with
       the new street number.
    '''
    error=None
    if request.method == "POST":
        new_street_number = int(str(request.form['new_street_number']))
        user_email = session.get('email')
        user_address_id = session.get('address_id')
        role = session.get('role')
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        if role == 'bidder':
            cursor.execute("SELECT A.address_ID, A.zipcode, A.street_number, A.street_name FROM Address A, Bidders B WHERE B.email = ? AND B.home_address_id = A.address_ID", (user_email,))
        else:
            cursor.execute("SELECT A.address_ID, A.zipcode, A.street_number, A.street_name FROM Address A, Local_Vendors L WHERE L.email = ? AND L.business_address_id = A.address_ID",(user_email,))
        current_address = cursor.fetchone()
        current_street_number = current_address[2]
        if current_street_number == None:
            current_street_number = 0
        else:
            current_street_number = int(str(current_street_number))

        if new_street_number == 0:
            error = "Street Number cannot be 0! Select or Type in a positive Street Number!"
        elif new_street_number < 0:
            error = "Street Number cannot be negative! Select or Type in a positive Street Number!"
        elif new_street_number == current_street_number:
            error = "New Street Number is the same as the Current Street Number! Select or Type in a different Street Number!"
        else:
            cursor.execute("UPDATE Address SET street_number = ? WHERE address_ID = ?", (new_street_number, user_address_id,))
            conn.commit()
            conn.close()
            zipcode = int(current_address[1])
            street_name = current_address[3]
            return render_template('change_address.html', zipcode=zipcode, street_number=new_street_number, street_name=street_name)

    return render_template('change_street_number.html', error=error)

@app.route("/change_street_name.html", methods=['POST', 'GET'])
def change_street_name():
    '''This function displays the change
       street name portal and handles the
       user input. Based on the user input,
       the function will check to see if the
       new street name field is empty, and if
       the new street name is the same as
       the current street name. If the user
       input is valid, then the function
       will update the proper row in the
       address table with the new street
       name.
    '''
    error=None
    if request.method == "POST":
        new_street_name = request.form['new_street_name']
        user_email = session.get('email')
        user_address_id = session.get('address_id')
        role = session.get('role')
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        if role == 'bidder':
            cursor.execute("SELECT A.address_ID, A.zipcode, A.street_number, A.street_name FROM Address A, Bidders B WHERE B.email = ? AND B.home_address_id = A.address_ID",(user_email,))
        else:
            cursor.execute("SELECT A.address_ID, A.zipcode, A.street_number, A.street_name FROM Address A, Local_Vendors L WHERE L.email = ? AND L.business_address_id = A.address_ID",(user_email,))
        current_address = cursor.fetchone()
        current_street_name = current_address[3]
        if current_street_name == None:
            current_street_name = ""
        else:
            current_street_name = str(current_street_name)

        if new_street_name == "":
            error = "Street Name field cannot be empty! Enter a Street Name!"
        elif new_street_name == current_street_name:
            error = "New Street Name is the same as the Current Street Name! Type in a different Street Name!"
        else:
            cursor.execute("UPDATE Address SET street_name = ? WHERE address_ID = ?", (new_street_name, user_address_id,))
            conn.commit()
            conn.close()
            zipcode = int(str(current_address[1]))
            street_number = current_address[2]
            return render_template('change_address.html', zipcode=zipcode, street_number=street_number, street_name=new_street_name)

    return render_template('change_street_name.html', error=error)

@app.route('/view_credit_cards.html')
def view_credit_cards():
    '''This function displays the view credit
       card settings webpage (number of
       credit cards the user has) and handles
       the user input that will take them to
       different webpages that will allow
       the user to add/remove credit cards
       associated with their email.(bidder).
    '''
    user_email = session.get('email')
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Credit_Cards C WHERE C.owner_email = ? ", (user_email,))
    number_credit_cards = len(cursor.fetchall())
    return render_template('view_credit_cards.html', number_credit_cards=number_credit_cards)

@app.route('/add_credit_card.html', methods=['POST', 'GET'])
def add_credit_card():
    '''This function displays the add credit
       card portal and handles the user input.
       based on the user input, the function will
       check to see if the new credit card number
       is in an incorrect format, if the new credit
       card number field is empty, if the new
       credit card type field is empty, if the
       new expire month field is empty, if the
       new expire year field is empty, if the
       new security code field is empty, if the
       new credit card number is already registered
       with another user, if the expire month is
       a number not between 1 and 12, if the expire year
       is a number less than 1950, and if the security
       code is a number not between 0 and 999. If the user
       input is valid, then the function will
       insert the new credit card number, new
       credit card type, expire month, expire
       year, security code, and the user email
       into a new row in the credit cards table.
    '''
    error=None
    if request.method == "POST":
        new_credit_card_number = request.form['new_credit_card_number']
        new_credit_card_type = request.form['new_credit_card_type']
        new_expire_month = int(str(request.form['new_expire_month']))
        new_expire_year = int(str(request.form['new_expire_year']))
        new_security_code = int(str(request.form['new_security_code']))
        user_email = session.get('email')
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Credit_Cards")
        duplicate_credit_cards = cursor.fetchall()
        credit_card_number_format_1 = r'(?:[0-9]{4}-){3}[0-9]{4}'
        credit_card_number_format_2 = r'[0-9]{4}-[0-9]{6}-[0-9]{5}'
        credit_card_number_match_1 = re.search(credit_card_number_format_1, new_credit_card_number)
        credit_card_number_match_2 = re.search(credit_card_number_format_2, new_credit_card_number)
        if credit_card_number_match_1 == None and credit_card_number_match_2 == None:
            error = "Credit Card Number is in the incorrect format! Enter in the credit card number using the format above!"
        elif credit_card_number_match_1 and len(new_credit_card_number) > 19:
            error = "Credit Card Number is in the incorrect format! Enter in the credit card number using the format above!"
        elif credit_card_number_match_2 and len(new_credit_card_number) > 17:
            error = "Credit Card Number is in the incorrect format! Enter in the credit card number using the format above!"
        elif (new_credit_card_number == ""):
            error = "Credit Card Number field is empty! Type in a valid credit card number using the format above!"
        else:
            for iterator in range (len(duplicate_credit_cards)):
                if(new_credit_card_number == str(duplicate_credit_cards[iterator][0])):
                    error = "Credit Card with that number already exists! Type in a different credit card number using the format above!"

            if error == "Credit Card with that number already exists! Type in a different credit card number using the format above!":
                error = "Credit Card with that number already exists! Type in a different credit card number using the format above!"

            elif new_credit_card_type == "":
                error = "Credit Card Type field is empty! Type in a valid credit card type!"

            elif new_expire_month < 1 or new_expire_month > 12:
                error = "Expire Month field is not a number between 1 and 12 inclusive! Select or Type In an valid expire month!"

            elif new_expire_year < 1950:
                error = "Expire Year field is not a valid year! Select or Type in a valid expire year!"

            elif new_security_code < 0 or new_security_code > 999:
                error = "Security Code field is not valid! Select or Type In a security code between 0 and 999!"
            else:
                cursor.execute("INSERT OR IGNORE INTO Credit_Cards(credit_card_num, card_type, expire_month, expire_year, security_code, owner_email) VALUES (?,?,?,?,?,?)", (new_credit_card_number,new_credit_card_type,new_expire_month,new_expire_year,new_security_code,user_email,))
                conn.commit()
                cursor.execute("SELECT * FROM Credit_Cards C WHERE C.owner_email = ?", (user_email,))
                number_credit_cards = len(cursor.fetchall())
                return render_template('view_credit_cards.html', number_credit_cards=number_credit_cards)

    return render_template('add_credit_card.html', error=error)

@app.route('/remove_credit_card.html', methods=['POST', 'GET'])
def remove_credit_card():
    '''This function displays the remove
       credit card portal and handles the
       user input. Based on the user input,
       the function will check to see if
       the credit card number is in an
       incorrect format, if the credit
       card number is associated with a
       different email, and if the
       remove credit card number field is
       empty. If the user input is valid,
       then the function will use the
       DELETE FROM SQL command to remove
       the row associated with the user email
       and the inputted credit card number.
    '''
    error = None
    if request.method == 'POST':
        credit_card_number = request.form['delete_credit_card']
        user_email = session.get('email')
        conn = sqlite3.connect("NittanyAuctionDB")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Credit_Cards")
        duplicate_credit_cards = cursor.fetchall()
        credit_card_number_format_1 = r'(?:[0-9]{4}-){3}[0-9]{4}'
        credit_card_number_format_2 = r'[0-9]{4}-[0-9]{6}-[0-9]{5}'
        credit_card_number_match_1 = re.search(credit_card_number_format_1, credit_card_number)
        credit_card_number_match_2 = re.search(credit_card_number_format_2, credit_card_number)
        if credit_card_number_match_1 == None and credit_card_number_match_2 == None:
            error = "Credit Card Number is in the incorrect format! Enter in the credit card number using the format above!"
        elif credit_card_number_match_1 and len(credit_card_number) > 19:
            error = "Credit Card Number is in the incorrect format! Enter in the credit card number using the format above!"
        elif credit_card_number_match_2 and len(credit_card_number) > 17:
            error = "Credit Card Number is in the incorrect format! Enter in the credit card number using the format above!"
        elif (credit_card_number == ""):
            error = "Credit Card Number field is empty! Type in a valid credit card number using the format above!"
        else:
            for iterator in range(len(duplicate_credit_cards)):
                if (credit_card_number == str(duplicate_credit_cards[iterator][0]) and user_email != str(duplicate_credit_cards[iterator][5])):
                    error = "Credit Card with that number is owned by a different account! Type in a credit card number you own!"

            if error == "Credit Card with that number is owned by a different account! Type in a credit card number you own!":
                error = "Credit Card with that number is owned by a different account! Type in a credit card number you own!"

            else:
                cursor.execute("DELETE FROM Credit_Cards WHERE owner_email = ? AND credit_card_num = ?", (user_email, credit_card_number))
                conn.commit()
                cursor.execute("SELECT * FROM Credit_Cards C WHERE C.owner_email = ?", (user_email,))
                number_credit_cards = len(cursor.fetchall())
                return render_template('view_credit_cards.html', number_credit_cards=number_credit_cards)

    return render_template('remove_credit_card.html', error=error)

@app.route("/product_listings.html", methods=['POST', 'GET'])
def product_listings():
    '''This function displays the product
       listing webpage and allows users to
       click on subcategories to explore
       what other subcategories exist
       inside of the clicked-on
       parent category.
    '''
    category_selected= request.args.get("category_name","All")#All is root categroy
    conn = sqlite3.connect("NittanyAuctionDB")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT category_name, parent_category FROM Categories")#get the categories and parents
    rows = cursor.fetchall()

    categories =[]#array of tuples of categories with their name, parents and children
    for row in rows:#each row in the rows of categories from databse
        category = {"category_name":row["category_name"],"parent_category":row["parent_category"],"children":[]}
        categories.append(category)
    categoriesD = {}#categories dictionary
    for category in categories:#adding each category to the dictionary so easier to access parent name and children
        categoriesD[category["category_name"]] = category

    category_hierarchy = []#the actual hierarchy of categories so subcategories appear underneath their parent
    for category in categories:
        parent_name = category["parent_category"]#get the parent name of current category
        if parent_name == "Root":#to find 1st level of children under root cat
            category_hierarchy.append(category)
        else:#all other subcategories not directly under root
            parent = categoriesD.get(parent_name)#get the parent name from cat dictionary
            if parent: parent["children"].append(category)

    if category_selected=="All":#root cat selected
        cursor.execute("SELECT product_name, category FROM Auction_Listings WHERE status=1")#status=1 is active auctions
    else:#more specific cat selected
        cursor.execute("SELECT product_name, category FROM Auction_Listings WHERE category = ? AND status=1", (category_selected,))#status=1 for active auctions
    products= cursor.fetchall()
    conn.close()

    return render_template("product_listings.html", categories=category_hierarchy, products=products, category_selected=category_selected)#sends the cat hierarchy, products in category selected and the category selected

if __name__ == '__main__':
    app.run()
