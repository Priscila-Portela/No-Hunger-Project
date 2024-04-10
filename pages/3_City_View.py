#Libraries
import pandas as pd
import plotly.express as px
from streamlit_folium import folium_static
import streamlit as st
from PIL import Image


st.set_page_config(page_title='City - No Hunger', page_icon='🍅', layout='wide')

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
colors_per_country = {
                    "India": "#FF1493",
                    "Australia": "#FF69B4",
                    "Brazil": "#FFA500",
                    "Canada": "#FF6347",
                    "Indonesia": "#00FFFF",
                    "New Zealand": "#00FFFF",
                    "Philippines": "#7FFF00",
                    "Qatar": "#32CD32",
                    "Singapore": "#EE82EE",
                    "South Africa": "#FF4500",
                    "Sri Lanka": "#20B2AA",
                    "Turkey": "#FF4500",
                    "United Arab Emirates": "#FF8C00",
                    "England": "#6495ED",
                    "USA": "#FF69B4"
                            }

def top_cities(df, numeric_variable, label_variable, title_graph):

    """ 
        This function is responsible for generating a bar chart that groups cities according to the numerical variable of interest and shows the Top 10.
    
        1. Selects the rows and columns of interest
        2. Groups by city
        3. Counts the unique values of the variable of interest for each city
        4. Creates a chart
        5. Applies white lines to the outline of the bars
        6. Hides the color scale
        7. Applies the title to the chart
        8. Generates the chart with the desired information
        
        Input: 
            - df: DataFrame with the necessary data for the calculation
            - numeric_variable: Numerical variable of interest to compose the "y" axis
            - label_variable: Title of the "y" axis
            - title_graph: Title of the chart

        Output: Bar chart
    """   
    cols = [numeric_variable, 'City', 'Country_Name']

    df_aux = (df.loc[:, cols].groupby(['City', 'Country_Name'])
                                .nunique()
                                .sort_values(by=numeric_variable, ascending=False)
                                .reset_index())
    df_top10 = df_aux.head(10)
    fig =(px.bar(df_top10, x='City', y=numeric_variable,
        labels={'City': '<b>City</b>', numeric_variable: label_variable, 'Country_Name': '<b>Country:</b>'},
        text=numeric_variable,
        color='Country_Name',
        color_discrete_map = colors_per_country,
        category_orders={'City': df_top10['City']}))
    fig.update_traces(marker_line_color = 'white', marker_line_width = 1.5)
    fig.update_layout(coloraxis_showscale=False)    
    fig.update_layout(title_text=title_graph, title_x=0.3)
    return fig    

def inverted_graph(df, top_asc, title_graph):

    """ This function is responsible for generating a horizontal bar chart that groups cities according to the mean of meal values for two people and shows the Top 7
    
        1. Selects the rows and columns of interest
        2. Groups by city
        3. Calculates the mean of meal values for each city
        4. Creates a chart
        5. Applies white lines to the outline of the bars
        6. Hides the color scale
        7. Applies the title to the chart
        8. Generates the chart with the desired information

        Input: 
            - df: DataFrame with the necessary data for the calculation
            - top_asc: Boolean value indicating whether the function should sort in ascending order (True) or descending order (False)
            - title_graph: Title of the chart

        Output: Horizontal bar chart
    """   

    cols = ['Cost_dolar', 'City', 'Country_Name']
    df_aux = df.loc[:, cols].groupby(['City', 'Country_Name']).mean().sort_values(by='Cost_dolar', ascending=top_asc).round(2).reset_index()
    df_top10 = df_aux.head(7)
    fig = (px.bar(df_top10, x="Cost_dolar", y='City',
    labels={'City': '<b>City</b>', 'Cost_dolar': '<b>Average price for two people (American dolar)</b>', 'Country_Name': '<b>Country:</b>'},
    color='Country_Name',
    color_discrete_map = colors_per_country,
    text='Cost_dolar',
    height=400,  
    category_orders={'City': df_top10['City']}))
    fig.update_traces(marker_line_color = 'white', marker_line_width = 1.5)
    fig.update_layout(coloraxis_showscale=False)    
    fig.update_layout(title_text=title_graph, title_x=0.3)
    return fig



def graph_top_filtered(df, line_filter, label_variable, graph_title):
    df_aux = df.loc[line_filter,  ['City', 'Restaurant ID', 'Country_Name', 'Aggregate rating']].groupby(['City', 'Country_Name']).count().sort_values('Restaurant ID', ascending=False).reset_index()

    df_top10 = df_aux.head(7)

    fig = (px.bar(df_top10, x='City', y='Restaurant ID',
        labels={'City': '<b>City</b>', 'Restaurant ID': label_variable, 'Country_Name': '<b>Country:</b>'},
        color='Country_Name',
        color_discrete_map = colors_per_country,
        text='Restaurant ID',
        height=400,  
        category_orders={'City': df_top10['City']}))
    
    fig.update_traces(marker_line_color = 'white', marker_line_width = 1.5)
    fig.update_layout(coloraxis_showscale=False)            
    fig.update_layout(title_text=graph_title, title_x=0.12)
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
st.sidebar.markdown('##  Discover the best restaurants!')
st.sidebar.markdown("""---""")


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

st.sidebar.markdown("""---""")
st.sidebar.markdown('##### Powered by Priscila Rockenbach Portela')

#======================================================
#================== Streamlit Layout ==================
#======================================================



st.header('📍 Cities Analysis', divider='red')

tab1, tab2 = st.tabs(['Overview', 'Price/Rating Analyses' ])

#----------------------------------------------------TAB 1--------------------------------------------------------------

with tab1:

#----------------Container 1---------------
    with st.container():

        fig= top_cities(df, 'Restaurant ID', '<b>Restaurants Registered</b>', '🍽️ Top 10 cities with more restaurants registered on the plataform')
        st.plotly_chart(fig, use_container_width=True)


#----------------Container 2---------------


    with st.container():

        fig= top_cities(df, 'Cuisines', '<b>Cuisine types offered </b>', '🍝 Top 10 cities with the greatest culinary diversity')
        st.plotly_chart(fig, use_container_width=True)

#----------------------------------------------------TAB 2--------------------------------------------------------------

with tab2:

#----------------Container 1---------------    

    with st.container(border=True):

        st.markdown("### 💲 Cities - Price")
        col1, col2 = st.columns(2, gap = "large")

        with col1:         
            fig = inverted_graph(df, False, '↑ Top 7 cities with highest price for two')
            st.plotly_chart( fig, use_container_width=True)

        with col2:
            fig = inverted_graph(df, True, '↓ Top 7 cities with lowest price for two')
            st.plotly_chart( fig, use_container_width=True)

#----------------Container 2---------------    

    with st.container(border=True):
        st.markdown("### 🏅 Cities - Rating")
        col1, col2 = st.columns(2, gap = "large")

        with col1:
            fig = graph_top_filtered(df,  (df['Aggregate rating'] >= 4), '<b>Number of Restaurants</b>', '⭐ Top 7 cities with the most restaurants rated higher than 4.0')
            st.plotly_chart( fig, use_container_width=True)

        with col2:
            fig = graph_top_filtered(df, (df['Aggregate rating'] <= 2.5), '<b>Average price for two people</b>', '🔻 Top 7 cities with the most restaurants rated lower than 2.5')
            st.plotly_chart( fig, use_container_width=True)