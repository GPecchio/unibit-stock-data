# retrieve stock prices using UniBit APIs and use them to analyse stock and predict them 
# (it's a simple method that probably won't predict the fiture correctly)
import requests

initial_amount = 1000.0
account_value = initial_amount
profit_loss = 0.0

API_key = 'VcXdxijTKEx5U11IzmuWSkkwUAWwY608'

def getStockInfo(ticker):
    '''
    Given a ticker represting a stock, get its info thorugh the realtime API 
    and create a new stock instance with the data retrieved
    '''
    # create a request, retrieve the JSON from the API and set it equal to request
    request = requests.get('https://api.unibit.ai/realtimestock/'+ ticker + '?AccessKey=' + API_key)
    request = request.json()
    # retrieve only the opening and latest quotes for the stock
    opening = request[len(request)-1]
    latest = request[0]
    # check if day ended in a gain or loss
    positive_day = False
    if round(latest['price'] - opening['price'], 2) > 0.0: 
        positive_day = True
    # create a new stock instance with info needed
    stock = {
        'ticker': ticker,
        'latest' : latest['price'],
        'open': opening['price'],
        'daily_profit_loss': round(latest['price'] - opening['price'], 2),
        'positive_day': positive_day
    }
    return stock

def lastNDays(ticker):
    '''
    Given a ticker represting a stock, range is 1 month and interval is 1 day, 
    get its info thorugh the realtime API and create a new stock instance with the data retrieved
    '''
    # create a request, retrieve the JSON from the API and set it equal to request
    request = requests.get('https://api.unibit.ai/historicalstockprice/'+ ticker + '?range=1m&interval=1&AccessKey=' + API_key)
    request = request.json()
    # create a list to store every day
    data = []
    # add each day data to the overall list
    day_number = 0
    # for every day, save it in a new stock instance and add it to the overall list
    for day in request:
        day_number = day_number + 1
        # check if day ended in a gain or loss
        positive_day = False
        print day
        if round(day['close'] - day['open'], 2) > 0.0: 
            positive_day = True
        new_day = {
            'day': day_number,
            'ticker': ticker,
            'close' : day['close'],
            'open': day['open'],
            'daily_profit_loss': round(day['close'] - day['open'], 2),
            'positive_day': positive_day
        }
        data.append(new_day)
    # calculate profit and loss and the percentage gained or lost
    profit_loss = round(data[0]['close'] - data[len(data)-1]['close'], 2)
    percentage_profit_loss = round((profit_loss / data[0]['close']) * 100, 2)
    
    return data, profit_loss, percentage_profit_loss

# TESTS

print '========= Apple - AAPL ========='
print getStockInfo('AAPL')
print lastNDays('AAPL')

print '========= Clovis - CLVS ========='
print getStockInfo('CLVS')
print lastNDays('CLVS')

print '========= Twilio - TWLO ========='
print getStockInfo('TWLO')
#print lastNDays('TWLO')