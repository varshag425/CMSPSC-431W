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
    listing_removals_setup()

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

def listing_removals_setup():
    '''This function sets up the listing removals table using the csv file Listing_Removals.csv'''
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Listing_Removals(listing_ID INTEGER, seller_email VARCHAR(50), removal_reason VARCHAR(300), remaining_bids INTEGER, removal_date VARCHAR(30), PRIMARY KEY(listing_ID), FOREIGN KEY (listing_ID) REFERENCES Auction_Listings(listing_ID), FOREIGN KEY (seller_email) REFERENCES Sellers(email))')

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
                    session['email'] = email
                    return redirect(url_for('helpdesk', email=email))
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
    cursor.execute("SELECT first_name, last_name, home_address_id FROM Bidders WHERE email = ?", (email,))
    user = cursor.fetchone()
    first_name = user[0]
    last_name = user[1]
    home_address = str(user[2])
    session['webpage'] = 'bidder'
    session['address_id'] = home_address
    conn.close()
    return render_template('bidder.html', email=email, first_name=first_name, last_name=last_name)


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


@app.route('/seller_listings.html')
def seller_listings():
    email = session.get('email')
    session['webpage'] = 'seller_listings'
    conn = sqlite3.connect("NittanyAuctionDB")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Auction_Listings WHERE seller_email = ? ORDER BY listing_ID DESC", (email,))
    all_listings = cursor.fetchall()

    active_listings = []
    inactive_listings = []
    sold_listings = []

    for listing in all_listings:
        listing_dict = dict(listing)
        listing_dict['bid_count'] = get_bid_count(listing['listing_ID'])
        listing_dict['remaining_bids'] = int(listing['max_bids']) - int(listing_dict['bid_count'])
        if listing['status'] == 1:
            active_listings.append(listing_dict)
        elif listing['status'] == 0:
            inactive_listings.append(listing_dict)
        elif listing['status'] == 2:
            sold_listings.append(listing_dict)

    conn.close()
    return render_template('seller_listings.html', active_listings=active_listings, inactive_listings=inactive_listings, sold_listings=sold_listings)

@app.route('/create_listing.html', methods=['POST', 'GET'])
def create_listing():
    error = None
    email = session.get('email')
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()
    cursor.execute("SELECT category_name FROM Categories ORDER BY category_name")
    categories = cursor.fetchall()

    if request.method == 'POST':
        auction_title = str(request.form['auction_title']).strip()
        product_name = str(request.form['product_name']).strip()
        product_description = str(request.form['product_description']).strip()
        category = str(request.form['category']).strip()
        quantity = str(request.form['quantity']).strip()
        reserve_price = str(request.form['reserve_price']).strip()
        max_bids = str(request.form['max_bids']).strip()

        if auction_title == "":
            error = "Auction Title field is empty! Type in an Auction Title!"
        elif product_name == "":
            error = "Product Name field is empty! Type in a Product Name!"
        elif category == "":
            error = "Please select a Category!"
        elif quantity == "" or quantity.isdigit() == False or int(quantity) <= 0:
            error = "Quantity must be a positive whole number!"
        elif max_bids == "" or max_bids.isdigit() == False or int(max_bids) <= 0:
            error = "Max Bids must be a positive whole number!"
        else:
            try:
                reserve_price_float = float(reserve_price)
                if reserve_price_float < 0:
                    error = "Reserve Price cannot be negative!"
            except ValueError:
                error = "Reserve Price must be a valid number!"

        if error == None:
            cursor.execute("SELECT MAX(listing_ID) FROM Auction_Listings")
            current_max_listing_id = cursor.fetchone()[0]
            if current_max_listing_id == None:
                new_listing_id = 1
            else:
                new_listing_id = int(current_max_listing_id) + 1

            cursor.execute("INSERT INTO Auction_Listings(seller_email, listing_ID, category, auction_title, product_name, product_description, quantity, reserve_price, max_bids, status) VALUES (?,?,?,?,?,?,?,?,?,?)", (email, new_listing_id, category, auction_title, product_name, product_description, int(quantity), str(reserve_price), int(max_bids), 1))
            conn.commit()
            conn.close()
            return redirect(url_for('seller_listings'))

    conn.close()
    return render_template('create_listing.html', error=error, categories=categories)

@app.route('/edit_listing.html', methods=['POST', 'GET'])
def edit_listing():
    error = None
    email = session.get('email')
    listing_ID = request.args.get('listing_ID')
    if request.method == 'POST':
        listing_ID = request.form['listing_ID']

    if listing_ID == None:
        return redirect(url_for('seller_listings'))

    conn = sqlite3.connect("NittanyAuctionDB")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Auction_Listings WHERE listing_ID = ? AND seller_email = ?", (listing_ID, email))
    listing = cursor.fetchone()
    if listing == None:
        conn.close()
        return redirect(url_for('seller_listings'))

    bid_count = get_bid_count(listing_ID)
    if int(listing['status']) == 2:
        error = "Sold listings cannot be edited!"
    elif int(listing['status']) == 1 and bid_count > 0:
        error = "This active listing already has bids on it, so it cannot be edited!"

    cursor.execute("SELECT category_name FROM Categories ORDER BY category_name")
    categories = cursor.fetchall()

    if request.method == 'POST' and error == None:
        auction_title = str(request.form['auction_title']).strip()
        product_name = str(request.form['product_name']).strip()
        product_description = str(request.form['product_description']).strip()
        category = str(request.form['category']).strip()
        quantity = str(request.form['quantity']).strip()
        reserve_price = str(request.form['reserve_price']).strip()
        max_bids = str(request.form['max_bids']).strip()

        if auction_title == "":
            error = "Auction Title field is empty! Type in an Auction Title!"
        elif product_name == "":
            error = "Product Name field is empty! Type in a Product Name!"
        elif category == "":
            error = "Please select a Category!"
        elif quantity == "" or quantity.isdigit() == False or int(quantity) <= 0:
            error = "Quantity must be a positive whole number!"
        elif max_bids == "" or max_bids.isdigit() == False or int(max_bids) <= 0:
            error = "Max Bids must be a positive whole number!"
        else:
            try:
                reserve_price_float = float(reserve_price)
                if reserve_price_float < 0:
                    error = "Reserve Price cannot be negative!"
            except ValueError:
                error = "Reserve Price must be a valid number!"

        if error == None:
            cursor.execute("UPDATE Auction_Listings SET category = ?, auction_title = ?, product_name = ?, product_description = ?, quantity = ?, reserve_price = ?, max_bids = ? WHERE listing_ID = ? AND seller_email = ?", (category, auction_title, product_name, product_description, int(quantity), str(reserve_price), int(max_bids), int(listing_ID), email))
            conn.commit()
            conn.close()
            return redirect(url_for('seller_listings'))

    listing = dict(listing)
    listing['bid_count'] = bid_count
    listing['remaining_bids'] = int(listing['max_bids']) - int(bid_count)
    conn.close()
    return render_template('edit_listing.html', error=error, listing=listing, categories=categories)

@app.route('/remove_listing.html', methods=['POST', 'GET'])
def remove_listing():
    error = None
    email = session.get('email')
    listing_ID = request.args.get('listing_ID')
    if request.method == 'POST':
        listing_ID = request.form['listing_ID']

    if listing_ID == None:
        return redirect(url_for('seller_listings'))

    conn = sqlite3.connect("NittanyAuctionDB")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Auction_Listings WHERE listing_ID = ? AND seller_email = ?", (listing_ID, email))
    listing = cursor.fetchone()
    if listing == None:
        conn.close()
        return redirect(url_for('seller_listings'))

    bid_count = get_bid_count(listing_ID)
    remaining_bids = int(listing['max_bids']) - int(bid_count)

    if int(listing['status']) != 1:
        error = "Only active listings can be removed from the market!"

    if request.method == 'POST' and error == None:
        removal_reason = str(request.form['removal_reason']).strip()
        if removal_reason == "":
            error = "Removal Reason field is empty! Type in a reason for removing the listing!"
        else:
            cursor.execute("UPDATE Auction_Listings SET status = ? WHERE listing_ID = ? AND seller_email = ?", (0, int(listing_ID), email))
            cursor.execute("INSERT OR REPLACE INTO Listing_Removals(listing_ID, seller_email, removal_reason, remaining_bids, removal_date) VALUES (?,?,?,?,datetime('now'))", (int(listing_ID), email, removal_reason, remaining_bids))
            conn.commit()
            conn.close()
            return redirect(url_for('seller_listings'))

    listing = dict(listing)
    listing['bid_count'] = bid_count
    listing['remaining_bids'] = remaining_bids
    conn.close()
    return render_template('remove_listing.html', error=error, listing=listing)

@app.route('/helpdesk.html', methods=['GET','POST'])
def helpdesk():
    '''This function displays the helpdesk
       homepage.
    '''
    email = session.get('email')
    session['role'] = 'helpdesk'
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()
    cursor.execute("SELECT email, position FROM Helpdesk WHERE email = ?", (email,))
    user = cursor.fetchone()
    email = user[0]
    position = user[1]

    cursor.execute("SELECT * FROM Categories")
    categories = cursor.fetchall()

    if request.method == 'POST':
        new_request = request.form.get('new_request')
        if new_request != None:
            cursor.execute("UPDATE Requests SET helpdesk_staff_email = ?, request_status=0 WHERE request_id = ?",(email, new_request))
            conn.commit()
        completed_request = request.form.get('completed_request')
        if completed_request != None:
            cursor.execute("UPDATE Requests SET request_status = 1 WHERE request_id = ?", (completed_request,))
            conn.commit()
        new_category = request.form.get('new_category')
        parent_category = request.form.get('parent_category')
        if new_category != None and parent_category != None:
            cursor.execute("INSERT INTO Categories (parent_category, category_name) VALUES (?,?)", (parent_category, new_category))
            conn.commit()

    cursor.execute("SELECT * FROM Requests WHERE helpdesk_staff_email = ? AND request_status = 1", (email,))
    complete_requests = cursor.fetchall()

    cursor.execute("SELECT * FROM Requests WHERE helpdesk_staff_email = ? AND request_status = 0", (email,))
    active_requests = cursor.fetchall()

    cursor.execute("SELECT * FROM Requests WHERE helpdesk_staff_email = 'helpdeskteam@lsu.edu'")
    new_requests = cursor.fetchall()

    session['webpage'] = 'helpdesk'
    conn.close()
    return render_template('helpdesk.html', email=email, position=position, active_requests=active_requests, new_requests=new_requests, complete_requests=complete_requests, categories=categories)

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

    product_images = {
        "Sephora Rouge Gel Lip Liner": "https://www.sephora.com/productimages/sku/s2871036-main-zoom.jpg?imwidth=1224",
        'Wilson Basketball 9"': "https://dks.scene7.com/is/image/GolfGalaxy/25WILUNCRHYTHMBSKBKB_Brown?qlt=70&wid=1100&hei=1100&fmt=webp&op_sharpen=1&fit=constrain",
        "Mainstays Linen Bathrobe": "https://www.roughlinen.com/cdn/shop/products/LINENROBEZION_1_2000x.jpg?v=1767661845",
        "Mainstays Satin Bathrobe": "https://i5.walmartimages.com/seo/Ekouaer-Women-s-Satin-Robe-Valentines-Lingerie-for-Women-Kimono-Bathrobe-3-4-Sleeve-Ruffle-Belted-Robes-Bridesmaids-Champagne-Color-S_7dfc780b-eb9b-4c95-8076-4390d682dfab.c8e69b046cf6305c9375199d3b976a57.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "Mainstays Waffled Bathrobe": "https://m.media-amazon.com/images/I/71QaiOluK0L._AC_SY879_.jpg",
        "Rare Beauty Liquid Touch Brush": "https://www.sephora.com/productimages/sku/s2362408-main-zoom.jpg?imwidth=1224",
        "Lotus SuperProtector Sunscreen": "https://www.lotus.in/cdn/shop/products/SPF70_Frontcopy2.jpg?v=1688806548&width=1400",
        "Loreal Foundation Supreme": "https://i5.walmartimages.com/seo/L-Oreal-Paris-Infallible-Pro-Matte-Blendable-Foundation-Oil-Free-102-Shell-Beige-1-fl-oz_9e3287a3-a6a5-46e7-8aae-31ba52894b37.9e73b3f20229de094885f486a72ed193.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "Ribeye": "https://assets2.kansascitysteaks.com/dyn-images/pdp_hero/1080_USDA_Prime_Bone-20d33f5d7c7b2dbaf946f3dd90995133.jpg",
        "Steak Rolls": "https://www.daringgourmet.com/wp-content/uploads/2014/05/Steak-Rolls-4.jpg",
        "Wilde Black Ribbed Long Sleeve Mock Neck Bodysuit": "https://images.express.com/is/image/expressfashion/0086_09610902_0058_a001?cache=on&wid=480&fmt=jpeg&qlt=85,1&resmode=sharp2&op_usm=1,1,5,0&defaultImage=Photo-Coming-Soon",
        "MM OC Dry Cat Food": "https://i5.walmartimages.com/seo/Meow-Mix-Original-Choice-Dry-Cat-Food-3-15-Pound-Bag_4f4e12bb-b3e9-482f-ab11-f04108998b23.7f813b8f3f6522b8fa01037cbce91784.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "13 Pro Max": "https://m.media-amazon.com/images/I/61ERgud-SbL._AC_SX679_.jpg",
        "S22": "https://m.media-amazon.com/images/I/81OIgOznJIL._AC_SX679_.jpg",
        "S23": "https://m.media-amazon.com/images/I/61yUiD1CVML._AC_SX679_.jpg",
        "Selby Mini Skirt": "https://us.princesspolly.com/cdn/shop/products/2-modelinfo-izy-US2_15368558-1402-4446-a5cf-da68af27576e.jpg?v=1679633327&width=1800",
        "Skeleton Hand Print Oversized tee": "https://di2ponv0v5otw.cloudfront.net/posts/2025/08/02/688e4a0a9b2158f1ba0d9302/l_688e4a1388849a732a874c9f.jpg",
        "Ankle-length Leather Pants": "https://m.media-amazon.com/images/I/51r96OlCtlL._AC_SY879_.jpg",
        "H&M Jersey Top": "https://image.hm.com/assets/hm/ee/05/ee0549d1fcba079ae1939e52dfd4023135ac4074.jpg?imwidth=2160",
        "Skinny High Jeans": "https://lscoglobal.scene7.com/is/image/lscoglobal/WB_18882-0594_GLO_CM_D1?fmt=webp&qlt=70&resMode=sharp2&fit=crop,1&op_usm=0.6,0.6,8&wid=309&hei=309",
        "Mac Nut Cookies": "https://sallysbakingaddiction.com/wp-content/uploads/2012/09/white-chocolate-macadamia-nut-cookies-1.jpg",
        "Mr.Mixing bowl": "https://images.squarespace-cdn.com/content/v1/5f63ff3dce6e39523e4b6b80/a59cb1ae-9de6-46aa-8886-497a256273fe/8+Quart+Bowl+Right+Branded.png",
        "Double boiler insert_for_all": "https://m.media-amazon.com/images/I/51ouyTiwLfL._AC_SX679_.jpg",
        "BB TSP Wet Cat Food": "https://i5.walmartimages.com/seo/Blue-Buffalo-Tastefuls-Natural-Wet-Cat-Food-Adult-Chicken-Pat-5-5-oz-Can_e32eccbf-4d76-4d35-bd1e-321fd966155e.9c5188ab155574bf701cdbeee182ec02.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "GW Electric Scooter": "https://i5.walmartimages.com/asr/942a38b1-5c2f-4cf8-bae6-2de1d2eaf661.e45f321513195d45bc0ae97faed7ff53.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "AW SE": "https://t-mobile.scene7.com/is/image/Tmusprod/Apple-Watch-SE-3-40mm-Midnight-Aluminum-Case-Midnight-Sport-Band-frontimage",
        "AW S6": "https://m.media-amazon.com/images/I/71uN94CB+jL._AC_SX679_.jpg",
        "AW S7": "https://m.media-amazon.com/images/I/61SJZzxSSAL._AC_SX679_.jpg",
        "AirPods pro": "https://m.media-amazon.com/images/I/71zny7BTRlL._AC_SX679_.jpg",
        "AirPods max": "https://m.media-amazon.com/images/I/71tOG91oC6L._AC_SX679_.jpg",
        "Samsung Tizen": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcT-dz4LEV_cC7fXuBtvMv3s7puPw2xC2tbySX2-ckOSz0qYh65qrNEk4-SeOil6uxVSFooHEfIY-tbx0nA32oE3ApH_RDtg-zhBKwLGJWI",
        "Insignia Fire": "https://m.media-amazon.com/images/I/41ZcMd+O1YL._AC_.jpg",
        "LG Nanocell": "https://www.lg.com/eastafrica/images/tvs/md07596252/D-02.jpg",
        "CB Punching Bag and Gloves": "https://i5.walmartimages.com/asr/e292a227-4837-47af-bed8-124880055b17.7c5c5a799f2f3d34f49b97fc4580dc63.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "Diced Ham": "https://www.gfsstore.com/wp-content/uploads/2022/10/199834-RAW-6-768x768.jpg",
        "Luden's Throat Drops": "https://www.cvs.com/bizcontent/merchandising/productimages/high_res/81483201062.jpg?im=Resize=(160,160),aspect=ignore",
        "Ikea WC - Haggeby White": "https://www.ikea.com/us/en/images/products/sektion-high-cabinet-with-shelves-2-doors-white-veddinge-white__0299204_pe508280_s5.jpg?f=xl",
        "Lily Plant": "https://mynortherngarden.com/wp-content/uploads/2021/04/orange-lily-in-pot.jpg",
        "KK BC Wooden Playhouse": "https://m.media-amazon.com/images/I/81nqefxL-xL._AC_SX679_.jpg",
        "Ikea WC - White": "https://www.ikea.com/us/en/images/products/sektion-high-cabinet-with-shelves-2-doors-white-vallstena-white__1172992_pe893679_s5.jpg?f=xl",
        "Black quartz Sink": "https://images.thdstatic.com/productImages/59ebbfb2-58fe-41cc-bc40-6f182bee388c/svn/black-karran-undermount-kitchen-sinks-qu-670-bl-e1_100.jpg",
        "White Apron Sink": "https://images.thdstatic.com/productImages/b5e03f27-624f-4464-bafb-5caae7e1178c/svn/white-kohler-farmhouse-kitchen-sinks-k-5827-0-64_100.jpg",
        "Top Mount Sink": "https://s3.img-b.com/image/private/t_base,c_lpad,f_auto,dpr_auto,w_70,h_70/product/kohler/kohler-k-5846-4-0-3980066.jpg",
        "KF with HS": "https://m.media-amazon.com/images/I/51+C7E4MjHL._AC_SX679_.jpg",
        "DCKF": "https://images.signaturehardware.com/i/signaturehdwr/455764-hurston-faucet-cp-front.jpg?w=1425&fmt=auto",
        "KF with Sensor": "https://s3.img-b.com/image/private/t_base,c_lpad,f_auto,dpr_auto,w_70,h_70/product/kraus/kraus-ktf-3104ch-578883.jpg",
        "Ikea WC - 2 doors": "https://www.ikea.com/us/en/images/products/sektion-wall-cabinet-with-2-doors-white-vallstena-white__1173078_pe893762_s5.jpg?f=xl",
        "Gap Jersey Top": "https://www.gap.com/webcontent/0061/462/510/cn61462510.jpg",
        "Snow Crab": "https://seabear.com/cdn/shop/files/SnowCrab1x1.webp?v=1762988194&width=800",
        "Deep Seat Cushion": "https://m.media-amazon.com/images/I/81sfkPgZ51L._AC_SX679_.jpg",
        "Tylenol Gel": "https://target.scene7.com/is/image/Target/GUEST_1cda7c4c-4d06-4f25-b8da-0efddf393c48?wid=750&qlt=80",
        "Chinese Lanterns": "https://www.paperlanternstore.com/cdn/shop/products/36TCL-RD-chinese-paper-lantern.jpg?v=1614219474",
        "Tuscany Ridge Conversation Set": "https://assets.wfcdn.com/im/412663/resize-h1200-p1-w1200%5Ecompr-r85/3823/382380651/Argyri+9+-+Person+Outdoor+Wicker+Patio+Conversation+Furniture+Set+with+Optional+Fire+Pit+Table-87292006-87054263.jpg",
        "BF SA Whey": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcRiImhW1yCz5inlk7yBkmkWMQJbM_XxXnmhu5t2k9gk59U-Ml3EHtZiEB7V5VU4TCpJZ4S-Y4Kee36wVdbQut8kh_0ZEO3taTuJgphE-cETIyraoEnwCw1qrm5OGcHTg98SM9xJY3U&usqp=CAc",
        "BB FC Dry Dog Food": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcTa2RlwFsjMKC_HIiaYOy4I8xjmxGUo9mfhVGMgcGiVCbPDLgllt2KKpJs-aF-xoXO83IhN8vaxJ3voPOxhVyBZrZtuYFzjXbMvfTQOeGxvUfNz-O9mMBId1rR8R7sIzjgaFkaq-ts&usqp=CAc",
        "Sweet Potato Pie": "https://i5.walmartimages.com/seo/Patti-LaBelle-8-inch-Sweet-Potato-Pie-21-oz-1-count_6aab41a4-16c9-4e6f-9ef1-284795c44f6b.3bb6a1eb01502d98858309c23c882a64.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "Horizon: FW": "https://m.media-amazon.com/images/I/81JulKoOyLL._SX522_.jpg",
        "MJ Mega El Toro": "https://m.media-amazon.com/images/I/917IGsFpltL._AC_SX679_.jpg",
        "ER: MMO": "https://m.media-amazon.com/images/I/71GPiuyNtkL._AC_CR0%2C0%2C0%2C0_SX960_SY720_.jpg",
        "SV ES Melatonin": "https://i5.walmartimages.com/seo/Spring-Valley-Extra-Strength-Melatonin-Tablets-Dietary-Supplement-Value-Size-10-mg-240-Count_192a6111-e5bc-4d6d-bce8-aea574f86f5d.5c142b8bc0135d8b5ebce8b836915607.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "GG Yoga Socks": "https://m.media-amazon.com/images/I/81RNX14aqkL._AC_SX679_.jpg",
    }

    return render_template("product_listings.html", categories=category_hierarchy, products=products, category_selected=category_selected, product_images=product_images)#sends the cat hierarchy, products in category selected and the category selected

@app.route('/listing/<int:Listing_ID>')
def product_detail(Listing_ID):
    conn = sqlite3.connect("NittanyAuctionDB")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Auction_Listings WHERE Listing_ID = ?", (Listing_ID,))
    listing = cursor.fetchone()

    cursor.execute("SELECT * FROM Bids WHERE Listing_ID = ? ORDER BY bid_price DESC", (Listing_ID,))
    bids = cursor.fetchall()

    current_bid = bids[0]['bid_price'] if bids else None

    cursor.execute("SELECT AVG(rating), COUNT(*) FROM Ratings WHERE Seller_Email = ?", (listing['Seller_Email'],))
    rating_row = cursor.fetchone()

    product_images = {
        "Sephora Rouge Gel Lip Liner": "https://www.sephora.com/productimages/sku/s2871036-main-zoom.jpg?imwidth=1224",
        'Wilson Basketball 9"': "https://dks.scene7.com/is/image/GolfGalaxy/25WILUNCRHYTHMBSKBKB_Brown?qlt=70&wid=1100&hei=1100&fmt=webp&op_sharpen=1&fit=constrain",
        "Mainstays Linen Bathrobe": "https://www.roughlinen.com/cdn/shop/products/LINENROBEZION_1_2000x.jpg?v=1767661845",
        "Mainstays Satin Bathrobe": "https://i5.walmartimages.com/seo/Ekouaer-Women-s-Satin-Robe-Valentines-Lingerie-for-Women-Kimono-Bathrobe-3-4-Sleeve-Ruffle-Belted-Robes-Bridesmaids-Champagne-Color-S_7dfc780b-eb9b-4c95-8076-4390d682dfab.c8e69b046cf6305c9375199d3b976a57.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "Mainstays Waffled Bathrobe": "https://m.media-amazon.com/images/I/71QaiOluK0L._AC_SY879_.jpg",
        "Rare Beauty Liquid Touch Brush": "https://www.sephora.com/productimages/sku/s2362408-main-zoom.jpg?imwidth=1224",
        "Lotus SuperProtector Sunscreen": "https://www.lotus.in/cdn/shop/products/SPF70_Frontcopy2.jpg?v=1688806548&width=1400",
        "Loreal Foundation Supreme": "https://i5.walmartimages.com/seo/L-Oreal-Paris-Infallible-Pro-Matte-Blendable-Foundation-Oil-Free-102-Shell-Beige-1-fl-oz_9e3287a3-a6a5-46e7-8aae-31ba52894b37.9e73b3f20229de094885f486a72ed193.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "Ribeye": "https://assets2.kansascitysteaks.com/dyn-images/pdp_hero/1080_USDA_Prime_Bone-20d33f5d7c7b2dbaf946f3dd90995133.jpg",
        "Steak Rolls": "https://www.daringgourmet.com/wp-content/uploads/2014/05/Steak-Rolls-4.jpg",
        "Wilde Black Ribbed Long Sleeve Mock Neck Bodysuit": "https://images.express.com/is/image/expressfashion/0086_09610902_0058_a001?cache=on&wid=480&fmt=jpeg&qlt=85,1&resmode=sharp2&op_usm=1,1,5,0&defaultImage=Photo-Coming-Soon",
        "MM OC Dry Cat Food": "https://i5.walmartimages.com/seo/Meow-Mix-Original-Choice-Dry-Cat-Food-3-15-Pound-Bag_4f4e12bb-b3e9-482f-ab11-f04108998b23.7f813b8f3f6522b8fa01037cbce91784.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "13 Pro Max": "https://m.media-amazon.com/images/I/61ERgud-SbL._AC_SX679_.jpg",
        "S22": "https://m.media-amazon.com/images/I/81OIgOznJIL._AC_SX679_.jpg",
        "S23": "https://m.media-amazon.com/images/I/61yUiD1CVML._AC_SX679_.jpg",
        "Selby Mini Skirt": "https://us.princesspolly.com/cdn/shop/products/2-modelinfo-izy-US2_15368558-1402-4446-a5cf-da68af27576e.jpg?v=1679633327&width=1800",
        "Skeleton Hand Print Oversized tee": "https://di2ponv0v5otw.cloudfront.net/posts/2025/08/02/688e4a0a9b2158f1ba0d9302/l_688e4a1388849a732a874c9f.jpg",
        "Ankle-length Leather Pants": "https://m.media-amazon.com/images/I/51r96OlCtlL._AC_SY879_.jpg",
        "H&M Jersey Top": "https://image.hm.com/assets/hm/ee/05/ee0549d1fcba079ae1939e52dfd4023135ac4074.jpg?imwidth=2160",
        "Skinny High Jeans": "https://lscoglobal.scene7.com/is/image/lscoglobal/WB_18882-0594_GLO_CM_D1?fmt=webp&qlt=70&resMode=sharp2&fit=crop,1&op_usm=0.6,0.6,8&wid=309&hei=309",
        "Mac Nut Cookies": "https://sallysbakingaddiction.com/wp-content/uploads/2012/09/white-chocolate-macadamia-nut-cookies-1.jpg",
        "Mr.Mixing bowl": "https://images.squarespace-cdn.com/content/v1/5f63ff3dce6e39523e4b6b80/a59cb1ae-9de6-46aa-8886-497a256273fe/8+Quart+Bowl+Right+Branded.png",
        "Double boiler insert_for_all": "https://m.media-amazon.com/images/I/51ouyTiwLfL._AC_SX679_.jpg",
        "BB TSP Wet Cat Food": "https://i5.walmartimages.com/seo/Blue-Buffalo-Tastefuls-Natural-Wet-Cat-Food-Adult-Chicken-Pat-5-5-oz-Can_e32eccbf-4d76-4d35-bd1e-321fd966155e.9c5188ab155574bf701cdbeee182ec02.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "GW Electric Scooter": "https://i5.walmartimages.com/asr/942a38b1-5c2f-4cf8-bae6-2de1d2eaf661.e45f321513195d45bc0ae97faed7ff53.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "AW SE": "https://t-mobile.scene7.com/is/image/Tmusprod/Apple-Watch-SE-3-40mm-Midnight-Aluminum-Case-Midnight-Sport-Band-frontimage",
        "AW S6": "https://m.media-amazon.com/images/I/71uN94CB+jL._AC_SX679_.jpg",
        "AW S7": "https://m.media-amazon.com/images/I/61SJZzxSSAL._AC_SX679_.jpg",
        "AirPods pro": "https://m.media-amazon.com/images/I/71zny7BTRlL._AC_SX679_.jpg",
        "AirPods max": "https://m.media-amazon.com/images/I/71tOG91oC6L._AC_SX679_.jpg",
        "Samsung Tizen": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcT-dz4LEV_cC7fXuBtvMv3s7puPw2xC2tbySX2-ckOSz0qYh65qrNEk4-SeOil6uxVSFooHEfIY-tbx0nA32oE3ApH_RDtg-zhBKwLGJWI",
        "Insignia Fire": "https://m.media-amazon.com/images/I/41ZcMd+O1YL._AC_.jpg",
        "LG Nanocell": "https://www.lg.com/eastafrica/images/tvs/md07596252/D-02.jpg",
        "CB Punching Bag and Gloves": "https://i5.walmartimages.com/asr/e292a227-4837-47af-bed8-124880055b17.7c5c5a799f2f3d34f49b97fc4580dc63.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "Diced Ham": "https://www.gfsstore.com/wp-content/uploads/2022/10/199834-RAW-6-768x768.jpg",
        "Luden's Throat Drops": "https://www.cvs.com/bizcontent/merchandising/productimages/high_res/81483201062.jpg?im=Resize=(160,160),aspect=ignore",
        "Ikea WC - Haggeby White": "https://www.ikea.com/us/en/images/products/sektion-high-cabinet-with-shelves-2-doors-white-veddinge-white__0299204_pe508280_s5.jpg?f=xl",
        "Lily Plant": "https://mynortherngarden.com/wp-content/uploads/2021/04/orange-lily-in-pot.jpg",
        "KK BC Wooden Playhouse": "https://m.media-amazon.com/images/I/81nqefxL-xL._AC_SX679_.jpg",
        "Ikea WC - White": "https://www.ikea.com/us/en/images/products/sektion-high-cabinet-with-shelves-2-doors-white-vallstena-white__1172992_pe893679_s5.jpg?f=xl",
        "Black quartz Sink": "https://images.thdstatic.com/productImages/59ebbfb2-58fe-41cc-bc40-6f182bee388c/svn/black-karran-undermount-kitchen-sinks-qu-670-bl-e1_100.jpg",
        "White Apron Sink": "https://images.thdstatic.com/productImages/b5e03f27-624f-4464-bafb-5caae7e1178c/svn/white-kohler-farmhouse-kitchen-sinks-k-5827-0-64_100.jpg",
        "Top Mount Sink": "https://s3.img-b.com/image/private/t_base,c_lpad,f_auto,dpr_auto,w_70,h_70/product/kohler/kohler-k-5846-4-0-3980066.jpg",
        "KF with HS": "https://m.media-amazon.com/images/I/51+C7E4MjHL._AC_SX679_.jpg",
        "DCKF": "https://images.signaturehardware.com/i/signaturehdwr/455764-hurston-faucet-cp-front.jpg?w=1425&fmt=auto",
        "KF with Sensor": "https://s3.img-b.com/image/private/t_base,c_lpad,f_auto,dpr_auto,w_70,h_70/product/kraus/kraus-ktf-3104ch-578883.jpg",
        "Ikea WC - 2 doors": "https://www.ikea.com/us/en/images/products/sektion-wall-cabinet-with-2-doors-white-vallstena-white__1173078_pe893762_s5.jpg?f=xl",
        "Gap Jersey Top": "https://www.gap.com/webcontent/0061/462/510/cn61462510.jpg",
        "Snow Crab": "https://seabear.com/cdn/shop/files/SnowCrab1x1.webp?v=1762988194&width=800",
        "Deep Seat Cushion": "https://m.media-amazon.com/images/I/81sfkPgZ51L._AC_SX679_.jpg",
        "Tylenol Gel": "https://target.scene7.com/is/image/Target/GUEST_1cda7c4c-4d06-4f25-b8da-0efddf393c48?wid=750&qlt=80",
        "Chinese Lanterns": "https://www.paperlanternstore.com/cdn/shop/products/36TCL-RD-chinese-paper-lantern.jpg?v=1614219474",
        "Tuscany Ridge Conversation Set": "https://assets.wfcdn.com/im/412663/resize-h1200-p1-w1200%5Ecompr-r85/3823/382380651/Argyri+9+-+Person+Outdoor+Wicker+Patio+Conversation+Furniture+Set+with+Optional+Fire+Pit+Table-87292006-87054263.jpg",
        "BF SA Whey": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcRiImhW1yCz5inlk7yBkmkWMQJbM_XxXnmhu5t2k9gk59U-Ml3EHtZiEB7V5VU4TCpJZ4S-Y4Kee36wVdbQut8kh_0ZEO3taTuJgphE-cETIyraoEnwCw1qrm5OGcHTg98SM9xJY3U&usqp=CAc",
        "BB FC Dry Dog Food": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcTa2RlwFsjMKC_HIiaYOy4I8xjmxGUo9mfhVGMgcGiVCbPDLgllt2KKpJs-aF-xoXO83IhN8vaxJ3voPOxhVyBZrZtuYFzjXbMvfTQOeGxvUfNz-O9mMBId1rR8R7sIzjgaFkaq-ts&usqp=CAc",
        "Sweet Potato Pie": "https://i5.walmartimages.com/seo/Patti-LaBelle-8-inch-Sweet-Potato-Pie-21-oz-1-count_6aab41a4-16c9-4e6f-9ef1-284795c44f6b.3bb6a1eb01502d98858309c23c882a64.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "Horizon: FW": "https://m.media-amazon.com/images/I/81JulKoOyLL._SX522_.jpg",
        "MJ Mega El Toro": "https://m.media-amazon.com/images/I/917IGsFpltL._AC_SX679_.jpg",
        "ER: MMO": "https://m.media-amazon.com/images/I/71GPiuyNtkL._AC_CR0%2C0%2C0%2C0_SX960_SY720_.jpg",
        "SV ES Melatonin": "https://i5.walmartimages.com/seo/Spring-Valley-Extra-Strength-Melatonin-Tablets-Dietary-Supplement-Value-Size-10-mg-240-Count_192a6111-e5bc-4d6d-bce8-aea574f86f5d.5c142b8bc0135d8b5ebce8b836915607.jpeg?odnHeight=573&odnWidth=573&odnBg=FFFFFF",
        "GG Yoga Socks": "https://m.media-amazon.com/images/I/81RNX14aqkL._AC_SX679_.jpg",
    }

    image_url = product_images.get(listing['Product_Name'], None)

    conn.close()
    return render_template('product_detail.html', listing=listing, bids=bids, current_bid=current_bid, seller_rating=rating_row[0], rating_count=rating_row[1], image_url=image_url, error=None, success=None)


if __name__ == '__main__':
    app.run()