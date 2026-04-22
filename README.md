# CMPSC 431W – NittanyAuction Final Project (Phase 2)

This project is a full implementation of the **NittanyAuction** system developed for CMPSC 431W. The application is a Flask-based online auction platform that allows users to register, log in, create listings, place bids, complete payments, manage accounts, and access helpdesk support.

## What the System Does

### User Management
- Allows new users to register accounts
- Supports multiple roles:
  - Bidder
  - Seller
  - Local Vendor
  - Helpdesk Staff
- Stores user credentials securely with hashed passwords
- Provides login/logout functionality

### Auction Features
- Sellers can create auction listings
- Sellers can edit or delete their listings
- Listings include product details, category, reserve price, bid limits, and optional image links
- Users can browse available listings
- Users can view detailed product pages

### Bidding System
- Bidders can place bids on active listings
- Tracks highest bid
- Enforces bid limits and reserve prices
- Automatically determines auction winners when bidding ends
- Sends winning users to payment flow

### Payment System
- Winning bidders can complete payment
- Transactions are recorded
- Sold listings are removed from active auctions

### Ratings & Reviews
- Buyers can rate sellers after completed purchases
- Seller ratings are displayed on listing pages

### Helpdesk Features
- Users can submit support requests
- Helpdesk staff can view and manage requests

## Database Features

The system uses **SQLite** (`NittanyAuctionDB`) and includes tables such as:

- Users
- Bidders
- Sellers
- Local_Vendors
- Helpdesk
- Auction_Listings
- Bids
- Transactions
- Ratings
- Requests
- Categories
- Credit_Cards
- Address
- Zipcode_Info

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- Bootstrap
- Jinja2 Templates
- Pandas

## Project Files / Folders

- `app.py` – Main Flask application
- `templates/` – HTML pages for all user interfaces
- `data/` – CSV files used for database setup
- `static/` – Optional images / CSS / assets
- `README.md` – Project documentation

## How to Run

1. Install required packages:

```bash
pip install flask pandas
```

2. Make sure the project folder contains:
- `app.py`
- `templates/`
- `data/`

3. Run the application:
```bash
python app.py
```

4. Open the local server URL shown in the terminal (usually `http://127.0.0.1:5000`).

## Notes
SQLite database file will be created automatically if it does not already exist.
CSV files are used to initialize database tables.
Some features depend on having sample data loaded.
