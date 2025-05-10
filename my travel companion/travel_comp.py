import streamlit as st
import psycopg2
import folium.map
import pandas as pd
import folium
import folium.plugins as plugins #custom icon
from streamlit_folium import st_folium

from dotenv import load_dotenv
import os
load_dotenv()

#establishing db connection to neondb
conn = psycopg2.connect(
    host=os.getenv("db_host"),
    database=os.getenv("db_name"),
    user=os.getenv("db_user"),
    password=os.getenv("db_password")
)
#fetch data from neon
query = "SELECT name,category,address,ST_Y(geom::geometry) AS latitude,ST_X(geom::geometry) AS longitude FROM poi"
data = pd.read_sql(query, conn)
conn.close()


#get categories from the table
categories = data['category'].unique().tolist()

#Initializing as streamlit app
st.title("My Travel Companion")
st.write("This app shows an interactive GIS map that allows you to lookup interesting places in your area")
st.sidebar.header("What are you looking to find")

#enabling the filter option
selected_categories = st.sidebar.multiselect("Select categories:", categories)
if selected_categories:
    filtered_data = data[data['category'].isin(selected_categories)]
else:
    filtered_data = data
#display the results
if selected_categories:
    st.write(f"Showing: {', '.join(selected_categories)}")
else:
    st.write("Showing all categories")

st.write(filtered_data)

#creating the basemap using folium
places = folium.Map(location=[-1.9445401885863784,30.08988685088784],zoom_start= 12)

# Adding base layers
folium.TileLayer('OpenStreetMap').add_to(places)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Satellite'
).add_to(places)

# Add layer control so user can toggle layers
folium.LayerControl().add_to(places)

#iterating through the different coordinates and create markers

for index, row in filtered_data.iterrows():
    if row['category'] == "Health facility" :
        icon = plugins.BeautifyIcon(
            icon="tent",
            icon_shape="circle",
            border_color='red',
            text_color="#007799",
            background_color='red'
        )
    elif row['category'] == "bank":
        icon = plugins.BeautifyIcon(
            icon="tent",
            icon_shape="circle",
            border_color='purple',
            text_color="#007799",
            background_color='purple'
        )
    elif row['category'] == "Market":
        icon = plugins.BeautifyIcon(
            icon="tent",
            icon_shape="circle",
            border_color='yellow',
            text_color="#007799",
            background_color='yellow'
        )
    elif row['category'] == "Police Station":
        icon = plugins.BeautifyIcon(
            icon="tent",
            icon_shape="circle",
            border_color='blue',
            text_color="#007799",
            background_color='blue'
        )
    else:
        icon = plugins.BeautifyIcon(
            icon="tent",
            icon_shape="circle",
            border_color='green',
            text_color="#007799",
            background_color='green'
        )

    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"{row['name']}<br>{row['category']}<br>{row['address']}",
        icon=icon
    ).add_to(places)
#displaying in streamlit
st_folium(places, width=700, height=500)

#save map to the file
places.save('index.html')