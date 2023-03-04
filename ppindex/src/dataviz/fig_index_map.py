import geopandas as gpd
import pandas as pd
import plotly.express as px
import numpy as np


def create_idx_maps(zoom, lat, lon, font_family, 
                    font_size, font_sub_size):
    '''
    this function creates the period poverty index choropleth

    inputs: df (pandas dataframe)
            gdf (geopandas dataframe)
            zoom (int) zoom level for displaying map
            lat (int) latitute for displaying map 
            lon (lon) longitude for displaying map
    output: choropleth map (plotly express class)
    '''
    census_tracts = gpd.read_file("ppindex/src/boundaries_census_tracts_2010.geojson")
    df = pd.read_json("ppindex/src/index_w_neigh_names.json")
    df = df.rename(columns={'tract':'Census Tract', 'pp_index':'Period Poverty Index'})

    fig = px.choropleth_mapbox(
        df, 
        geojson = census_tracts, 
        locations = "Census Tract", 
        featureidkey="properties.tractce10",
        color="Period Poverty Index", color_continuous_scale="amp", 
               range_color=(0, 1), 
        mapbox_style="carto-positron", opacity=0.5,
        hover_name="neighborhood_name",
        center={"lat": lat, "lon": lon}, zoom=zoom)

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title_x=0.5,
        font=dict(family=font_family), 
        margin={"r":0,"t":0,"l":0,"b":0}) 
    fig.update_coloraxes( # edit legend
        colorbar=dict(
            title=dict(text="Period Poverty<br>Index", 
                       font=dict(size=font_size)),
            tickfont=dict(size=font_sub_size),
            orientation='v', 
            len=0.8,
            thickness=15,
            ypad=8,
            yanchor='middle'))
    fig.update_traces( # polygon border
        marker_line_width=0.8, marker_line_color='white')

    return fig