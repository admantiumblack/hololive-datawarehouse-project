from utilities.queries import get_table_content, get_table_dates, get_topics
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def talent_name_menu(container, key=None):
    available_talents = get_table_content('user_dim')
    return container.selectbox('Talent Username', available_talents, key=key)

def date_menu(container, vtuber_name, key=None, table_name='tweet_fact'):
    date_range = get_table_dates(vtuber_name, table_name=table_name)
    return container.date_input(
        'date_range', 
        [date_range.iloc[0]['min_date'], date_range.iloc[0]['max_date']],
        min_value = date_range.iloc[0]['min_date'],
        max_value = date_range.iloc[0]['max_date'],
        key=key
    )

def stream_plot(container, data, username):
    topics = get_topics(data['topic_mapping_id'].tolist())
    fig1 = px.line(data, x='date', y='revenue_total', title=f"{username}'s stream revenue")
    fig2 = px.line(data, x='date', y='superchat_count', title=f"{username}'s superchat count")
    cols = container.columns(2)
    cols[0].plotly_chart(fig1, use_container_width=True)
    cols[1].plotly_chart(fig2, use_container_width=True)
    
    hist_plot = px.histogram(topics, x='topic_title')
    container.plotly_chart(hist_plot, use_container_width=True)
    