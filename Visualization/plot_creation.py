from plot_util import *
from data_load_util import *

scl = [0,"rgb(150,0,90)"],[0.125,"rgb(0, 0, 200)"],[0.25,"rgb(0, 25, 255)"],\
[0.375,"rgb(0, 152, 255)"],[0.5,"rgb(44, 255, 150)"],[0.625,"rgb(151, 255, 0)"],\
[0.75,"rgb(255, 234, 0)"],[0.875,"rgb(255, 111, 0)"],[1,"rgb(255, 0, 0)"]

Hot_color_scale = ["rgb(255, 0, 0)","rgb(255, 111, 0)","rgb(255, 234, 0)","rgb(151, 255, 0)","rgb(44, 255, 150)","rgb(0, 152, 255)","rgb(0, 25, 255)","rgb(0, 0, 200)","rgb(150,0,90)"]
scl =["rgb(150,0,90)","rgb(0, 0, 200)","rgb(0, 25, 255)","rgb(0, 152, 255)","rgb(44, 255, 150)","rgb(151, 255, 0)","rgb(255, 234, 0)","rgb(255, 111, 0)","rgb(255, 0, 0)"]

# color scales : "hot", "deep", 'rainbow'    ## Add _r to reverse

'''
Full list of color scales:
'aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
'ylorrd'
'''

zip_codes, solar_df, census_df, pos_df = load_data()

combined_df = pd.concat([solar_df, census_df, pos_df], axis=1)

print("Plotting")

# Remove outliers for carbon offset (4 outliers in this case)
mask = combined_df['carbon_offset_metric_tons'] < 1000000
combined_df = combined_df[mask]

# Removing outliers for existing install counts (~90)
mask = combined_df['existing_installs_count'] < 1000
combined_df = combined_df[mask]

# Current working metric of "solar utilization", should be ~ current carbon offset
combined_df['solar_utilization'] = (combined_df['existing_installs_count'] / combined_df['count_qualified']) * combined_df['carbon_offset_metric_tons']

asian_prop = (combined_df['asian_population'].values / combined_df['Total_Population'].values)
white_prop = (combined_df['white_population'].values / combined_df['Total_Population'].values)
black_prop = (combined_df['black_population'].values / combined_df['Total_Population'].values)

combined_df['asian_prop'] = asian_prop 
combined_df['white_prop'] = white_prop 
combined_df['black_prop'] = black_prop


# log_solar_pot = np.log((solar_df['solar_potential_per_capita'].values + 0.001))
# log_solar_util = np.log((solar_df['solar_potential_per_capita'].values * solar_df['existing_installs_count']) + 0.001)

# geo_plot(log_solar_pot,'hot', "log solar potential per capita", pos_df)
# geo_plot(census_df['Median_income'], 'mint', "Median income", pos_df)
# geo_plot(log_solar_util,'hot', "log solar utilization", pos_df)
# geo_plot(np.log(asian_prop),'rainbow', "Log Asian Population Proportion", pos_df)
# geo_plot(white_prop,'rainbow', "Log White Population Proportion", pos_df)
# geo_plot(np.log(black_prop),'rainbow', "Log Black Population Proportion", pos_df)
# geo_plot(combined_df['carbon_offset_metric_tons'] ,'rainbow', "Carbon offset", pos_df)
# geo_plot(np.log((combined_df['carbon_offset_metric_tons']/ combined_df['Total_Population'].values) + 0.001) ,'rainbow', "Log Carbon offset per capita", pos_df)
# geo_plot(combined_df['percent_covered'] ,'rainbow', "Carbon offset", pos_df)
# geo_plot(combined_df['existing_installs_count'] ,'rainbow', "Existing Install count", pos_df)


# Xs = [(asian_prop, "Proportional of people which are asian"), (white_prop, "Proportional of people which are white"), (black_prop, "Proportional of people which are black"), (census_df['Median_income'].values, "Median Income")]
# Ys = [(np.log(solar_df['solar_potential_per_capita'].values), "Log Solar Potential Per Capita"), ((solar_df['carbon_offset_metric_tons']/ census_df['Total_Population'].values), "Carbon Offset if all panels built (metric tons) per capita")]

# for x, xname in Xs:
#     for y, yname in Ys:
#         scatter_plot(x, y, xlabel=xname, ylabel=yname, fit=[1,5,10])

for key in ['solar_utilization', 'carbon_offset_metric_tons', 'Median_income']:
    state_stats = stats_for_states(combined_df, key)
    plot_state_stats(state_stats, key)

pop_bins_quartile = quartile_binning(combined_df['Total_Population'].values, 'Total_Population')
white_prop_bins_quartile = quartile_binning(combined_df['white_prop'].values, 'white_prop')
asain_prop_bins_quartile = quartile_binning(combined_df['asian_prop'].values, 'asian_prop')
black_prop_bins_quartile = quartile_binning(combined_df['black_prop'].values, 'black_prop')

bins_list = [pop_bins_quartile, white_prop_bins_quartile, asain_prop_bins_quartile, black_prop_bins_quartile]
bins_list = []

for bins in bins_list:
    complex_scatter(combined_df=combined_df, x=combined_df['Median_income'].values, y=np.log(combined_df['carbon_offset_metric_tons'].values/combined_df['Total_Population'] + 1), xlabel="Median Income", ylabel="Log Carbon Offset (metric tons) per capita", title=None, bins= bins, fit=[1])
    complex_scatter(combined_df=combined_df, x=combined_df['Median_income'].values, y=np.log(combined_df['solar_utilization'].values/combined_df['Total_Population'] +1), xlabel="Median Income", ylabel="Log Log Solar Utilization per capita", title=None, bins=bins, fit=[1])
