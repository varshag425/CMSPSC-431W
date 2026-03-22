# CMPSC 431W - NittanyAuction Progress Check
---
This is a partial implementation of the NittanyAuction system developed for the progress check. At this stage, we have created a simple Flask-based login prototype for the NittanyAuction system. It loads user data from CSV files into a SQLite database and allows a user to log in as a bidder, seller, or helpdesk staff member.

## What it does

- creates the SQLite database `NittanyAuctionDB`
- creates and populates these tables from CSV files:
  - `Users`
  - `Bidders`
  - `Sellers`
  - `Local_Vendors`
  - `Helpdesk`
- hashes user passwords using SHA-256 before storing them
- provides a login page where the user enters:
  - email
  - password
  - role button clicked
- checks whether the login is valid
- redirects to:
  - bidder page
  - seller page
  - helpdesk page
- shows an error message if the login fails

## Files / folders

- `app.py` – main Flask application
- `templates/` – HTML pages
	- `index.html`
	- `login.html`
	- `bidder.html`
	- `seller.html`
	- `helpdesk.html`
- `data/` – CSV files used to populate the database
	- `Address.csv`
	- `Auction_Listings.csv`
	- `Bidders.csv`
	- `Bids.csv`
	- `Categories.csv`
	- `Credit_Cards.csv`
	- `Helpdesk.csv`
	- `Local_Vendors.csv`
	- `Ratings.csv`
	- `Requests.csv`
	- `Sellers.csv`
	- `Transactions.csv`
	- `Users.csv`
	- `Zipcode_Info.csv`

## How to run

1. Install the required packages on your command line tool if needed:
   pip install flask pandas
2. Make sure the following files/folders are in the same directory:
	- app.py
	- data/
	- templates/
3. run: python app.py
