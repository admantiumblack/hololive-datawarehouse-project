from hydralit import HydraHeadApp
import streamlit as st


class SingleTalentApp(HydraHeadApp):
    
    def __init__(self, title='', **kwargs) -> None:
        self.__dict__.update(kwargs)
        self.title=title
        
    def run(self):
        st.title('bod')