import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    msg = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': msg, 'msg_date': dates})
    df['msg_date'] = pd.to_datetime(df['msg_date'], format='%d/%m/%Y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['Years'] = df['msg_date'].dt.year
    df['month_num'] = df['msg_date'].dt.month
    df['Months'] = df['msg_date'].dt.month_name()
    df['Day'] = df['msg_date'].dt.day
    df['Hour'] = df['msg_date'].dt.hour
    df['Minute'] = df['msg_date'].dt.minute
    df['Only_Date'] = df['msg_date'].dt.date
    df['day_name'] = df['msg_date'].dt.day_name()

    period = []
    for Hour in df[['day_name', 'Hour']]['Hour']:
        if Hour == 23:
            period.append(str(Hour) + "-" + str('00'))
        elif Hour == 0:
            period.append(str('00') + "-" + str(Hour + 1))
        else:
            period.append(str(Hour) + "-" + str(Hour + 1))

    df['period'] = period
    return df
