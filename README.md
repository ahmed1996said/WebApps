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





