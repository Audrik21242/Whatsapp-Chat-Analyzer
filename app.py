import streamlit as st
import Preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = Preprocess.preprocess(data)
    # st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Analyse", user_list)

    if st.sidebar.button("Analyse"):
        no_messages, words, media_links, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(no_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(media_links)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['Time'], timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Timeline")
        d_timeline = helper.daily_timelines(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(d_timeline['Only_Date'], d_timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Most Active Days")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            most_busy_day = helper.daily_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(most_busy_day.index, most_busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Months")
            most_busy_months = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(most_busy_months.index, most_busy_months.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("User Activity Heatmap")
        activity_map = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_map)
        st.pyplot(fig)

        if selected_user == "Overall":
            st.title("Busiest Users")
            x, df_busy = helper.busiest_users(df, selected_user)  # Pass selected_user to the function
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(df_busy)

        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        most_com_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_com_df[0], most_com_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)
