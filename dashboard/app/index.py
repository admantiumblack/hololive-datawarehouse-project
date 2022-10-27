import streamlit as st
from parts.stats import single_stat

def main():
    st.set_page_config(layout='wide', initial_sidebar_state='collapsed')
    is_compare = st.sidebar.checkbox('Compare Talent Stats')
    if is_compare:
        st.title('TBA')
    else:
        single_stat()

main()