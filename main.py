STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
api_key =  "x"
news_key = "x"
sid = 'x'
token = 'x'
import requests
from datetime import datetime as dt
from datetime import timedelta as td
from twilio.rest import Client


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

today = dt.now()
delta = td(days=-1)
yday = today+delta
yday.strftime('%Y-%m-%d')
yday = str(yday)[:10]
day_b4 = today + delta*2
day_b4.strftime('%Y-%m-%d')
day_b4 = str(day_b4)[:10]
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey={api_key}'
response = requests.get(url)
response.raise_for_status()
stock_data = response.json()
price_day_b4_close = float(stock_data["Time Series (Daily)"][day_b4]["4. close"])
del stock_data["Time Series (Daily)"][yday]["5. volume"]
yday_data = stock_data["Time Series (Daily)"][yday]
price_yday_high = float(stock_data["Time Series (Daily)"][yday]["2. high"])
get_news = False
if abs((price_yday_high - price_day_b4_close))/(price_day_b4_close) >= 0.05:
    get_news = True
    
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

news_url = f"https://newsapi.org/v2/everything?q=tesla&from=2022-08-16&sortBy=publishedAt&apiKey={news_key}"
news_response = requests.get(news_url)
news_response.raise_for_status()
news_data = news_response.json()

if get_news:

    news_piece1 = news_data["articles"][0]
    news_piece2 = news_data["articles"][1]
    news_piece3 = news_data["articles"][2]
    news_piece =[news_piece1, news_piece2, news_piece3]

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
    
    def send_msg():
        price_change = (price_yday_high - price_day_b4_close)/(price_day_b4_close)
        if price_change < 0:
            stock_change = f'🔻{price_change*100:.4f}%'
        else:
            stock_change = f'🔺{price_change*100:.4f}%'
        client = Client(sid, token)
        message = client.messages \
                        .create(
                            body=f"\nTSLA: {stock_change} ",
                            from_='+15076153535',
                            to='+61412715347'
                        )
        print(message.status)
   
        for news in news_piece:
            client = Client(sid, token)
            message = client.messages \
                            .create(
                                body=f"\nHeadline: {news['title']}\n\nBrief: {news['description']} ",
                                from_='+15076153535',
                                to='+61412715347'
                            )
            print(message.status)
    send_msg()
#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

