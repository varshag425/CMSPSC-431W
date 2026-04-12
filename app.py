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
    columns = ['email', 'password']
    data = pd.read_csv('/data/Users.csv',
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
    data = pd.read_csv('/data/Bidders.csv',
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
    columns = ['email', 'bank_routing_number', 'bank_account_number', 'balance']
    data = pd.read_csv('/data/Sellers.csv',
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
    data = pd.read_csv('/data/Local_Vendors.csv',
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
    columns = ['email', 'position']
    data = pd.read_csv('/data/Helpdesk.csv',
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
    columns = ['seller_email', 'listing_ID', 'category', 'auction_title', 'product_name', 'product_description', 'quantity', 'reserve_price', 'max_bids', 'status']
    data = pd.read_csv('/data/Auction_Listings.csv', names=columns, header=0)
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
    columns = ['bid_ID', 'seller_email', 'listing_ID', 'bidder_email', 'bid_price']
    data = pd.read_csv('/data/Bids.csv', names=columns, header=0)
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
    columns = ['address_ID', 'zipcode', 'street_number', 'street_name']
    data = pd.read_csv('/data/Address.csv', names=columns, header=0)
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
    columns = ['parent_category', 'category_name']
    data = pd.read_csv('/data/Categories.csv', names=columns, header=0)
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
    columns = ['credit_card_num', 'card_type', 'expire_month', 'expire_year', 'security_code', 'owner_email']
    data = pd.read_csv('/data/Credit_Cards.csv', names=columns, header=0)
    col1 = data['credit_card_num'].values
    col2 = data['card_type'].values
    col3 = data['expire_month'].values
    col4 = data['expire_year'].values
    col5 = data['security_code'].values
    col6 = data['owner_email'].values

    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Credit_Cards(credit_card_num VARCHAR(20), card_type VARCHAR(50), expire_month INTEGER, expire_year INTEGER, security_code INTEGER, owner_email VARCHAR(50), PRIMARY KEY (credit_card_num), FOREIGN KEY (owner_email) REFERENCES Users(email))')

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
    columns = ['bidder_email', 'seller_email', 'date', 'rating', 'rating_description']
    data = pd.read_csv('/data/Ratings.csv', names=columns, header=0)
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
    columns = ['request_ID', 'sender_email', 'helpdesk_staff_email', 'request_type', 'request_description', 'request_status']
    data = pd.read_csv('/data/Requests.csv', names=columns, header=0)
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
    columns = ['transaction_ID', 'seller_email', 'listing_ID', 'bidder_email', 'date', 'payment']
    data = pd.read_csv('/data/Transactions.csv', names=columns, header=0)
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
    columns = ['zipcode', 'city', 'state']
    data = pd.read_csv('/data/Zipcode_Info.csv', names=columns, header=0)
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

@app.route('/registration.html', methods=['POST', 'GET'])
def user_registration():
    error = None
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
            cursor.execute("INSERT INTO Users(email, password) VALUES (?,?)", (user_email, hashed_password,))
            if user_role == "buyer":
                cursor.execute("INSERT INTO Bidders(email, first_name, last_name, age, home_address_id, major) VALUES (?, NULL, NULL, NULL, NULL, NULL)", (user_email,))
            elif user_role == "seller":
                cursor.execute("INSERT INTO Sellers(email, bank_routing_number, bank_account_number, balance) VALUES (?, NULL, NULL, NULL)", (user_email,))
            elif user_role == "helpdesk":
                cursor.execute("INSERT INTO Helpdesk(email, position) VALUES (?, NULL)", (user_email,))
            else:
                error = "User role not recognized! Select one of the user roles displayed"
            conn.commit()
            return redirect(url_for('login'))
    return render_template('/registration.html', error=error)
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
