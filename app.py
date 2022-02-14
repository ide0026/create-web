import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st
from newsapi import NewsApiClient

st.title('GAFA株価可視化& NEWS')

st.sidebar.write("""
# 株価
こちらはGAFA株価可視化Webアプリです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
### 過去 **{days}日間** のGAFA株価
""")

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try: 
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 3500.0, (0.0, 3500.0)
    )

    tickers = {
        'apple': 'AAPL',
        'facebook': 'FB',
        'google': 'GOOGL',
        #'microsoft': 'MSFT',
        #'netflix': 'NFLX',
        'amazon': 'AMZN'
    }
    
    df = get_data(days, tickers)
    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['google', 'amazon', 'facebook', 'apple']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価 (USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)

except:
    st.error(
        "エラーが発生しました。ページを読み込み直してください"
    )

#この先googleニュース取得
def getNews_google():
    newsapi = NewsApiClient(api_key='b4db0f52d6fe498e8153750a1ba090f9')
    news_google = newsapi.get_everything(q='google')

    articles_google = news_google["articles"]

    my_articles_google = []
    my_news_google = ""
    google_result = st.empty()

    for article_google in articles_google:
        my_articles_google.append(article_google["title"])
    
    with google_result:
        for i in range(10):
            my_news_google = my_news_google + str(i) + "" + my_articles_google[i] + "\n"
        st.write(my_news_google)

#apple
def getNews_apple():
    newsapi = NewsApiClient(api_key='b4db0f52d6fe498e8153750a1ba090f9')
    news_apple = newsapi.get_everything(q='apple')
    articles_apple = news_apple["articles"]
    my_articles_apple = []
    my_news_apple = ""
    apple_result = st.empty()

    for article_apple in articles_apple:
        my_articles_apple.append(article_apple["title"])
    
    with apple_result:
        for x in range(10):
            my_news_apple = my_news_apple + str(x) + "" + my_articles_apple[x] + "\n"
        st.write(my_news_apple)

#facebook
def getNews_facebook():
    newsapi = NewsApiClient(api_key='b4db0f52d6fe498e8153750a1ba090f9')
    news_facebook = newsapi.get_everything(q='facebook')
    articles_facebook = news_facebook["articles"]
    my_articles_facebook = []
    my_news_facebook = ""
    facebook_result = st.empty()

    for article_facebook in articles_facebook:
        my_articles_facebook.append(article_facebook["title"])
    
    with facebook_result:
        for y in range(10):
            my_news_facebook = my_news_facebook + str(y) + "" + my_articles_facebook[y] + "\n"
        st.write(my_news_facebook)

#amazon
def getNews_amazon():
    newsapi = NewsApiClient(api_key='b4db0f52d6fe498e8153750a1ba090f9')
    news_amazon = newsapi.get_everything(q='amazon')
    articles_amazon = news_amazon["articles"]
    my_articles_amazon = []
    my_news_amazon = ""
    amazon_result = st.empty()

    for article_amazon in articles_amazon:
        my_articles_amazon.append(article_amazon["title"])
    
    with amazon_result:
        for z in range(10):
            my_news_amazon = my_news_amazon + str(z) + "" + my_articles_amazon[z] + "\n"
        st.write(my_news_amazon)


if __name__ == '__main__':
    getNews_google()

if __name__ == '__main__':
    getNews_apple()

if __name__ == '__main__':
    getNews_facebook()

if __name__ == '__main__':
    getNews_amazon()