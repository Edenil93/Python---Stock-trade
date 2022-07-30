import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "WJ1SYYF4XMVM7F67"
NEWS_API_KEY = "30f5bcbe3668486488b9bb053809dfb9"

account_sid = "Your Twilio account sid"
auth_token = "Your Twilio API token"
client = Client(account_sid, auth_token)

STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

NEWS_PARAMETERS = {
    "q": "tesla",
    "from": "2022-07-29",
    "apikey": NEWS_API_KEY
}

# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
response_stock_price = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMETERS)
json_stock_data = response_stock_price.json()
yesterday_close = json_stock_data['Time Series (Daily)']['2022-07-29']['4. close']

# TODO 2. - Get the day before yesterday's closing stock price
day_before_yesterday_close = json_stock_data['Time Series (Daily)']['2022-07-28']['4. close']

# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
day_before_yesterday_close_fl = float(day_before_yesterday_close)
yesterday_close_fl = float(yesterday_close)
two_day_difference = yesterday_close_fl - day_before_yesterday_close_fl

# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
difference_by_perc_up = round((two_day_difference / (yesterday_close_fl + day_before_yesterday_close_fl / 2)) * 100, 2)
difference_by_perc_down = round((two_day_difference / (day_before_yesterday_close_fl + yesterday_close_fl / 2)) * 100,
                                2)

# TODO 5. - If TODO4 percentage is greater than 3 then extract the relevant articles from the News API.
if difference_by_perc_up > 3 or difference_by_perc_down > 3:
    response_news = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMETERS)
    response_news_json = response_news.json()
    todays_articles = response_news_json['articles']
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    first_article = todays_articles[0]['title']
    first_article_desc = todays_articles[0]['description']
    first_article_url = todays_articles[0]['url']
    second_article = todays_articles[1]['title']
    second_article_desc = todays_articles[1]['description']
    second_article_url = todays_articles[1]['url']
    third_article = todays_articles[2]['title']
    third_article_desc = todays_articles[2]['description']
    third_article_url = todays_articles[2]['url']
    # TODO 6. use the News API to get articles related to the COMPANY_NAME.
    first_article_full = f"{first_article}\n{first_article_desc}\n{first_article_url}"
    second_article_full = f"{second_article}\n{second_article_desc}\n{second_article_url}"
    third_article_full = f"{third_article}\n{third_article_desc}\n{third_article_url}"

    # TODO 7. - Use Python to create an output that contains the first 3 articles.
    relevant_articles = first_article_full + "\n\n" + second_article_full + "\n\n" + third_article_full

    # TODO 9. - Send each article as a separate message via Twilio.
    if difference_by_perc_up > 3:
        message = client.messages \
            .create(
            body=f"TSLA: 🔺{difference_by_perc_up}%\nHeadline: {first_article}\nBrief: {first_article_desc}\n{first_article_url}",
            from_='Twilio phone number',
            to='Your phone number'
        )
        print(message.status)
    elif difference_by_perc_down > 3:
        message = client.messages \
            .create(
            body=f"TSLA: 🔻{difference_by_perc_down}%\nHeadline: {first_article}\nBrief: {first_article_desc}\n{first_article_url}",
            from_='Twilio phone number',
            to='Your phone number'
        )
        print(message.status)
    if difference_by_perc_up > 3:
        message = client.messages \
            .create(
            body=f"TSLA: 🔺{difference_by_perc_up}%\nHeadline: {second_article}\nBrief: {second_article_desc}\n{second_article_url}",
            from_='Twilio phone number',
            to='Your phone number'
        )
        print(message.status)
    elif difference_by_perc_down > 3:
        message = client.messages \
            .create(
            body=f"TSLA: 🔻{difference_by_perc_down}%\nHeadline: {second_article}\nBrief: {second_article_desc}\n{second_article_url}",
            from_='Twilio phone number',
            to='Your phone number'
        )
        print(message.status)
    if difference_by_perc_up > 3:
        message = client.messages \
            .create(
            body=f"TSLA: 🔺{difference_by_perc_up}%\nHeadline: {third_article}\nBrief: {third_article_desc}\n{third_article_url}",
            from_='Twilio phone number',
            to='Your phone number'
        )
        print(message.status)
    elif difference_by_perc_down > 3:
        message = client.messages \
            .create(
            body=f"TSLA: 🔻{difference_by_perc_down}%\nHeadline: {third_article}\nBrief: {third_article_desc}\n{third_article_url}",
            from_='Twilio phone number',
            to='Your phone number'
        )
        print(message.status)