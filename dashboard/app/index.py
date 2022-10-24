import hydralit as hy
import hydralit_components as hc
from pages.single_talent_page import SingleTalentApp
import streamlit as st

# st.write('Some options to change the way our Hydralit application looks and feels')
c1,c2,c3,c4,_ = st.columns([2,2,2,2,8])
hydralit_navbar = c1.checkbox('Use Hydralit Navbar',True)
sticky_navbar = c2.checkbox('Use Sticky Navbar',False)
animate_navbar = c3.checkbox('Use Animated Navbar',True)
hide_st = c4.checkbox('Hide Streamlit Markers',True)

app = hy.HydraApp(
        title='Secure Hydralit Data Explorer',
        favicon="🐙",
        hide_streamlit_markers=hide_st,
        #add a nice banner, this banner has been defined as 5 sections with spacing defined by the banner_spacing array below.
        use_banner_images=["./resources/hydra.png",None,{'header':"<h1 style='text-align:center;padding: 0px 0px;color:grey;font-size:200%;'>Secure Hydralit Explorer</h1><br>"},None,"./resources/lock.png"], 
        banner_spacing=[5,30,60,30,5],
        use_navbar=hydralit_navbar, 
        navbar_sticky=sticky_navbar,
        navbar_animation=animate_navbar,
        # navbar_theme=over_theme
    )

app.add_app('talent tweet stats', app=SingleTalentApp(title='test'), is_home=True)

app.run()