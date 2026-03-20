from flask import Flask, render_template, request, session
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
    data = pd.read_csv('C:/Users/mhbth/Downloads/NittanyAuctionDataset_v1/NittanyAuctionDataset_v1/Users.csv',
                       names=columns)
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
    data = pd.read_csv('C:/Users/mhbth/Downloads/NittanyAuctionDataset_v1/NittanyAuctionDataset_v1/Bidders.csv',
                       names=columns)
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
    data = pd.read_csv('C:/Users/mhbth/Downloads/NittanyAuctionDataset_v1/NittanyAuctionDataset_v1/Sellers.csv',
                       names=columns)
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
    data = pd.read_csv('C:/Users/mhbth/Downloads/NittanyAuctionDataset_v1/NittanyAuctionDataset_v1/Local_Vendors.csv',
                       names=columns)
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
    data = pd.read_csv('C:/Users/mhbth/Downloads/NittanyAuctionDataset_v1/NittanyAuctionDataset_v1/Helpdesk.csv',
                       names=columns)
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
    return render_template('Main_webpage.html')

@app.route('/login.html', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        # firstname is the email of the user
        firstname = request.form['FirstName']
        result = add_name(firstname, request.form['LastName'])

        # login success
        if result:
            user_type = getUserType(firstname)
            session['user'] = firstname
            session['type'] = user_type
            return render_template('checkingInfo.html', error=error, result=result)
        else:
            return render_template('fail.html', error=error, result=result)
    return render_template('login.html', error=error)

def add_name(email, password):
    # hash the password using MD5
    password = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE email='" +
                   email+"' AND password='"+password+"'")
    result = cursor.fetchall()
    if result:
        return 1
    else:
        return 0

def getInfo(email):
    ''' return:
        email ID,
        name,
        age,
        gender,
        home and billing address (street, city, state, zipcode),
        last 4 digits of credit cards
        of a buyer/seller(buyer)'''
    # connect to database
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bidders WHERE email='"+email+"'")

    # result=[(email, first_name, last_name, gender, age, home_address, billing_address, last_4_digits_of_credit_cards)]
    result = []

    # temp is the element in the result
    # right now temp is in list type, and it will be changed to tuple type later
    temp = []

    # buyer_result=[(email, first_name, last_name, gender, age, home_address_id, billing_address_id)]
    buyer_result = cursor.fetchall()

    # adding email, first_name, last_name, age (first 5 elements) to temp
    for element in buyer_result[0][:5]:
        temp.append(element)

    result = [tuple(temp)]

    return result

def getUserType(email):
    '''Returns the user type (buyer, seller(buyer), local_vendor) based on the given email'''

    # at first we assume the user type is buyer
    user_type = "buyer"

    # connect to the database
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    # determine whether it is a local vendor
    cursor.execute("SELECT * FROM Local_Vendors WHERE email='"+email+"'")
    result = cursor.fetchall()
    if result:
        user_type = "local_vendor"
    else:
        # not a local vendor, but seller(buyer) still possible
        cursor.execute("SELECT * FROM Sellers WHERE email='"+email+"'")
        result = cursor.fetchall()
        if result:
            user_type = "seller(buyer)"
        else:
            cursor.execute("SELECT * FROM Helpdesk WHERE email='"+email+"'")
            result = cursor.fetchall()
            if result:
                user_type = "helpdesk"
    return user_type

def getSellerInfo(email, user_type):
    '''Returns the information of a seller(buyer) or a local vender'''

    # connect to the database
    conn = sqlite3.connect("NittanyAuctionDB")
    cursor = conn.cursor()

    # seller(buyer) and local vender both have information about routing number, account number, and balance
    cursor.execute(
        "SELECT * FROM Sellers WHERE email='"+email+"'")
    result = cursor.fetchall()

    # if the user is a local vendor, there are some other information (business name, business address, customer service number)
    if user_type == 'local_vendor':
        cursor.execute('''  SELECT business_name, business_address_id, customer_service_phone_number
                            FROM Local_Vendors
                            WHERE email="'''+email+'"')
        local_vendor_info = cursor.fetchall()
        result = [result[0]+local_vendor_info[0]]

    return result

if __name__ == '__main__':
    app.run()
