
import re
import pandas as pd

def clean_date(date_str):
    # Remove square brackets and any extra spaces
    cleaned_str = date_str.strip('[] ')
    # Replace any non-standard spaces with standard spaces
    cleaned_str = re.sub(r'\s+', ' ', cleaned_str)
    # Parse the cleaned date string
    return pd.to_datetime(cleaned_str, format='%d/%m/%Y, %H:%M:%S %p')

def preprocessor(data):
    #pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s[A-Za-z][A-Za-z]]\s'
    pattern1 = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[A-Za-z][A-Za-z]\s-\s'
    messages=re.split(pattern1,data)[1:]
    dates=re.findall(pattern1,data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    #df['message_date'] = df['message_date'].apply(clean_date)
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M %p - ')
    df.rename(columns={'message_date':'date'},inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    #df['message'] = df['message'].str.replace('\u200e', '')
    df.drop(columns=['user_message'], inplace=True)
    df['year']=df['date'].dt.year
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    return df
