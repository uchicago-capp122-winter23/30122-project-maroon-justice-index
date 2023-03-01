# Author: Ivanna
# Date: 2/26/2023
# Purpose: save a geojson file with points for community centers to
#          be able to map them in plotly express

import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim

# read community centers filename and subset
df = pd.read_json("data/community_centers_chicago.json")

# initialize nominatim geocoder
geolocator = Nominatim(timeout=10, user_agent='myGeolocator')

# geocode address column
df['gcode'] = df['Address'].apply(geolocator.geocode)

# filter dataframe to remove NAs
df_without_none = df.dropna(subset=['gcode'])
df_without_none['lat'] = [g.latitude for g in df_without_none.gcode]
df_without_none['lon'] = [g.longitude for g in df_without_none.gcode]

df_without_none.to_csv("data/geocoded_community_centers_chicago.csv", index = False)

# turn dataframe into points
geometry = gpd.points_from_xy(df_without_none['lon'], df_without_none['lat'])
gdf = gpd.GeoDataFrame(df_without_none, geometry=geometry)

# bring in neighborhood polygons
s = "https://raw.githubusercontent.com/blackmad/neighborhoods/master/chicago.geojson"
neighborhoods = gpd.read_file(s)

# spatial join for community centers points and neighborhood names
joined = gpd.sjoin(gdf, neighborhoods, predicate='within')
joined = joined.rename(columns={'name':'Neighborhood', 'Name':'Community Center'})
joined.to_file('src/comm_centers_neighborhoods.geojson', driver='GeoJSON')  