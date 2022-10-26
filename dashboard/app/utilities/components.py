from utilities.queries import get_table_content, get_tweet_dates
import streamlit as st

def talent_name_menu(container, key=None):
    available_talents = get_table_content('user_dim')
    return container.selectbox('Talent Username', available_talents, key=key)

def date_menu(container, vtuber_name, key=None):
    date_range = get_tweet_dates(vtuber_name)
    return container.date_input(
        'date_range', 
        [date_range.iloc[0]['min_date'], date_range.iloc[0]['max_date']],
        min_value = date_range.iloc[0]['min_date'],
        max_value = date_range.iloc[0]['max_date'],
        key=key
    )