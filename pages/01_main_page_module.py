import folium
import pandas as pd
import numpy  as np
import streamlit as st
import sys
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import folium_static
import inflection
import plotly.express       as px
import plotly.graph_objects as go
from matplotlib             import pyplot as plt

RAW_DATA_PATH = f"./data/raw/zomato.csv"
SAVE_DATA_PATH = f"./data/processed/data.csv"

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}


COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}


def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new

    return df

def country_name(country_id):
    return COUNTRIES[country_id]


def color_name(color_code):
    return COLORS[color_code]


def create_price_tye(price_range):
    if price_range == 1:
        return "Cheap"
    elif price_range == 2:
        return "Normal"
    elif price_range == 3:
        return "Expensive"
    else:
        return "Gourmet"


def adjust_columns_order(dataframe):
    df = dataframe.copy()

    new_cols_order = [
        "restaurant_id",
        "restaurant_name",
        "country",
        "city",
        "address",
        "locality",
        "locality_verbose",
        "longitude",
        "latitude",
        "cuisines",
        "price_type",
        "average_cost_for_two",
        "currency",
        "has_table_booking",
        "has_online_delivery",
        "is_delivering_now",
        "aggregate_rating",
        "rating_color",
        "color_name",
        "rating_text",
        "votes",
    ]

    return df.loc[:, new_cols_order]


#Carregando a base de dados
df = pd.read_csv(RAW_DATA_PATH)
def process_data(df):

    df1 = df.copy()

    # Renomeando os arquivos
    df1 = rename_columns(df)

    # Criação de colunas
    df1['country'] = df1.loc[:,'country_code'].apply(lambda x: country_name(x))
    df1['price_type'] = df1.loc[:, 'price_range'].apply(lambda x: create_price_tye(x))
    df1['color'] = df1.loc[:, 'rating_color'].apply(lambda x: color_name(x))

    # Pegando apenas o primeiro elemento do tipo de cozinha
    df1 = df1.loc[df1['cuisines'].notnull(), :]
    df1['cuisines'] = df1.loc[:, 'cuisines'].astype(str).apply(lambda x: x.split(',')[0])

    # Removendo colunas desnecessárias
    df1 = df1.drop(columns = ['country_code','locality_verbose', 'switch_to_order_menu','rating_color'])

    # Removendo dados duplicados, entre outros
    df1 = df1.drop_duplicates(subset='restaurant_id', keep='first')
    df1 = df1.loc[df1['average_cost_for_two'] != 0, :]

    # Resetando o index
    df1 = df1.reset_index(drop = True)
    
    df1.to_csv(SAVE_DATA_PATH, index=False)
    
    return df1

df1 = process_data(df)
df1.head()

# Side bar Topo#

st.header ('Fome Zero')
st.header ('The best place to find your newest favorite restaurant!')

st.subheader ('We have the following brands within our platform:')

# Barra Lateral: Cabeçalho - Logo e nome da empresa

image_path = "logo.png"
image = Image.open(image_path)
st.sidebar.image(image)

st.sidebar.markdown ("<h3 style='text-align: center; color: red;'> World Gastronomic Best Experiences</h3>", unsafe_allow_html=True)
st.sidebar.markdown ('''___''')

# FILTROS SIDEBAR

st.sidebar.markdown ('# Filtros')

# País
paises = df1.loc[:, "country"].unique().tolist()
country_options = st.sidebar.multiselect('Selecione os países: ', paises, default = paises)

# Habilidatação dos filtros

# Filtro País

linhas = df1['country'].isin(country_options)
df1 = df1.loc[linhas, :]

# SIDEBAR - Final

st.sidebar.markdown("### Dados Tratados")

processed_data = pd.read_csv(SAVE_DATA_PATH)

st.sidebar.download_button(
        label="Download",
        data=processed_data.to_csv(index=False, sep=";"),
        file_name="data.csv",
        mime="text/csv",
    )


st.sidebar.markdown ('''___''')
st.sidebar.markdown ('###### Powered by Comunidade DS')
st.sidebar.markdown ('###### Data Analyst: Luccas Magalhães')

# Layout - Visão Home

with st.container():
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
               
        contagem = df1['restaurant_id'].nunique()
        col1.metric('Restaurantes Cadastrados', value = contagem)
               
        contagem = df1.loc[df1['has_table_booking'] == 1,:].shape[0]
        col1.metric('Restaurantes que aceitam reserva', value = contagem)
        
    with col2:
               
        contagem = df1.loc[df1['has_online_delivery'] == 1,:].shape[0]
        col2.metric('Restaurantes com pedido online', value = contagem)
        
        contagem = df1.loc[df1['is_delivering_now'] == 1,:].shape[0]
        col2.metric('Restaurantes que fazem entrega', value = contagem)

    with col3:
              
        contagem = df1['country'].nunique()
        col3.metric('Países Cadastrados', value = contagem)
    
        contagem = df1['city'].nunique()
        col3.metric('Cidades Cadastradas', value = contagem)
        
    with col4:
        
        contagem = df1['cuisines'].nunique()
        col4.metric('Culinárias Ofertadas', value = contagem)
        
        contagem = df1['votes'].sum()
        col4.metric('Avaliações feitas na plataforma', value = contagem)

with st.container():

    # Armazenamento dos dados

    datamapa = df1[['restaurant_name', 'longitude', 'latitude', 'cuisines', 'average_cost_for_two', 'currency', 'aggregate_rating', 'color']].reset_index(drop = True)

   # Criando o mapa
    mapa = folium.Map(zoom_start = 15)

    #Criando os clusters
    cluster = MarkerCluster().add_to(mapa)

    icon = 'fa-cutlery'

    #Colocando os pinos
    for index, location_info in datamapa.iterrows():
        folium.Marker([location_info['latitude'],       
                       location_info['longitude']],
                       icon = folium.Icon(color=location_info['color'], icon=icon, prefix='fa'),
                       popup = folium.Popup(f"""<h6> <b> {location_info['restaurant_name']} </b> </h6> <br>
                                            Cozinha: {location_info['cuisines']} <br>
                                            Preço médio para dois: {location_info['average_cost_for_two']} ({location_info['currency']}) <br>
                                            Avaliação: {location_info['aggregate_rating']} / 5.0 <br> """,
                                            max_width= len(f"{location_info['restaurant_name']}")*20)).add_to(cluster)

    # Exibindo o mapa
    folium_static(mapa, width = 1024, height = 600)  
 

    with st.container():
       
        st.markdown('#### Top 10 restaurantes')
    
        df1 = df1[['restaurant_id', 'restaurant_name', 'country', 'city', 'cuisines', 'currency', 'average_cost_for_two', 'aggregate_rating', 'votes']].sort_values(['aggregate_rating', 'restaurant_id'], ascending = [False, True]).reset_index(drop=True).head(10)
        df1.columns=['ID','Nome','País','Cidade','Culinária', 'Moeda', 'Preço Médio - Prato p/2', 'Avaliação Média', 'Qt. Votos']
        st.dataframe(df1.style.format(subset=['Preço Médio - Prato p/2', 'Avaliação Média'], formatter="{:.2f}")) 

    