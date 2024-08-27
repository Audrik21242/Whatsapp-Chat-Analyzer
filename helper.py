from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd


extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    media_links = df[df['messages'] == '<Media omitted>\n'].shape[0]
    words = []
    for message in df['messages']:
        words.extend(message.split())

    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), media_links, len(links)


# def busiest_users(df):
#     x = df['user'].value_counts()
#     busy_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
#         columns={'index': 'name', 'user': 'percent'})
#     return x, busy_df

def busiest_users(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    x = df['user'].value_counts()
    busy_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, busy_df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt', 'r')
    stopwords = f.read()
    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
    ret = pd.DataFrame(Counter(words).most_common(20))
    return ret


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['Years', 'month_num', 'Months']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Months'][i] + "-" + str(timeline['Years'][i]))
    timeline['Time'] = time

    return timeline


def daily_timelines(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('Only_Date').count()['messages'].reset_index()

    return daily_timeline


def daily_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['Months'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    activity_map = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return activity_map


