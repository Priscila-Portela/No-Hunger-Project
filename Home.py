import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config( 
    page_title="Home",
    page_icon='🍅'
)


#====================================================
#=============== Sidebar in Streamlit ===============
#====================================================


image = Image.open('logo.png')
st.sidebar.image(image, width=250)

st.sidebar.markdown('# 🍅 No Hunger')
st.sidebar.markdown('## Discover the best restaurants!')

st.sidebar.markdown("""---""")

st.sidebar.markdown('### Our Dataset')

######

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')
my_large_df = pd.read_csv('dataset.csv')
csv = convert_df(my_large_df)
st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name='dataset.csv',
    mime='text/csv',
)

st.sidebar.markdown("""---""")
st.sidebar.markdown('##### Powered by Priscila Rockenbach Portela')


#======================================================
#================== Streamlit Layout ==================
#======================================================


st.write("# 📊 No Hunger Data Dashboard")
st.markdown( """ 
    Growth Dashboard was built to track data metrics of Countries and Restaurants registered on the platform.
    ### How to use this Growth Dashboard?
    - Main Page:
        - General metrics about our plataform
        - Geographic Visualization
    - Countries View:
        - General metrics of the countries served by No Hunger
    - Cities View:
        - Overview: General information about the cities with greatest metric relevance
        - Price/Rating Analysis: Insights on ratings and prices in the main cities
    - Cuisine View:
        - Visualization of metrics according to the types of cuisine registered
        - Identification of top restaurants according to price and rating
            
    ### ❗Ask for Help
        ✉️ Contact: priscila.rportela@gmail.com       
    """)