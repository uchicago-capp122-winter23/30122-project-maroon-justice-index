<!-- [![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9875283&assignment_repo_type=AssignmentRepo) -->

# Cook County Period Poverty Index 

### Authors: Betty Fang, Ivanna Rodríguez, Jimena Salinas, Diamon Dunlap

Period poverty is defined as “the limited or inadequate access to menstrual products or menstrual health education as a result of financial constraints or negative socio-cultural stigmas associated with menstruation.” Period poverty - such as using products longer than recommended or missing work or school due to period leaks, pain and shame - is harmful to one’s health as well as emotional well-being. Period poverty disproportionately affects those who are impoverished or experiencing homelessness. 
 
To understand this disparity geographically in Cook County, IL, we focused on factors such as income, public assistance usage, number of menstruating people, percent of income spent on rent, and proximity to community-based services. To obtain these variables, we used demographic data from the U.S Census API, webscraped services data, and personally collected community resource informatiion to create a period poverty index at the census tract level and visualize the results on a map. We found that the risk of period poverty was concentrated in three areas – west side, south side and far south side. We also found that the number of community centers was correlated with our index - areas with less access to community-based services were, on average, at higher risk of period poverty. From this analysis, we were able to identify neighborhoods that would benefit the most from greater access to free menstrual care resources.


## How to run the Dash application:

To visualize our results we built a Dash app, here are the steps to run the app:

Setting up virtual environment using poetry

Once the repo is cloned, in the root directory 30122-project-maroon-justice-index:

1.	Run *poetry install* to install the necessary packages

```python 
poetry install
```
2.	Run *poetry shell* to activate the virtual environment

```python
poetry shell
```

3.	Run *python -m ppindex* to open the webapp

```python
python -m ppindex
```

The diagram below illustrates the basic structure for our project. To collect the data we needed for our analysis we used two different tables from the American Community Survey (ACS) API, maintained by the U.S. Census Bureau, and we built a webscraper to compile the addresses for community-based services and commercial retailers. Additionally, we personally reached out to period poverty alleviation organizations in Chicago to compile a list of community resources and we asked for conscent to include these resources in our map.

Once we had our Census Tract demographic data and our service centers and retail data, we built a Python class using GeoPandas to identify the number of service centers within walking distance to the centroid of each Census Tract. This information was then incorporated into our period poverty index.

<p align="center">
  <img src="https://github.com/uchicago-capp122-spring23/30122-project-maroon-justice-index/blob/main/ppindex/assets/updated_structure.jpg" alt="GitHub Project Structure" style="display: block; margin: 0 auto;" width="500"/>
</p>



## Period Poverty Cook County Map

Below is a map illustrating our resulting index for each census tract in Chicago. In our Dash app, you can hover over each census tract to view the index value, and the neighborhood each tract is located within.

![Mapping Period Poverty across Cook County](https://github.com/uchicago-capp122-spring23/30122-project-maroon-justice-index/blob/main/ppindex/assets/map_image_new.png)


## Map of Neighbourhood Resources and Retail Centers

It was important for us to incorporate existing community services and commercial retailers providing period products into our index. For people in need, having a community service nearby could ameliorate their lack of access to period products. To find existing resources around Chicago, we built a webscraper to compile the addresses for community-based services and commercial retailers, and reached out to period poverty alleviation organizations in Chicago to understand the services offered and restrictions (if any) to access period products.

The map below includes all the resources we scraped, and the organizations that consented to being added to the map. In our Dash app, you can choose your neighborhood from the dropdown on the left to find the resources closest to you.

![Mapping Community Services and Retail Centers by Census Tract](https://github.com/uchicago-capp122-spring23/30122-project-maroon-justice-index/blob/main/ppindex/assets/community%20centers_bigger.png)


## Data Insights

In the process of working on creating our period poverty index and community resources and retailers map, we realized that some of the Census Tracts with the highest period poverty index were also some of the tracks with the least resources at walking distance. The scatter plot below shows the relationship between the period poverty index we calculated and the number of service centers and retailers at walking distance. We see that a lot of period resources are concentrated in areas with low period poverty levels. Our ultimate hope is to use data to inform policymakers on the areas where resources are most needed.

![Period Poverty, Services, and Commercial Retailers](https://github.com/uchicago-capp122-spring23/30122-project-maroon-justice-index/blob/main/ppindex/assets/income_pop.png)


It is especially important to consider areas with high period poverty rates and large numbers of menstruating people. The graph below helped us identify tracts with a high number of menstruating people and low monthly disposable incomes. For instance, the graph below highlights a few tracts within neighbourhoods like Riverdale, Washington Park, South Deering, Chatham, Humbolt Park, and Englewood, where additional resources could be greatly  beneficial.

![Menstruating People and Disposable Income](https://github.com/uchicago-capp122-spring23/30122-project-maroon-justice-index/blob/main/ppindex/assets/community_centers_index.png)



### Project Takeaways

While working through this project we experienced some limitations and made several adaptations. The first to note, an important population is missing from our index, which are those who are unhoused. We learned that in order to receive more granular data on those experiencing homelessness, we would have to apply to the Census Bureau which takes several months. The public use data does not identify those who are unhoused—they are grouped with those in group quarters such as prisons and dormitories. Unfortunately, we did not have a way to segment by the unhoused population or by gender. As a result, our index is focused on those who have fixed housing and are low-income.

Secondly, the intent of the resource map (second figure) was to create a resource for the community to use to locate affordable menstrual products and services since one does not currently exist. We later found that many community organizations did not want their addresses published. The reasoning was either the resources are only for their clients, or their centers also act as domestic violence refuges and exposing their addresses would jeopardize the safety of the people seeking their services. However, we were still able to gain consent from a small subset of organizations who distribute free menstrual products to their clients to be added to our resource map. We thank them for participating and for the work they do for the community!

During our outreach, we also learned that homeless shelters, public schools and colleges/universities are now required by the State of Illinois to provide free menstrual products. Due to complexity and time constraints we did not have the opportunity to scrape theses. We were able to scrape the Illinois Department of Health Services (IDHS) website for Women, Infant and Children offices (WIC) and other community-based services. It was mentioned that some provided resources and some do not. Therefore, we used these centers as a proxy for access within our index. In the end, we didn’t have the data to generate the exact resource map that we envisioned, but we’ve successfully depicted what our best guess of what access looks like in Cook County.

In summary, we used income-based variables and community center locations as proxies for estimating risk for period poverty at the census tract level. Before our analysis, we expected there to be variation in any given census tracts’ risk for period poverty based on whether we were factoring in residents’ income or proximity to community-services. Instead, we found that the two were largely correlated. We were surprised to find that the locations of IDHS’s community-based services, which serve high-need or low-income populations, were lacking in the areas with high concentrations of poverty because we expected there to be greater investment in the infrastructure of community-based services in these areas. Instead, the infrastructure and availability of community-based services appear to be lagging behind available data on poverty. We found these insights interesting, and we learned that there is much work to be done to completely understand the issue of period poverty and inform policy initiatives that aim to provide resources.
