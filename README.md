# Overview

Stocks is a stock trading web application that uses real-time stock data for purchasing and selling stocks. This is a simulator, so no real money is used.Every new user is given $10,000 :dollar: to begin with (of virtual, not real money-sorry!).


## Development

To develop this application, I wrote code in HTML, CSS, and JS for client end and Python (using Flask micro framework) for server end controller and a SQLite database stored locally. Additionally, the web applications uses [IEX API](https://iexcloud.io/) to receive real time stock prices.

## Getting Started

To run this Web App, make sure you have [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [SQlite](https://www.sqlite.org/index.html) installed and register for [IEXCloud](https://iexcloud.io/) to receive an API key. Once this is done run the following commands in the stock directory:
```
export API_KEY = <user API key from IEXCloud>
export FLASK_APP = application.py
run flask
```

## Screenshots
You may first want to create an account
![Sign up](stocks/screenshots/register.png?raw=true "signup")

Or, if you already have one, you may log in
![Login](stocks/screenshots/login.png?raw=true "login")

This is your main dashboard. As you can see, you are initially given a balance of $10,000
![Dashboard](stocks/screenshots/index.png?raw=true "Dashboard")

You can get a quote of a stock by typing in the stock symbol
![Quote](stocks/screenshots/quote.png?raw=true "Quote")

The result:
![Quoted](stocks/screenshots/quoted.png?raw=true "Quoted")

Let's say you want to buy 4 Netflix (NFLX) stocks:
![Buy](stocks/screenshots/buy.png?raw=true "Buy")

After purchasing 4 Netflix stocks, 5 Google Stocks and 2 Microsoft Stocks our dashboard now looks like this :money_with_wings::
![Summary](stocks/screenshots/summary.png?raw=true "Summary")

You know what.. let's sell the Microsoft stocks. It was an impulse decision:grimacing: :
![Sell](stocks/screenshots/sell.png?raw=true "Sell")

Now, lets look at the history page, it shows all of our transactions:
![History](stocks/screenshots/history.png?raw=true "history")


Awesome- now you're a professional in stock trading! :laughing:




