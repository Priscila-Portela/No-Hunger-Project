#Libraries
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

st.set_page_config(page_title='Country - No Hunger', page_icon='🍅', layout='wide')

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

def country_metric(df, numeric_variable, title_variable, title_graph):
        
    """ 
        This function is responsible for generating a bar chart, which groups countries according to unique values and a chosen numerical variable.
    
        1. Selects the rows and columns of interest
        2. Groups by country
        3. Calculates the number of unique values of the numerical variable of interest (numeric_variable) for each grouping
        4. Creates a chart
        5. Applies white lines to the outline of the bars
        6. Hides the color scale
        7. Applies the title to the chart
        8. Generates the chart with the desired information

                Input:
            - df: DataFrame with the necessary data for the calculation
            - numeric_variable: Numerical variable of interest to compose the "y" axis
            - title_variable: Title of the "y" axis
            - title_graph: Title of the chart

        Output: Bar chart
    """   

    df_aux = (df.loc[:, [numeric_variable, 'Country_Name']].groupby('Country_Name')
                            .nunique()
                            .sort_values(by=numeric_variable, ascending=False)
                            .reset_index())

    fig = (px.bar(df_aux, x='Country_Name', y=numeric_variable,
        labels={'Country_Name': '<b>Country</b>', numeric_variable: title_variable},
        color= numeric_variable,
        text=numeric_variable,
        color_continuous_scale=['#D19792', '#CB3B2F' ])
        )

    fig.update_traces(marker_line_color = 'white', marker_line_width = 1.5)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(title_text= title_graph , title_x=0.31)
    return fig


def country_metric_mean(df, numeric_variable, title_variable, title):
        
    """ 
    This function is responsible for generating a horizontal bar chart, which groups countries according to the mean and a chosen numerical variable.
    
        1. Selects the rows and columns of interest
        2. Groups by country
        3. Calculates the mean of the numerical variable of interest (numeric_variable) for each grouping
        4. Creates a chart
        5. Applies white lines to the outline of the bars
        6. Hides the color scale
        7. Applies the title to the chart
        8. Generates the chart with the desired information

        Input: 
            - df: DataFrame with the necessary data for the calculation
            - numeric_variable: Numerical variable of interest to compose the "x" axis
            - title_variable: Title of the "x" axis
            - title_graph: Title of the chart

        Output: Output: Horizontal bar chart
    """   

    df_aux = df.loc[:, [numeric_variable, 'Country_Name']].groupby('Country_Name').mean().sort_values(by=numeric_variable, ascending=True).round(1).reset_index()

    fig = (px.bar(df_aux, x=numeric_variable, y='Country_Name',
                labels={'Country_Name': '<b>Country</b>', numeric_variable: title_variable},
                color= numeric_variable,
                text=numeric_variable,
                color_continuous_scale=['#D19792', '#CB3B2F' ]))
    
    fig.update_traces(marker_line_color = 'white', marker_line_width = 1.5)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(title_text=title, title_x=0.1)
    return fig

#------------------------------------Ending Graphics function--------------------------------

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

#======================================================
#================== Streamlit Layout ==================
#======================================================

st.header('🌎 Countries Analysis', divider='red')

#----------------Container 1---------------

with st.container(border=True):

    col1, col2 = st.columns(2, gap = "large")

    with col1:
        fig = country_metric(df, 'Restaurant ID', '<b>Number of Restaurants</b>', '🌎 Number of restaurants registered per country')
        st.plotly_chart( fig, use_container_width=True)

    with col2:
        fig = country_metric(df, 'City', '<b>Number of Cities</b>', '📍 Number of Cities registered per Country')
        st.plotly_chart( fig, use_container_width=True)

#----------------Container 2---------------

with st.container(border=True):
    st.markdown("<h1 style='text-align: center; color: #E85246;'><p style='font-size:25px;'><b>Country-wise Costs and Ratings</b></p></h1>", unsafe_allow_html=True)

    df_aux = df.loc[:, ['Country_Name', 'Cost_dolar', 'Aggregate rating', 'Votes']].groupby('Country_Name').mean().round(2).sort_values('Cost_dolar', ascending=False).reset_index()
    column_names = {"Country_Name": "Country",
            "Cost_dolar": st.column_config.NumberColumn("Price for two people", format="$ %d"),
            "Aggregate rating": "Rating",
            "Votes": "Votes"}
    st.dataframe(df_aux, use_container_width=True, 
                 height=300, column_config= column_names , 
                 hide_index=True)
        
#----------------Container 3---------------

with st.container(border=True):

    col1, col2, col3 = st.columns(3)

    with col1:
        fig = country_metric_mean(df, 'Aggregate rating', '<b>Average rating</b>', '⭐️ Average rating per Country')
        st.plotly_chart( fig, use_container_width=True)
        
    with col2:
        fig = country_metric_mean(df, 'Votes', '<b>Number of Evaluations</b>', '🗒️ Average evaluations per Country')
        st.plotly_chart( fig, use_container_width=True)

    with col3:    
        fig = country_metric_mean(df, 'Cost_dolar', '<b>Average price per two</b>', '💲 Average Cost for Two People Worldwide')
        st.plotly_chart( fig, use_container_width=True)