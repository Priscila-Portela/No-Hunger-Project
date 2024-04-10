#Libraries
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import streamlit as st
from PIL import Image


st.set_page_config(page_title='Main Page - No Hunger', page_icon='🍅', layout='wide')

#Import dataset
df_raw = pd.read_csv('dataset.csv')
df = df_raw.copy()

#----------------------------------------------------------------------------------#
#--------------------------------- Data Cleaning ----------------------------------#
#----------------------------------------------------------------------------------#

#Remove columns where all variables are the same
df = df.drop('Switch to order menu', axis=1)

#Create a column with the name of the countries
def country_code_to_name(row):
    if row['Country Code'] == 1:
        return 'India'
    elif row['Country Code'] == 14:
        return 'Australia'
    elif row['Country Code'] == 30:
        return 'Brazil'
    elif row['Country Code'] == 37:
        return 'Canada'
    elif row['Country Code'] == 94:
        return 'Indonesia'
    elif row['Country Code'] == 148:
        return 'New Zeland'
    elif row['Country Code'] == 162:
        return 'Philippines'
    elif row['Country Code'] == 166:
        return 'Qatar'
    elif row['Country Code'] == 184:
        return 'Singapure'
    elif row['Country Code'] == 189:
        return 'South Africa'
    elif row['Country Code'] == 191:
        return 'Sri Lanka'
    elif row['Country Code'] == 208:
        return 'Turkey'
    elif row['Country Code'] == 214:
        return 'United Arab Emirates'
    elif row['Country Code'] == 215:
        return 'England'
    elif row['Country Code'] == 216:
        return 'USA'

# Apply the function to the 'Country_Name' column using apply
df['Country_Name'] = df.apply(country_code_to_name, axis=1)

# Removing duplicate values
df = df.drop_duplicates().reset_index()

# Removal of unwanted values
df = df.loc[(df['Cuisines'] != 'nan')]
df = df.loc[(df['Cuisines'] != 'Mineira')]
df = df.loc[(df['Cuisines'] != 'Drinks Only')]
df = df.loc[(df['Cuisines'] != 'Others')]
df = df.loc[(df['Restaurant ID'] != 16608070)]
df = df.loc[(df['Restaurant ID'] != 95314)]

#Transform column types
df.loc[:, ['Cuisines']] = df['Cuisines'].astype(str)
df.loc[:, 'Restaurant ID'] = df['Restaurant ID'].astype(int)
df.loc[:, 'Has Table booking'] = df['Has Table booking'].astype(int)
df.loc[:, 'Has Online delivery'] = df['Has Online delivery'].astype(int)
df.loc[:, 'Longitude'] = df['Longitude'].astype(float)
df.loc[:, 'Latitude'] = df['Latitude'].astype(float)

#Manipulate the "Cuisines" column so that only the first type of cuisine is applied in each restaurant
df["Cuisines"] = df.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])

#Create a column with the values related to the dish for two in dollars
def calculate_currency_dolar(row):
    if row['Currency'] == 'Botswana Pula(P)':
        return row['Average Cost for two'] / 13.60
    elif row['Currency'] == 'Brazilian Real(R$)':
        return row['Average Cost for two'] / 5.07
    elif row['Currency'] == 'Emirati Diram(AED)':
        return row['Average Cost for two'] / 3.67
    elif row['Currency'] == 'Indian Rupees(Rs.)':
        return row['Average Cost for two'] / 83.29
    elif row['Currency'] == 'Indonesian Rupiah(IDR)':
        return row['Average Cost for two'] / 15888.45
    elif row['Currency'] == 'NewZealand($)':
        return row['Average Cost for two'] / 1.66
    elif row['Currency'] == 'Pounds(£)':
        return row['Average Cost for two'] / 0.79
    elif row['Currency'] == 'Qatari Rial(QR)':
        return row['Average Cost for two'] / 3.64
    elif row['Currency'] == 'Rand(R)':
        return row['Average Cost for two'] / 18.68
    elif row['Currency'] == 'Sri Lankan Rupee(LKR)':
        return row['Average Cost for two'] / 298.98
    elif row['Currency'] == 'Turkish Lira(TL)':
        return row['Average Cost for two'] / 32.01
    elif row['Country Code'] == 14:
        return row['Average Cost for two'] / 1.52
    elif row['Country Code'] == 184:
        return row['Average Cost for two'] / 1.35
    elif row['Country Code'] == 37:
        return row['Average Cost for two'] / 1.36
    else:
        return row['Average Cost for two']
    
# Apply the function to the 'Cost_dollar' column using .apply
df['Cost_dolar'] = df.apply(calculate_currency_dolar, axis=1)

#Round values
df['Cost_dolar'] = df['Cost_dolar'].round(2)


#--------------------------------------------------------------------------------------#
#--------------------------------- End Data Cleaning ----------------------------------#
#--------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------
#------------------------------- START CODE -------------------------------------
#--------------------------------------------------------------------------------

#====================================================
#=============== Sidebar in Streamlit ===============
#====================================================


image_path = 'logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width=250)

st.sidebar.markdown('# 🍅 No Hunger')
st.sidebar.markdown('## Discover the best restaurants!')
st.sidebar.markdown("""---""")

country_list = ['Philippines', 'Brazil', 'Australia', 'USA',
                'Canada', 'Singapure', 'United Arab Emirates', 'India',
                'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
                'Sri Lanka', 'Turkey']

country_options = st.sidebar.multiselect('Choose the countries for visualization:',
                                         country_list,
                                         default=country_list)
  
df = df.loc[df['Country_Name'].isin( country_options), :]       

st.sidebar.markdown("""---""")
st.sidebar.markdown('##### Powered by Priscila Rockenbach Portela')

#=======================================================
#=================== Layout Streamlit ==================
#=======================================================

st.header('🍅 No Hunger', divider='red')
st.markdown('### The best place to find your favorite new restaurant!')

with st.container(border=True):    
    st.markdown('##### We have the following metrics within our platform:')

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        df_aux = df.loc[:,'Restaurant ID'].nunique()
        col1.metric('Registered Restaurants', df_aux)

    with col2:
        df_aux = df.loc[:,'Country_Name'].nunique()
        col2.metric('Registered Countries', df_aux)

    with col3:
        df_aux = df.loc[:,'City'].nunique()
        col3.metric('Registered Cities', df_aux)

    with col4:
        df_aux = df.loc[:,'Votes'].sum()
        col4.metric('Registered Evaluations', df_aux)

    with col5:
        df_aux = df.loc[:,'Cuisines'].nunique()
        col5.metric('Registered Cuisines', df_aux)

with st.container(border=True):    
    st.markdown('##### 📌 Our Restaurants Around the World:')

    map = folium.Map(max_bounds=True, location=[0, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(map)
    for index, location_info in df.iterrows():
        folium.Marker(
            [location_info['Latitude'], location_info['Longitude']],
            popup=location_info[['Country_Name', 'Restaurant ID', 'Restaurant Name']]
        ).add_to(marker_cluster)
    folium_static(map, width=1024, height=600)