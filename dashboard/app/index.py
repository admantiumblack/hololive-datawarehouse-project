import streamlit as st
from parts.stats import single_stat
from parts.compare import compare_stats

def main():
    st.set_page_config(layout='wide', initial_sidebar_state='collapsed')
    is_compare = st.sidebar.checkbox('Compare Talent Stats')
    if is_compare:
        compare_stats()
    else:
        single_stat()

main()