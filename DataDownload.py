import pytz
import pandas as pd
import snscrape.modules.twitter as tw
from datetime import datetime as dt

def text_downloader(file_name,twitter_ID,start,end):


    f = open(file_name, 'w', encoding='utf-8')
    my_query = "from:" + twitter_ID + " since:" + start + " until:" + end
    for tweet in tw.TwitterSearchScraper(query=my_query).get_items():
        date_str = tweet.date.strftime("%Y-%m-%d %H:%M:%S%z")
        date_str = date_str[:-2] + ":" + date_str[-2:]
        f.write(date_str + "|" + tweet.content + "\n")
    f.close()

    # Read Twitter data into Python
    em = []
    dates = []
    f = open(file_name, "r", encoding="utf-8")
    for l in f:
        line = l.split("|")
        date_str = line[0]  # +"+00:00"
        try:
            date_time = dt.fromisoformat(date_str)
            date_time = date_time.astimezone(pytz.timezone("US/Eastern"))
            line[0] = date_time
            line[1] = line[1][:-1]
            em.append(line)
            dates.append(date_time.date())
        except:
            em[-1][1] += " " + l[:-1]
    f.close()

    em = pd.DataFrame(data=em, columns=['Time', 'Tweet'])
    em['Date'] = dates
    # em['Date'] = em['Date'].astype(str)
    return em

file_name = ['trump','Lisa','BloombergNews','YahooFinance']
ID = ['realDonaldTrump','lisaabramowicz1','business','YahooFinance']
for i in range(len(file_name)):
    text = text_downloader(file_name=file_name[i], twitter_ID=ID[i],
                       start="2016-01-01", end="2020-12-01")
    output_name = file_name[i]+'_tweets.csv'
    text.to_csv(output_name,index=False)
    print(file_name[i]+" Done!")
