from utilities.components import talent_name_menu, date_menu
import hydralit_components as hc
from utilities.queries import get_tweet_fact_table
import streamlit.components.v1 as sc
from PIL import Image
import matplotlib.pyplot as plt
import math
from config import IMG_URLS
import streamlit as st
import networkx as nx
from pyvis.network import Network


def tweet_stats(container, data, username):
    cols = container.columns([1, 2])
    cols[0].image(
        IMG_URLS[username]
    )
    average_data = data.mean()
    cols[1].write(f'average retweet count: ')
    cols[1].write(math.floor(average_data["retweet_count"]))
    override_theme = {'bgcolor': 'purple','progress_color': 'black', 'content_color':'white'}
    
    with cols[1]:
        st.write('density')
        hc.progress_bar(average_data['density'] * 100, f"{average_data['density']}", override_theme=override_theme, key='density')

        st.write('centrality')
        hc.progress_bar(average_data['centrality'] * 100, f"{average_data['centrality']}", override_theme=override_theme, key='centrality')

        st.write('clustering coeffecient')
        hc.progress_bar(average_data['avg_clustering_coef'] * 100, f"{average_data['avg_clustering_coef']}", override_theme=override_theme, key='clustering')

        st.write('reciprocity')
        hc.progress_bar(average_data['reciprocity'] * 100, f"{average_data['reciprocity']}", override_theme=override_theme, key='reciprocity')

def tweet_networks(container, data, username):
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
    with container:
        sc.html(HtmlFile.read(), height=435)

def stream_stats(container, username):
    pass

def create_stats(container, username):
    inspect = st.checkbox('inspect data')
    cat_tabs = container.tabs(['tweet', 'stream'])
    with cat_tabs[0]:
        dates = date_menu(st, username, key='date')
        if len(dates) == 2:
            data = get_tweet_fact_table(username, dates)
            if inspect:
                cat_tabs[0].dataframe(data.drop('row_number', axis=1))
            else:
                tabs = st.tabs(['stats', 'network'])
                tweet_stats(tabs[0], data, username)
                tweet_networks(tabs[1], data, username)
    with cat_tabs[1]:
        st.title('TBA')
    
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
    
