from datetime import datetime
from pandas_datareader import DataReader
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib
matplotlib.use('Agg')


def graphPlot(username, stock_name):
    tech_list = ['GOOG']
    end = datetime.now()
    start = datetime(end.year, end.month-1, end.day-1)
    for stock in tech_list:
        globals()[stock] = DataReader(stock_name, 'yahoo', start, end)

    plt.plot(GOOG['Open'])
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('1 month stocks open graph')
    fig1 = plt.gcf()
    plt.draw()
    fig1.savefig(f'./app/static/{username}/{stock_name}.png', dpi=600)
    plt.clf()
