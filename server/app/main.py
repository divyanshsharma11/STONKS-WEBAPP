from flask import Flask, json
from lxml import html
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return("Beel STOCKS API")


@app.route("/getmarket/<stock_name>")
def getMarket(stock_name="none"):
    url = f"https://in.finance.yahoo.com/quote/{stock_name}?p={stock_name}"
    resp = requests.get(url)
    tree = html.fromstring(resp.content)
    result = tree.xpath(
        '//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')
    stock_name = tree.xpath(
        '//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1')
    stock_price = {"stock_name": stock_name[0].text,
                   "marketprice": result[0].text}
    realtime = json.dumps(stock_price, sort_keys=False)
    return(realtime)


@app.route("/getdata/<stock_name>")
def getData(stock_name="none"):
    url = f"https://in.finance.yahoo.com/quote/{stock_name}?p={stock_name}"
    print(url)
    resp = requests.get(url)
    tree = html.fromstring(resp.content)

    stock_name = tree.xpath(
        '//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1')
    previous_close = tree.xpath(
        '//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span')
    open_price = tree.xpath(
        '//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]/span')
    Bid = tree.xpath(
        '//*[@id="quote-summary"]/div[1]/table/tbody/tr[3]/td[2]')

    if(Bid[0].text == None):
        Bid = tree.xpath(
            '//*[@id="quote-summary"]/div[1]/table/tbody/tr[3]/td[2]/span')

    Ask = tree.xpath(
        '//*[@id="quote-summary"]/div[1]/table/tbody/tr[4]/td[2]')

    if(Ask[0].text == None):
        Ask = tree.xpath(
            '//*[@id="quote-summary"]/div[1]/table/tbody/tr[4]/td[2]/span')

    Days_range = tree.xpath(
        '//*[@id="quote-summary"]/div[1]/table/tbody/tr[5]/td[2]')
    _week52range = tree.xpath(
        '//*[@id="quote-summary"]/div[1]/table/tbody/tr[6]/td[2]')
    volume = tree.xpath(
        '//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/span')
    avg_volume = tree.xpath(
        '//*[@id="quote-summary"]/div[1]/table/tbody/tr[8]/td[2]/span')

    stock_data = {"Stock_name": stock_name[0].text,
                  "Previous_close": previous_close[0].text,
                  "Open_price": open_price[0].text,
                  "Bid": Bid[0].text,
                  "Ask": Ask[0].text,
                  "Days-range": Days_range[0].text,
                  "52_weeks_range": _week52range[0].text,
                  "Volume": volume[0].text,
                  "Avg_volume": avg_volume[0].text,
                  }
    result = json.dumps(stock_data, sort_keys=False)
    return(result)
