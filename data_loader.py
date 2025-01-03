import yfinance as yf

def fetch_stock_data(symbol, period='1y'):
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    data.columns = [col if isinstance(col, str) else col[0] for col in data.columns]
    return data

