import urllib.request as urllib
from bs4 import BeautifulSoup
import csv
import os
import time


field_order = ['date', 'last_trade', 'change', 'ah_price', 'ah_change']
fields = {'date': 'Date',
        'last_trade': 'Last Trade',
        'change': 'Change',
        'ah_price': 'After Hours Price',
        'ah_change': 'After Hours Change'}


def find_quote_section(html):
    soup = BeautifulSoup(html, "html.parser")
    quote = soup.find('div', attrs={'id': 'quote-header-info'})
    return quote


def get_stock_html(ticker_name):
    opener = urllib.build_opener(
        urllib.HTTPRedirectHandler(),
        urllib.HTTPHandler(debuglevel=0),
    )
  
    opener.addheaders = [
        ('User-agent',
        "Mozilla/4.0 (compatible; MSIE 7.0; "
        "Windows NT 5.1; .NET CLR 2.0.50727; "
        ".NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)")
    ]

    url = "http://finance.yahoo.com/q?s=" + ticker_name
    response = opener.open(url)
    return b''.join(response.readlines())

    
def parse_stock_html(html, ticker_name):
    quote = find_quote_section(html)
    result = {}
    tick = ticker_name.lower()
    
    # <h1>Alphabet Inc. (GOOG)</h1>
    result['stock_name'] = quote.find('h1').contents[0]
    
    #After hours values
    result['ah_price'] = quote.find(attrs={'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).contents[0]
    
    #Change in value
    result['ah_change'] = quote.find(attrs={'class': 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($dataGreen)'}).contents[0]
    
    return result
    
def write_row(ticker_name, stock_values):
    file_name = "stocktracker-" + ticker_name + ".csv"
    if os.access(file_name, os.F_OK):
        file_mode = 'ab'
    else:
        file_mode = 'wb'
        
    csv_writer = csv.DictWriter(
        open(file_name, file_mode),
        fieldnames=field_order,
        restval='',
        extrasaction='ignore')
        
    if file_mode == 'wb':
        csv_writer.writeheader()
    csv_writer.writerow(stock_values)
    

if __name__ == '__main__':
    html = get_stock_html('GOOG')
    stock = parse_stock_html(html, 'GOOG')
    stock['date'] = time.strftime("%Y-%m-%d %H:%M")
    write_row('GOOG', stock)
    print(stock)