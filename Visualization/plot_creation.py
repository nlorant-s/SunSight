from plot_util import *

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

asian_prop = (census_df['asian_population'].values / census_df['Total_Population'].values)
white_prop = (census_df['white_population'].values / census_df['Total_Population'].values)
black_prop = (census_df['black_population'].values / census_df['Total_Population'].values)

census_df['asian_prop'] = asian_prop 
census_df['white_prop'] = white_prop 
census_df['black_prop'] = black_prop


log_solar_pot = np.log((solar_df['solar_potential_per_capita'].values + 0.001))
log_solar_util = np.log((solar_df['solar_potential_per_capita'].values * solar_df['existing_installs_count']) + 0.001)

# geo_plot(log_solar_pot,'hot', "log solar potential per capita", pos_df)
# geo_plot(census_df['Median_income'], 'mint', "Median income", pos_df)
# geo_plot(log_solar_util,'hot', "log solar utilization", pos_df)
# geo_plot(np.log(asian_prop),'rainbow', "Log Asian Population Proportion", pos_df)
# geo_plot(white_prop,'rainbow', "Log White Population Proportion", pos_df)
# geo_plot(np.log(black_prop),'rainbow', "Log Black Population Proportion", pos_df)
mask = combined_df['carbon_offset_metric_tons'] < 1000000
combined_df = combined_df[mask]
geo_plot(combined_df['carbon_offset_metric_tons'] ,'rainbow', "Carbon offset", pos_df)
geo_plot(np.log((combined_df['carbon_offset_metric_tons']/ combined_df['Total_Population'].values) + 0.1) ,'rainbow', "Log Carbon offset per capita", pos_df)
# geo_plot(combined_df['percent_covered'] ,'rainbow', "Carbon offset", pos_df)
# Xs = [(asian_prop, "Proportional of people which are asian"), (white_prop, "Proportional of people which are white"), (black_prop, "Proportional of people which are black"), (census_df['Median_income'].values, "Median Income")]
# Ys = [(np.log(solar_df['solar_potential_per_capita'].values), "Log Solar Potential Per Capita"), ((solar_df['carbon_offset_metric_tons']/ census_df['Total_Population'].values), "Carbon Offset if all panels built (metric tons) per capita")]

x = len(combined_df)
mask = combined_df['existing_installs_count'] < 1000
combined_df = combined_df[mask]
y = len(combined_df)

print(x- y)
geo_plot(combined_df['existing_installs_count'] ,'rainbow', "Existing Install count", pos_df)

# for x, xname in Xs:
#     for y, yname in Ys:
#         scatter_plot(x, y, xlabel=xname, ylabel=yname, fit=[1,5,10])

pop_bins = [('Total_Population', (0, 10000), "total pop < 10000", "blue"), ('Total_Population', (10000, 10000000000), "total pop > 10000", "red")]

white_prop_med = np.median(census_df['white_prop'].values)
asian_prop_med = np.median(census_df['asian_prop'].values)
black_prop_med = np.median(census_df['black_prop'].values)

white_prop_bins = [('white_prop', (0, white_prop_med), "white prop < median", "blue"), ('white_prop', (white_prop_med, 2), "white prop > median", "red")]
asian_prop_bins = [('asian_prop', (0, asian_prop_med), "asian prop < median", "blue"), ('asian_prop', (asian_prop_med, 2), "asian prop > median", "red")]
black_prop_bins = [('black_prop', (0, black_prop_med), "black prop < median", "blue"), ('black_prop', (black_prop_med, 2), "black prop > median", "red")]

# complex_scatter(census_df=census_df, solar_df=solar_df, x=np.log(solar_df['carbon_offset_metric_tons'].values + 0.001), y=np.log(solar_df['existing_installs_count'].values + 0.001), xlabel="Log Carbon Offset (metric tons)", ylabel="Log Existing install count", title=None, bins= pop_bins)
# complex_scatter(census_df=census_df, solar_df=solar_df, x=np.log(solar_df['carbon_offset_metric_tons'].values + 0.001), y=np.log(solar_df['existing_installs_count'].values + 0.001), xlabel="Log Carbon Offset (metric tons)", ylabel="Log Existing install count", title=None, bins= white_prop_bins)
# complex_scatter(census_df=census_df, solar_df=solar_df, x=np.log(solar_df['carbon_offset_metric_tons'].values + 0.001), y=np.log(solar_df['existing_installs_count'].values + 0.001), xlabel="Log Carbon Offset (metric tons)", ylabel="Log Existing install count", title=None, bins= asian_prop_bins)
# complex_scatter(census_df=census_df, solar_df=solar_df, x=np.log(solar_df['carbon_offset_metric_tons'].values + 0.001), y=np.log(solar_df['existing_installs_count'].values + 0.001), xlabel="Log Carbon Offset (metric tons)", ylabel="Log Existing install count", title=None, bins= black_prop_bins)
# scatter_plot(combined_df['percent_covered'], combined_df['carbon_offset_metric_tons'], xlabel="Percent covered by Proj sunroof", ylabel="Carbon offset pred by Proj sunroof", fit=[1])
# scatter_plot(solar_df['carbon_offset_metric_tons'].values, np.log(solar_df['existing_installs_count'].values + 0.001), xlabel="Carbon Offset (metric tons)", ylabel="existing install count", fit=[1,5])

# scatter_plot(asian_prop, solar_df['solar_potential_per_capita'].values, xlabel="Proportional of people which are asian", ylabel="Solar Potential Per Capita", fit=[1,5,10, 20])
# scatter_plot(white_prop, solar_df['solar_potential_per_capita'].values, xlabel="Proportional of people which are white", ylabel="Solar Potential Per Capita", fit=[1,5,10, 30])
# scatter_plot(black_prop, solar_df['solar_potential_per_capita'].values, xlabel="Proportional of people which are black", ylabel="Solar Potential Per Capita", fit=[1,5,10, 30])
# scatter_plot(census_df['Median_income'].values, solar_df['solar_potential_per_capita'].values, xlabel="Median Income", ylabel="Solar Potential Per Capita", fit=[1,5,10, 30])

# scatter_plot(asian_prop, solar_df['solar_potential_per_capita'].values * solar_df['existing_installs_count'], xlabel="Proportional of people which are asian", ylabel="Solar Utilization Per Capita", fit=[1,5,10, 15])
# scatter_plot(white_prop, solar_df['solar_potential_per_capita'].values * solar_df['existing_installs_count'], xlabel="Proportional of people which are white", ylabel="Solar Utilization Per Capita", fit=[1,5,10, 20])
# scatter_plot(black_prop, solar_df['solar_potential_per_capita'].values * solar_df['existing_installs_count'], xlabel="Proportional of people which are black", ylabel="Solar Utilization Per Capita", fit=[1,5,10, 20])
# scatter_plot(census_df['Median_income'].values, solar_df['solar_potential_per_capita'].values * solar_df['existing_installs_count'], xlabel="Median Income", ylabel="Solar Utilization Per Capita", fit=[1,5,10, 20])