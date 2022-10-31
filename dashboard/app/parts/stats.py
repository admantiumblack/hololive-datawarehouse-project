from utilities.components import stream_plot, talent_name_menu, date_menu
import hydralit_components as hc
from utilities.queries import get_stream_fact_table, get_topics, get_tweet_fact_table
import streamlit.components.v1 as sc
from PIL import Image
import matplotlib.pyplot as plt
import math
from config import IMG_URLS
import streamlit as st
import networkx as nx
from pyvis.network import Network
from utilities.themes import vtuber_themes
from st_aggrid import AgGrid, GridOptionsBuilder


def tweet_stats(container, data, username):
    cols = container.columns([1, 2])
    cols[0].image(
        IMG_URLS[username]
    )
    average_data = data.mean()
    
    with cols[1]:
        st.write(f'average retweet count: ')
        st.write(math.floor(average_data["retweet_count"]))
        override_theme = vtuber_themes[username]
        st.write('density')
        hc.progress_bar(average_data['density'] * 100, f"{average_data['density']}", override_theme=override_theme, key=f'density_{username}')

        st.write('centrality')
        hc.progress_bar(average_data['centrality'] * 100, f"{average_data['centrality']}", override_theme=override_theme, key=f'centrality_{username}')

        st.write('clustering coeffecient')
        hc.progress_bar(average_data['avg_clustering_coef'] * 100, f"{average_data['avg_clustering_coef']}", override_theme=override_theme, key=f'clustering_{username}')

        st.write('reciprocity')
        hc.progress_bar(average_data['reciprocity'] * 100, f"{average_data['reciprocity']}", override_theme=override_theme, key=f'reciprocity_{username}')

def read_networks(data, username):
    file_path = '/data/data/{}'
    g = nx.DiGraph()
    for idx, i in data.iterrows():
        file_name = f'{username}_{i["date"]}_{i["row_number"]}'
        temp_graph = nx.read_graphml(file_path.format(file_name))
        g.update(temp_graph)
        
    tweet_net = Network(height='465px', bgcolor='#222222', font_color='white', notebook=True)
    tweet_net.from_nx(g)
    tweet_net.repulsion(node_distance=420, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)
    path = '/tmp'
    tweet_net.save_graph(f'../{path}/pyvis_graph.html')
    HtmlFile = open(f'../{path}/pyvis_graph.html', 'r', encoding='utf-8')
    return HtmlFile.read()

def tweet_networks(container, data, username):
    html_content = read_networks(data, username)
    with container:
        sc.html(html_content, height=435)

def create_stats(container, username):
    inspect = st.checkbox('inspect data')
    cat_tabs = container.tabs(['tweet', 'stream'])
    with cat_tabs[0]:
        tweet_dates = date_menu(st, username, key='tweet_date')
        if len(tweet_dates) == 2:
            data = get_tweet_fact_table(username, tweet_dates)
            if inspect:
                st.dataframe(data.drop('row_number', axis=1))
            else:
                tweet_stats(st, data, username)
                calculate_network = st.checkbox('show network')
                if calculate_network:
                    tweet_networks(cat_tabs[0], data, username)
                    
    with cat_tabs[1]:
        stream_dates = date_menu(st, username, key='stream_date', table_name='stream_fact')
        if len(stream_dates) == 2:
            data = get_stream_fact_table(username, stream_dates)
            if inspect:
                cols = st.columns(2)
                row_data = {}
                with cols[0]:
                    st.write('stream stats df')
                    gb = GridOptionsBuilder.from_dataframe(data.drop('topic_mapping_id', axis=1))
                    gb.configure_selection('single', use_checkbox=True)
                    row_data = AgGrid(
                        data,
                        gridOptions=gb.build(),
                        fit_columns_on_grid_load=True,
                        width='100%',
                        data_return_mode='AS_INPUT'
                    )['selected_rows']
                if row_data:
                    with cols[1]:
                        st.write('video topics')
                        topics = get_topics([row_data[0]['topic_mapping_id']])
                        st.dataframe(topics.drop('topic_mapping_id', axis=1), use_container_width=True)
                
            else:
                stream_plot(st, data, username)
    
def single_stat():
    talent_name = talent_name_menu(st.sidebar, key='name')
    st.title(f'{talent_name}')
    st.markdown("""
            <style>
            [data-testid=column]:nth-of-type(2) [data-testid=stVerticalBlock]{
                gap: 0rem;
            }
            </style>
            """,
            unsafe_allow_html=True
    )
    create_stats(st, talent_name)
    

