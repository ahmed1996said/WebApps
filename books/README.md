# :closed_book: Overview

Stocks is a stock trading web application that uses real-time stock data for purchasing and selling stocks. This is a simulator, so no real money is used.Every new user is given $10,000 :dollar: to begin with (of virtual, not real money-sorry!).


## Development

To develop this application, I wrote code in HTML, CSS, and JS for client end and Python (using Flask micro framework) for server end controller and a remote PostgreSQL database from Heroku.

### Key words
HTML, CSS, Javascript,Bootstrap, Python, Jinja , Flask, APIs, SQL, PostgreSQL, sessions


## Screenshots

![login]Once an account is created, we may log in:
(screenshots/login.png?raw=true "login")


This is the main page, you can search any books by author, title or ISBN number, let's look for a book about "Steve Jobs":

![Main Page](screenshots/index.png?raw=true "main page")


The result:

![Results](screenshots/results.png?raw=true "Quoted")


Clicking on the book, we see the book profile including reviews, ratings, book cover and other information:

![Book](screenshots/reveiwing.png?raw=true "Buy")


We can post the review and see it appended to the reviews. Users may only review once, so the review form is no longer available now:

![Reviewied](screenshots/reviewed.png?raw=true "Summary")


Let's take a look at another book that may be a little less popular, with no reviews:

![AnotherBook](screenshots/noreview.png?raw=true "Sell")






