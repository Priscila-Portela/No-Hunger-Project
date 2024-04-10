#Libraries
import pandas as pd
import plotly.express as px
from streamlit_folium import folium_static
import streamlit as st
from PIL import Image


st.set_page_config(page_title='Cuisines - No Hunger', page_icon='🍅', layout='wide')

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


#----------------------------------Beginning Graphics function------------------------------

def best_restaurant(df, cuisine_type, col_id):

    """ 
        This function returns the name and rating of the best restaurants of the chosen cuisine type.
            
        1. Selects the rows and columns of interest
        2. Organizes the data according to the highest rating and, secondarily, the lowest Restaurant ID.
        3. Identifies the name of the restaurant with the highest rating
        4. Identifies the rating of the best restaurant.
        5. Returns the desired metric information

        
        Input: 
            - df: DataFrame with the necessary data for the calculation
            - cuisine_type: Cuisine types (object) present in the dataset
            - col_id: Column identifier of the layout

        Output: Metrics
    """   

    the_best = (df.loc[(df['Cuisines'] == cuisine_type), :]
                .sort_values(['Aggregate rating', 'Restaurant ID'], ascending=[False, True])
                .reset_index())
    best_name = the_best.loc[0, 'Restaurant Name']
    best_rating = the_best.loc[0, 'Aggregate rating']
    return col_id.metric(best_name, f"{best_rating}/5.0")


def top_cuisines(df, top_asc, graph_title):

    """
        This function is responsible for generating a horizontal bar chart, with the top 10 cuisine types.
            
        1. Selects the rows and columns of interest
        2. Groups by cuisine types
        3. Calculates the average ratings for each cuisine type
        4. Creates a chart
        5. Applies white lines to the outline of the bars
        6. Hides the color scale
        7. Applies the title to the chart
        8. Generates the chart with the desired information

        
        Input: 
            - df: DataFrame with the necessary data for the calculation
            - top_asc: Boolean value indicating whether the function should sort in ascending order (True) or descending order (False)
            - graph_title: Title of the chart
        
        Output: Horizontal bar chart
    """   

    cols = ['Cuisines', 'Aggregate rating']
    df_aux = df.loc[:, cols].groupby('Cuisines').mean().sort_values(by='Aggregate rating', ascending=top_asc).round(1).reset_index()
    df_top10 = df_aux.head(10)
    fig = (px.bar(df_top10, x='Cuisines', y="Aggregate rating",
    labels={'Aggregate rating': '<b>Mean rating</b>', 'Cuisines': '<b>Cuisine Type</b>'},
    color= 'Aggregate rating',
    text='Aggregate rating',
    width=1000,
    height=400,
    color_continuous_scale=['#D19792', '#CB3B2F' ]))
    fig.update_traces(marker_line_color = 'white', marker_line_width = 1.5)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(title_text=graph_title, title_x=0.35)
    return fig
        
#------------------------------------Ending Graphics function--------------------------------

#--------------------------------------------------------------------------------
#------------------------------- START CODE -------------------------------------
#--------------------------------------------------------------------------------

#====================================================
#=============== Sidebar in Streamlit ===============
#====================================================

image_path = 'logo.png'
image = Image.open(image_path )
st.sidebar.image( image, width=250)

st.sidebar.markdown('# 🍅 No Hunger')
st.sidebar.markdown('## Discover the best restaurants!')
st.sidebar.markdown("""---""")

#-----------Sidebar Countries
country_options = st.sidebar.multiselect(
    'Choose the countries for visualization:',
    ['Philippines', 'Brazil', 'Australia', 'USA',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default=['Philippines', 'Brazil', 'Australia', 'USA',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'] )

linhas_selecionadas = df['Country_Name'].isin( country_options)
df = df.loc[linhas_selecionadas,  :]       

#-----------Sidebar Cuisines
cuisine_type = ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
                'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
                'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
                'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
                'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
                'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
                'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
                'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
                'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian', 'Author',
                'Gourmet Fast Food', 'Lebanese', 'Modern Australian', 'African',
                'Coffee and Tea', 'Australian', 'Middle Eastern', 'Malaysian',
                'Tapas', 'New American', 'Pub Food', 'Southern', 'Diner', 'Donuts',
                'Southwestern', 'Sandwich', 'Irish', 'Mediterranean', 'Cafe Food',
                'Korean BBQ', 'Fusion', 'Canadian', 'Breakfast', 'Cajun',
                'New Mexican', 'Belgian', 'Cuban', 'Taco', 'Caribbean', 'Polish',
                'Deli', 'British', 'California', 'Eastern European', 'Creole',
                'Ramen', 'Ukrainian', 'Hawaiian', 'Patisserie', 'Yum Cha',
                'Pacific Northwest', 'Tea', 'Moroccan', 'Burmese', 'Dim Sum',
                'Crepes', 'Fish and Chips', 'Russian', 'Continental',
                'South Indian', 'North Indian', 'Salad', 'Finger Food', 'Mandi',
                'Turkish', 'Kerala', 'Pakistani', 'Biryani', 'Street Food',
                'Nepalese', 'Goan', 'Iranian', 'Mughlai', 'Rajasthani', 'Mithai',
                'Maharashtrian', 'Gujarati', 'Rolls', 'Momos', 'Parsi',
                'Modern Indian', 'Andhra', 'Tibetan', 'Kebab', 'Chettinad',
                'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi', 'Afghan',
                'Lucknowi', 'Charcoal Chicken', 'Mangalorean', 'Egyptian',
                'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian', 'Western',
                'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian', 'Balti',
                'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji', 'South African',
                'Durban', 'World Cuisine', 'Izgara', 'Home-made', 'Giblets',
                'Fresh Fish', 'Restaurant Cafe', 'Kumpir', 'Döner',
                'Turkish Pizza', 'Ottoman', 'Old Turkish Bars', 'Kokoreç']

cuisines_options = st.sidebar.multiselect('Choose the Cuisines for visualization:', cuisine_type,
                                          default=cuisine_type)

linhas_selecionadas = df['Cuisines'].isin(cuisines_options)
df = df.loc[linhas_selecionadas, :]  

#--------------------------
st.sidebar.markdown("""---""")
st.sidebar.markdown('##### Powered by Priscila Rockenbach Portela')

#======================================================
#================== Streamlit Layout ==================
#======================================================

st.header('🍝 Cuisines Analysis', divider='red')

#----------------Container 1---------------

with st.container():
    st.markdown("<h1 style='text-align: center; color: #E85246;'><p style='font-size:25px;'><b>🏆 Best Restaurants in the Main Cuisines</b></p></h1>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown("#### Italian")        
        best_restaurant(df, 'Italian', col1)

    with col2:
        st.markdown("#### Arabian")  
        best_restaurant(df, 'Arabian', col2)

    with col3:
        st.markdown("#### Brazilian")  
        best_restaurant(df, 'Brazilian', col3)

    with col4:
        st.markdown("#### Japanese")  
        best_restaurant(df, 'Japanese', col4)

    with col5:
        st.markdown("#### Hamburger")  
        best_restaurant(df, 'Burger', col5)


#----------------Container 2---------------

with st.container():
    st.markdown("<h1 style='text-align: center; color: #E85246;'><p style='font-size:25px;'><b>⭐ Top 10 - Highest Rated Restaurants</b></p></h1>", unsafe_allow_html=True)

    df_aux = df.loc[:, ['Restaurant Name', 'Restaurant ID', 'Country_Name', 'Cuisines', 'Cost_dolar', 'Aggregate rating', 'Votes']].sort_values(by=['Aggregate rating', 'Votes', 'Restaurant ID'], ascending=[False, False, True]).reset_index()

    df_top10 = df_aux.loc[:, ['Restaurant Name', 'Country_Name', 'Cuisines', 'Aggregate rating', 'Votes']].head(10)

    column_names = {"Restaurant Name": "Restaurant",
                    "Country_Name": "Country",
                    "Cuisines": "Cuisine",
                    "Aggregate rating": "Rating",
                    "Votes": "Votes"}
    st.dataframe(df_top10, use_container_width=True, column_config=column_names  )

#----------------Container 3---------------    

with st.container():
    col1, col2 = st.columns(2)

    with col1:

        fig = top_cuisines(df, False, '⭐ Top 10 Best Cusines')
        st.plotly_chart( fig, use_container_width=True)     
 
    with col2:

        fig = top_cuisines(df, True, '⭐ Top 10 Worst Cusines')
        st.plotly_chart( fig, use_container_width=True)   
