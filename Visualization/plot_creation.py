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

# zip_codes, solar_df, census_df, pos_df = load_data()

# print("Plotting")

# asian_prop = (census_df['asian_population'].values / census_df['Total_Population'].values + 0.001)
# white_prop = (census_df['white_population'].values / census_df['Total_Population'].values + 0.001)
# black_prop = (census_df['black_population'].values / census_df['Total_Population'].values + 0.001)
# log_solar_pot = np.log((solar_df['solar_potential_per_capita'].values + 0.001))
# log_solar_util = np.log((solar_df['solar_potential_per_capita'].values * solar_df['existing_installs_count']) + 0.001)

# geo_plot(log_solar_pot,'hot', "log solar potential per capita", pos_df)
# geo_plot(census_df['Median_income'], 'mint', "Median income", pos_df)
# geo_plot(log_solar_util,'hot', "log solar utilization", pos_df)
# geo_plot(np.log(asian_prop),'rainbow', "Log Asian Population Proportion", pos_df)
# geo_plot(np.log(white_prop),'rainbow', "Log White Population Proportion", pos_df)
# geo_plot(np.log(black_prop),'rainbow', "Log Black Population Proportion", pos_df)

# scatter_plot(asian_prop, solar_df['solar_potential_per_capita'].values, xlabel="Proportional of people which are asian", ylabel="Solar Potential Per Capita")
# scatter_plot(white_prop, solar_df['solar_potential_per_capita'].values, xlabel="Proportional of people which are white", ylabel="Solar Potential Per Capita")
# scatter_plot(black_prop, solar_df['solar_potential_per_capita'].values, xlabel="Proportional of people which are black", ylabel="Solar Potential Per Capita")
# scatter_plot(census_df['Median_income'], solar_df['solar_potential_per_capita'].values, xlabel="Median Income", ylabel="Solar Potential Per Capita")

census_df = df = pd.read_csv('../Proj_sunroof_scraping/Data/census_by_zip.csv')

zips = list(census_df['place'])
output = [str(x) for x in zips]
zips = output
print(zips)

asian_pop = census_df['asian_population'].values
print(sum(asian_pop))

geo_plot(census_df['asian_population'].values,'piyg', "asian pop", edf=None, zipcodes=zips)
