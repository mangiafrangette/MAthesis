import plotly.express as px
import json
import geopandas as gpd
import matplotlib.pyplot as plt


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# world.plot()

world = world[(world.pop_est > 0) & (world.name != "Antarctica")]
world['gdp_per_cap'] = world.gdp_md_est / world.pop_est
# world.plot(column='gdp_per_cap')

# plt.show()

df = px.data.gapminder().query("year==2007")
with open("geo_json_world.json", "r", encoding="utf-8") as file:
    countries = json.load(file)

world.to_csv("test_geopandas.csv", index=False, header=True)

fig = px.choropleth(world, geojson=world.geometry,
                        locations=world.index,
                    color="gdp_per_cap", # lifeExp is a column of gapminder
                    # hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
fig.show()
print(df)
