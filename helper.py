from typing import Counter
from urlextract import URLExtract
import pandas as pd
from wordcloud import WordCloud
extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user=='Overall':
        #total msg
        t_msg=df.shape[0]
        #total words
        word=[]
        for msg in df['message']:
            word.extend(msg.split())

        #total media file shared
        media=df[df['message']=='<Media omitted>\n'].shape[0]

        #Total URLs
        links = []
        for message in df['message']:
            links.extend(extract.find_urls(message))

        return t_msg,len(word),media,len(links)
    else:
        user_tmsg=df[df['user']==selected_user]
        #total words
        word=[]
        for msg in user_tmsg['message']:
            word.extend(msg.split())
        #total media
        media=user_tmsg[user_tmsg['message']=='<Media omitted>\n'].shape[0]
         #Total URLs
        links = []
        for message in user_tmsg['message']:
            links.extend(extract.find_urls(message))

        return user_tmsg.shape[0],len(word),media,len(links)
    

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'})
    return x,df
        
def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df