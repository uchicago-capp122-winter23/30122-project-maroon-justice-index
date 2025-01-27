'''
Author: Ivanna

This app renders the Dash application for our project

Run this app with `python -m ppindex` and visit
http://127.0.0.1:8050/ in your web browser
'''

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd

# import dfs and static graph maker functions
from .geocode_pp_partners_chicago import gdf
from .dataviz.fig_index_map import create_idx_maps
from .dataviz.fig_scatters import create_index_centers_scatter, create_income_population_scatter


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ----------------------- data and charts here ---------------------------------

# global vars to store fonts and sizes for graphs
L_FONT = "Work Sans, sans-serif"
LT_SIZE = 16
L_SIZE = 14

# ------ census tract pp index map --------

fig_idx = create_idx_maps(zoom=9.4, lat=41.8227, lon=-87.6014, 
                font_family=L_FONT, font_size=LT_SIZE)

# ---- scatterplots --------

fig_centers_scatter = create_index_centers_scatter(L_FONT, LT_SIZE)
fig_pop_scatter = create_income_population_scatter(L_FONT, LT_SIZE)

# ------ interactive community centers map ----------

joined = gpd.read_file("ppindex/src/comm_centers_neighborhoods.geojson")
joined = joined[["Community Center", "Type", "Category", "Neighborhood", 
                 "Address", "Contact", "Note", "gcode", "lat", "lon",
                 "geometry"]]
gdf = gdf.rename(columns={"Name":"Community Center"})
joined = pd.concat([joined, gdf])

def create_cc_maps(df, lat, lon):
    '''
    this function creates the community centers map

    input: df (pandas dataframe)
           lat (int) latitude 
           long (int) longitude 
    output: scatter map (plotly express class)
    '''
    fig_cc = px.scatter_mapbox(df, 
                        lat=lat, 
                        lon=lon, 
                        hover_name="Community Center",
                        hover_data={'Neighborhood': True, 'lat':False, 
                                    'lon':False,
                                    'Address':True},
                        opacity=0.5,
                        color="Category",
                        color_discrete_sequence=px.colors.qualitative.Bold,
                        mapbox_style="carto-positron")
    
    fig_cc.update_layout(
        title_x=0.5, 
        font=dict(family=L_FONT,
                  size=L_SIZE+1),
        margin={"r":0,"t":0,"l":0,"b":10})

    return fig_cc

# neighborhood dropdown options
options = [{'label': neighborhood, 
'value': neighborhood} for neighborhood in sorted(joined['Neighborhood'\
].unique())]
options[0]['label'] = 'All'
options[0]['value'] = 'All'

fig_cc = create_cc_maps(joined, 'lat', 'lon')

# --------------------------- html page layout here ----------------------------

app.layout = dbc.Container([
    # header
    dbc.Row([
        dbc.Col([
            html.Br(), 
            html.H1('Understanding Period Poverty in Chicago', 
                    style={'text-align':'center'}),
            html.P('Betty Fang, Diamon Dunlap, Ivanna Rodríguez, Jimena Salinas', 
            style={'text-align':'center'}),
        ], width=12) 
    ], align='end'),

    # ----------- intro + index map ---------------
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.P(["Period poverty is defined as “limited or inadequate access \
            to menstrual products or menstrual health education as a result of \
            financial constraints or negative socio-cultural stigmas associated \
            with menstruation.” Period poverty includes using unsanitized \
            products or using products longer than recommended - and is harmful to \
            one’s health and emotional well-being. The impacts, such such as missing \
            work or school, disproportionately affect those who are impoverished \
            or experiencing homelessness."]),
        ], width=12)
    ], align='end'),

    dbc.Row([
        dbc.Col([
            html.P(["We wanted to understand this disparity geographically in \
            Chicago, IL. We focused on factors such as income, public \
            assistance usage, number of menstruating people, percent of income \
            spent on rent, and proximity to community-based services. Using \
            these variables, we created an index at the census tract level and \
            visualized it on a map. We found that the risk of period poverty \
            was concentrated in three areas: west side, south side and far \
            south side. We also found that the number of community centers was \
            correlated with our index: areas with less access to \
            community-based services were, on average, at higher risk of \
            period poverty. From this analysis, we were able to identify \
            neighborhoods that would benefit the most from greater access to \
            free menstrual care resources."]),

            html.P(["Below is a map illustrating our resulting index for each \
            census tract in Chicago. Hover over each census tract to view the \
            index value and the neighborhood each tract is located within."])

        ], width=12) 
    ], align='end'),

    # index map
    dbc.Row([
        dbc.Col([

            html.H3('Period Poverty by Census Tract', 
            style={'text-align':'center'}),
            
            dcc.Graph(
                id='map-idx',
                figure = fig_idx)
        ], width=12)
    ], align='center'),

    # --------- community centers map text -------------
    dbc.Row([
        dbc.Col([
            html.Br(), # add space above header
            html.P(["It was important for us to incorporate existing community \
            services and commercial retailers providing period products into our \
            index. For people in need, having a community service nearby could \
            ameliorate their lack of access to period products. In order to find \
            existing resources around Chicago, we built a webscraper to compile \
            addresses of community-based services and commercial retailers, \
            and we reached out to period poverty alleviation organizations in Chicago \
            to understand the services offered and restrictions (if any) to access \
            period products."]),

            html.P(["The map below includes all the resources we scraped, including \
            the period poverty alleviation partner organizations that consented \
            to being added to the map. Select your neighborhood from the dropdown \
            menu on the left to find the resources closest to you. Click on the \
            names of different categories in the map legend on the right to filter \
            for the categories you wish to see."])

        ], width = 12, align='end') 
    ], align='end'),

    # community centers map
    dbc.Row([
        
        html.Br(),
        html.H3('Community Based Services and Commercial Retailers', 
        style={'text-align':'center'}),

        dbc.Col([
            html.Label(['Neighborhood:'], style={"margin-top":0}),
            dcc.Dropdown(
                id='neighborhood_dropdown',
                options=options,
                value=options[0]['value'],
                style={"margin-top":7}
                )
        ], width=2, align='start'),

        dbc.Col([
            dcc.Graph(
                id='map-cc',
                figure = fig_cc
                )
        ], width=10),

        html.Br()

    ], align='center'),

    # --------- scatterplot texts -------------
    dbc.Row([
        html.Br(),
        dbc.Col([
            html.P(["In the process of working on creating our period poverty \
            index and community resources and retailers map, we realized that \
            some of the Census Tracts with the highest period poverty index \
            were also some of the tracks with the least resources at walking \
            distance. The scatter plot below shows the relationship between \
            the period poverty index we calculated and the number of service \
            centers and retailers at walking distance. We see that a lot of \
            period resources are concentrated in areas with low period poverty \
            levels. Our ultimate hope is to use data to inform policymakers on \
            the areas where resources are most needed."])
        ], width=12)        
    ], align='center'),

    dbc.Row([
        
        dbc.Col([

            html.H3("Period Poverty, Services, and Commercial Retailers", 
            style={'text-align':'center'}),
            
            dcc.Graph(
                id='scatter-centers',
                figure=fig_centers_scatter
            ),
            html.Br()
        ], width=8)
    ], justify='center'),

    dbc.Row([
        html.Br(),
        dbc.Col([
            html.P(["It is especially important to consider areas with high \
            period poverty rates and large numbers of menstruating people. The \
            graph below helped us identify tracts with a high number of \
            menstruating people and low monthly disposable incomes. For instance, \
            the graph below highlights a few tracts within neighbourhoods like \
            Riverdale, Washington Park, South Deering, Chatham, Humbolt Park, \
            and Englewood, where additional resources could be greatly \
            beneficial."])
        ], width=12)        
    ], align='center'),

    dbc.Row([
        dbc.Col([

            html.H3('Menstruating People and Disposable Income', 
            style={'text-align':'center'}),
            
            dcc.Graph(
                id='scatter-pop',
                figure=fig_pop_scatter
            ),

            html.Br()
        ], width=8)

    ], justify='center'),

    # ----- conclusion text -------

    dbc.Row([
        html.Br(),
        dbc.Col([
            html.P(["While working on this project we experienced a number of \
            limitations. We found that many community organizations didn’t want \
            their addresses published for different reasons. The organizations  \
            shown in the community centers map include those publicly available \
            in Illinois Department of Human Services (IDHS), and those who \
            consented to be included."]),

            html.P(["During our research and outreach to organizations, we also \
            learned that homeless shelters, public schools and colleges/\
            universities are required by the State of Illinois to provide free \
            menstrual products. Due to capacity and time constraints, we were unable to \
            include these. Additionally, including data on unhoused individuals \
            is challenging—as granular data from the census takes several \
            months to obtain, and we could not isolate the data by gender."]),

            html.P(["In summary, we used income and community center locations \
            as proxies for estimating risk for period poverty at the census \
            tract level. Initially, we expected some variation in any given \
            census tracts’ risk for period poverty based on residents’ income \
            or proximity to community-services. Instead, we found that the \
            locations of IDHS's community-based services, which serve high-need \
            or low-income populations, were lacking in areas with a high period \
            poverty index. We found these insights interesting, and we learned \
            that there is much work to be done to completely understand the \
            issue of period poverty and inform policy initiatives that aim to \
            reduce the barriers to menstrual care."]),
            html.Br()
        ], width=12)        
    ], align='center')


])

# ------------------- interactive cc map app callback --------------------------

@app.callback(
    Output('map-cc', 'figure'),
    Input('neighborhood_dropdown', 'value')
)
def update_map(neighborhood_dropdown):
    # Find the center and zoom level for the selected neighborhood

    if neighborhood_dropdown == "All":
        zoom_level = 9.4
        fig = create_cc_maps(joined, "lat", "lon")
        # Update the layout of the map with the new center and zoom level
        fig['layout']['mapbox']['center'] = {'lat': 41.8227, 'lon': -87.6014}
        fig['layout']['mapbox']['zoom'] = zoom_level
    else:
        center_lat = joined[joined['Neighborhood'] == neighborhood_dropdown\
        ]['lat'].mean()
        center_lon = joined[joined['Neighborhood'] == neighborhood_dropdown\
        ]['lon'].mean()
        zoom_level = 12
        fig = create_cc_maps(joined, "lat", "lon")
        # Update the layout of the map with the new center and zoom level
        fig['layout']['mapbox']['center'] = {'lat': center_lat, 
                                             'lon': center_lon}
        fig['layout']['mapbox']['zoom'] = zoom_level

    return fig
