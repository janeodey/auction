# Auction

Auction is an eBay-like e-commerce auction site that allow users to post auction items (listings), place bids on listings,
comment on those listings, and add listings to a “watchlist.” It was built using Python (Django), HTML, CSS.

### Project Description

The homepage shows all listings that are active. Clicking on any listing will show more deatils for that listing such as the current bid
and active status. A signed in user also has the ability to add a listing of interest to his watchlist, post a new listing for auction
and comment on existing listings. Whenever a listing is closed, the highest bidder becomes winner and is notified.

[views.py](/auctions/views.py) defines the functions for all of the routes. The folder, [templates](/auctions/templates/auctions), holds the front-end HTML
files. [db.sqlite3](/db.sqlite3) is a SQLite database that was used for the project.

A video of this application's demonstration is at https://youtu.be/MJZTLgjItCo


