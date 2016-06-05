import pandas as pd
import time
import datetime

def get_historical_gdp():
    df = pd.read_csv(r'../../data/GDP.csv')
    date = df['DATE']
    new_date = []
    for element in date:
        new_date.append(datetime.datetime.strptime(element, '%Y-%m-%d'))
    date = new_date
    value = df['VALUE']
    return date, value

def get_historical_quotes(start_date=datetime.datetime(1990,1,2),end_date=datetime.datetime(2016,1,1)):
    df = pd.read_csv('../data/usdgbp1990.csv')
    date = df['DATE'].values
    value = df['VALUE'].values
    # print(type(date))
    new_date = []
    for element in date:
        new_date.append(datetime.datetime.strptime(element, '%Y-%m-%d'))
    date = new_date
    # print(len(value))
    start_cut = date.index(start_date)
    end_cut = date.index(end_date)
    date = date[start_cut:end_cut]
    value = value[start_cut:end_cut]
    # print(len(date),value)
    return date, value

# date, x = get_historical_quotes(start_date=datetime.datetime(1995, 1, 2), end_date=datetime.datetime(2009, 1, 2))