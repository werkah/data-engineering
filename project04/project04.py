#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
with open('proj4_params.json') as file:
    params = json.load(file)


# In[2]:


params


# In[3]:


from shapely.geometry import Point
from shapely.ops import nearest_points
import geopandas as gpd
import pandas as pd


# In[4]:


gdf = gpd.read_file('proj4_points.geojson')
gdf = gdf.to_crs(epsg=2180)
buffer = gdf.geometry.buffer(100)
counts_series = gdf.geometry.apply(lambda geom: buffer.contains(geom).sum())
gdf['count'] = counts_series
gdf.to_csv('proj4_ex01_counts.csv', columns=[params['id_column'], 'count'], index=False)
gdf = gdf.to_crs(epsg=4326)
gdf['lat'] = gdf.geometry.y
gdf['lon'] = gdf.geometry.x
x = gdf[['lamp_id','lat', 'lon']]
x.to_csv('proj4_ex01_coords.csv', index = False)


# In[5]:


import pyrosm
fp = pyrosm.get_data('cracow')
osm = pyrosm.OSM(fp)


# In[6]:


gdf_driving = osm.get_network(network_type="driving")
gdf_driving.head()
gdf_driving.columns


# In[7]:


primary_roads = gdf_driving[gdf_driving["highway"] == "primary"]


# In[8]:


primary_roads.head()


# In[9]:


primary_roads.columns


# In[10]:


gd = gpd.GeoDataFrame(primary_roads)
gd = gd[['id', 'name', 'geometry']]
gd.rename(columns={'id': 'osm_id'}, inplace=True)
gd.to_file('proj4_ex02_primary_roads.geojson',  driver='GeoJSON')


# In[11]:


import contextily as ctx
import matplotlib.pyplot as plt

gdf = gpd.read_file('proj4_countries.geojson')
gdf.geometry = gdf.geometry.envelope
gdf.to_pickle('proj4_ex04_gdf.pkl')

ax = gdf.plot(column='name', edgecolor='black', figsize=(10,10), alpha=0.5)
ax.set_axis_off()
ctx.add_basemap(ax, crs=gdf.crs.to_string())

for i, row in gdf.iterrows():
    country = row['name'].lower()
    file_name = f"proj4_ex04_{country}.png"
    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_aspect('equal')
    ax.set_xlim(row.geometry.bounds[0], row.geometry.bounds[2])
    ax.set_ylim(row.geometry.bounds[1], row.geometry.bounds[3])
    ctx.add_basemap(ax, crs=gdf.crs.to_string())
    boundary = row.geometry.boundary
    if isinstance(boundary, (list,)):
        for geom in boundary:
            x, y = geom.xy
            ax.plot(x, y, color='black')
    plt.savefig(file_name, dpi=300)
    plt.close()



