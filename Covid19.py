#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


get_ipython().system('pip install plotly')


# In[3]:


import plotly.express as px


# In[4]:


import plotly
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import init_notebook_mode, plot, iplot


# In[5]:


current_data=pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv')
current_data.head()


# In[6]:


current_data.tail()


# ## CHOROPLETH MAP PARA CASOS CONFIRMADOS DE COVID

# In[7]:


fig=px.choropleth(current_data,locations='Country',locationmode='country names',color='Confirmed',animation_frame='Date')
fig.update_layout(title='Choropleth map of confirmed cases till today',template='plotly_dark')
fig.show()


# ## CHOROPLETH FOR A PARTICULAR CONTINENT

# In[8]:


fig=px.choropleth(current_data,locations='Country',locationmode='country names',color='Confirmed',animation_frame='Date',scope='south america')
fig.update_layout(title='Choropleth map of confirmed cases till today',template='plotly_dark')
fig.show()


# In[9]:


def continent(contin):
    scope=contin
    fig=px.choropleth(current_data,locations='Country',locationmode='country names',color='Confirmed',animation_frame='Date',scope=contin)
    fig.update_layout(title='Choropleth map of confirmed cases till today',template='plotly_dark')
    return fig.show()


# In[10]:


continent('europe')


# ## geographical scatter plot
# #### la data se ve como puntos (x1,y1 x2,y2 x3,y3)
# #### debemos pasar la locacion en base a latitudes y longitudes para colocar los puntos

# In[11]:


fig=px.scatter_geo(current_data, locations='Country', locationmode='country names',color='Confirmed', size='Confirmed',hover_name='Country',animation_frame='Date', title='Spread over time')
fig.update(layout_coloraxis_showscale=False, layout_template = 'plotly_dark')
fig.show()


# ## PLOTTING OF RECOVERYS

# In[12]:


current_data.head()


# In[13]:


fig=px.choropleth(current_data,locations='Country',locationmode='country names',color='Recovered',animation_frame='Date')
fig.update_layout(title='Choropleth map of Recovered cases till today',template='plotly_dark')
fig.show()


# In[14]:


fig=px.scatter_geo(current_data, locations='Country', locationmode='country names',color='Recovered', size='Recovered',hover_name='Country',animation_frame='Date', title='Recovery over time')
fig.update(layout_coloraxis_showscale=False, layout_template = 'plotly_dark')
fig.show()


# ## Plotting of Deaths using Choropleth & Geo Scatter plot

# In[15]:


fig=px.choropleth(current_data,locations='Country',locationmode='country names',color='Deaths',animation_frame='Date')
fig.update_layout(title='Choropleth map of Deaths cases till today',template='plotly_dark')
fig.show()


# In[16]:


fig=px.scatter_geo(current_data, locations='Country', locationmode='country names',color='Deaths', size='Deaths',hover_name='Country',animation_frame='Date', title='Deaths over time')
fig.update(layout_coloraxis_showscale=False, layout_template = 'plotly_dark')
fig.show()


# ## How to extract Latitudes & Longitudes of a location

# In[17]:


get_ipython().system('pip install geopy')


# In[18]:


import geopy
from geopy.geocoders import Nominatim #tool para buscar open streat map data


# In[19]:


geolocator=Nominatim(user_agent='app')


# In[20]:


#test de obtener lat y long
location=geolocator.geocode('Eiffel Tower')
print(location.latitude,location.longitude)


# ## Data Preparation For Spatial Analysis

# In[21]:


current_data.head()


# In[22]:


df=current_data.copy()


# In[23]:


df.head()


# In[24]:


#filtro para obtener los datos de un pais especifico
df[df['Country']=='Afghanistan']


# In[25]:


#Agrupar en base a Countrys, de cada pais obtengo el maximo de confirmados,
#recuperados y muertos
df.groupby(['Country'])[['Confirmed','Recovered','Deaths']].max()


# In[26]:


#Armo el dataframe de el maximo de cada pais
df2=df.groupby(['Country'])[['Confirmed','Recovered','Deaths']].max().reset_index()
df2.head(10)


# In[27]:


#Necesitamos latitud y longitud de cada pais
lat_lon=[]
geolocatos=Nominatim(user_agent='app')
for location in df2['Country']: #recorro cada  pais del dataframe
    location=geolocator.geocode(location)
    if location is None:
        lat_lon.append(np.nan)
    else:
        geo=(location.latitude,location.longitude)
        lat_lon.append(geo)


# In[28]:


lat_lon


# In[29]:


#asignar la latitud y longitud a mi dataframe
df2['geo_loc']=lat_lon


# In[30]:


df2.head()


# In[31]:


#debo separar esta data en latitud y longitud, ya que es una lista, hago unzip
lat,lon=zip(*np.array(df2['geo_loc']))


# In[32]:


df2['lat']=lat
df2['lon']=lon


# In[33]:


df2.head()


# In[34]:


#descarto la columna geo:loc pq no tiene sentido ya
df2.drop('geo_loc',axis=1,inplace=True)


# In[35]:


df2.head()


# In[ ]:





# ## TILESET
# #### es una coleccion de raster o vector dividido en un grid uniforme de square tiles, un raste es una matriz de celdas o pixeles, organizados en filas y columnas (grid) donde cada celda contiene un valor que representa informacion, mientras que el vector es un datastructure usado para guardar spatial data, definidio por puntos de principio y fin 

# ## MARKER
# #### identifica una ubicacion en un mapa, debemos crear un basemap donde se colocaran los markers y luego agregarle los markers a este. Lo hacemos con libreria folium

# In[ ]:





# ## CREATE A BESEMAP

# In[36]:


import folium


# In[37]:


folium.Map(location=[54,15],zoom_start=2)


# ## PLOT CONFIRMED CASES USING MARKERS

# In[38]:


m=folium.Map()
m


# In[39]:


for id,row in df2.iterrows():
    folium.Marker(location=[row['lat'],row['lon']],popup=row['Confirmed']).add_to(m)
m    


# In[ ]:





# ## PLOTTING OF RECOVERY AND DEATHS USING MARKERS

# In[40]:


for id,row in df2.iterrows():
    folium.Marker(location=[row['lat'],row['lon']],popup=row['Recovered']).add_to(m)
m    


# In[41]:


for id,row in df2.iterrows():
    folium.Marker(location=[row['lat'],row['lon']],popup=row['Deaths']).add_to(m)
m    


# In[ ]:





# ## PLOT DEATHS USING MARKER CLUSTERS

# In[ ]:





# In[42]:


from folium.plugins import MarkerCluster
mc=MarkerCluster()


# In[43]:


mp=folium.Map()
for id,row in df2.iterrows():
    mc.add_child(folium.Marker(location=[row['lat'],row['lon']],popup=row['Deaths']))
mp.add_child(mc)

mp   


# In[ ]:





# ## GEOGRAPHIC HEATMAP
# #### nos permite demostrar areas de alta o baja densidad de algo

# In[ ]:





# In[44]:


from folium.plugins import HeatMap


# In[45]:


df2.head()


# In[46]:


m=folium.Map()
HeatMap(data=df2[['lat','lon','Confirmed']],radius=15).add_to(m)
m


# In[ ]:




