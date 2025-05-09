import folium.map
import pandas as pd
import folium
import folium.plugins as plugins #custom icon



fp = "travel_data.csv"
data = pd.read_csv(fp, sep = ",")
#print(data)

#creating the basemap using folium
places = folium.Map(location=[5.082758114,-1.348043433],zoom_start= 10, tiles= "CartoDB positron")

#iterating through the different coordinates and create markers

for index , row in data.iterrows():
    folium.Marker(
        location=[row['Lat'], row['Long']],
        popup= f"{row['Place']} ({row['Name']}) {row['Status']} {row['Notes']}",
        icon=plugins.BeautifyIcon(
                        icon="tent",
                        icon_shape="circle",
                        border_color='purple',
                        text_color="#007799",
                        background_color='purple'
                    )
    ).add_to(places)
    
#save map to the file
places.save('index.html')