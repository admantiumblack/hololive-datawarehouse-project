from utilities.components import date_menu, stat_card, talent_name_menu, vtuber_image
from utilities.queries import get_stream_fact_table, get_tweet_fact_table
import streamlit as st

def get_theme(data1, data2, key):
    theme = 'neutral'
    if data1[key] > data2[key]:
        theme = 'good'
    elif data1[key] < data2[key]:
        theme = 'bad'
    return theme


def compare_stats():
    talent_names = []
    talent_names.append(talent_name_menu(st.sidebar, key='name1'))
    talent_names.append(talent_name_menu(st.sidebar, key='name2'))
    dates = date_menu(st, talent_names, 'talent_compare_dates')
    if len(dates) == 2:
        tweet_datas = [get_tweet_fact_table(i, dates).mean().fillna(0.0) for i in talent_names]
        stream_datas = [get_stream_fact_table(i, dates).mean().fillna(0.0) for i in talent_names]
        outer_cols = st.columns(2)
        for idx, i in enumerate(outer_cols):
            i.title(talent_names[idx])
            vtuber_image(i, talent_names[idx])
        for key in ['density', 'centrality', 'avg_clustering_coef', 'reciprocity']:
            cols = st.container().columns(2)
            for idx, j in enumerate(cols):
                theme = get_theme(tweet_datas[idx], tweet_datas[-(idx + 1)], key = key)
                stat_card(j, tweet_datas[idx], key, theme=theme, component_key=f'{idx}')
        
        for key in ['revenue_total', 'superchat_count']:
            cols = st.container().columns(2)
            for idx, j in enumerate(cols):
                theme = get_theme(stream_datas[idx], stream_datas[-(idx + 1)], key = key)
                stat_card(j, stream_datas[idx], key, theme=theme, component_key=f'{idx}')