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
mask = combined_df['carbon_offset_metric_tons'] < 100 * ( combined_df['Total_Population'])
combined_df = combined_df[mask]

# Removing outliers for existing install counts (~90)
mask = combined_df['existing_installs_count'] < 10000
combined_df = combined_df[mask]

# Removing outliers for existing install counts (~90)
mask = combined_df['existing_installs_count'] > 0
combined_df = combined_df[mask]

# Removing outliers for existing install counts (~90)
mask = combined_df['count_qualified'] > 0
combined_df = combined_df[mask]

print("zips after removing outliers:", len(combined_df))

# Current working metric of "solar utilization", should be ~ current carbon offset
combined_df['solar_utilization'] = (combined_df['existing_installs_count'] / combined_df['number_of_panels_total']) * combined_df['carbon_offset_metric_tons']
combined_df['panel_utilization'] = (combined_df['existing_installs_count'] / combined_df['total_households'])

combined_df['carbon_offset_metric_tons_per_panel'] = (combined_df['carbon_offset_metric_tons'] / combined_df['number_of_panels_total'])
combined_df['carbon_offset_metric_tons_per_capita'] = combined_df['carbon_offset_metric_tons']/ combined_df['Total_Population']

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
# geo_plot(np.log((combined_df['carbon_offset_metric_tons']/ combined_df['Total_Population'].values) + 0.001) ,'rainbow', "Log Carbon offset per capita", pos_df)
# geo_plot(combined_df['percent_covered'] ,'rainbow', "Carbon offset", pos_df)
# geo_plot(combined_df['existing_installs_count'] ,'rainbow', "Existing Install count", pos_df)


# Xs = [(asian_prop, "Proportional of people which are asian"), (white_prop, "Proportional of people which are white"), (black_prop, "Proportional of people which are black"), (census_df['Median_income'].values, "Median Income")]
# Ys = [(np.log(solar_df['solar_potential_per_capita'].values), "Log Solar Potential Per Capita"), ((solar_df['carbon_offset_metric_tons']/ census_df['Total_Population'].values), "Carbon Offset if all panels built (metric tons) per capita")]

# for x, xname in Xs:
#     for y, yname in Ys:
#         scatter_plot(x, y, xlabel=xname, ylabel=yname, fit=[1,5,10])

# for key in ['carbon_offset_metric_tons_per_panel', 'Median_income', 'solar_potential_per_capita', 'solar_utilization', 'panel_utilization']:

# # Example Geo Plot (map of us)
# geo_plot(combined_df['carbon_offset_metric_tons'] ,'rainbow', "Carbon offset", pos_df)
# geo_plot(np.log(combined_df['solar_potential_per_capita']) ,'rainbow', "Log Solar potential per capita", pos_df)

#### MAIN PLOTS FOR PAPER ############

##### INTRO PLOTS #########

# Demonstrates there is an issue of panel locations
scatter_plot(x=combined_df['carbon_offset_metric_tons'], y=combined_df['existing_installs_count'], xlabel="Potential carbon offset", ylabel="Existing Panel Count", title=None, fit=[5], log=False, color="red")

# Shows where we should put panels
# geo_plot(np.log(combined_df['carbon_offset_metric_tons_per_capita']) ,'rainbow', "Carbon offset Per Capita", pos_df)

#######################################

##### EXEMPLAR STATE CHOOSING #######

# Exemplar states carbon offset to demo why we picked them
for key in ['carbon_offset_metric_tons_per_panel', 'carbon_offset_metric_tons']:
    state_stats = stats_for_states(combined_df, key)
    plot_state_stats(state_stats, states=None, key=key, sort_by='mean')

state_energy_df = load_state_energy_dat(keys=['Clean','Fossil','Total Generation'], load=False)
energy_gen_bar_plot(state_energy_df,states=None, keys=['Clean','Fossil','Total Generation'],prop=True, sort_by="Clean")

state_energy_df = load_state_energy_dat(keys=['Solar', 'Bioenergy', 'Coal','Gas','Hydro','Nuclear','Wind', 'Other Renewables', 'Other Fossil', 'Total Generation'], load=False)
energy_gen_bar_plot(state_energy_df,states=None, keys=['Solar', 'Bioenergy', 'Coal','Gas','Hydro','Nuclear','Wind', 'Other Renewables', 'Other Fossil', 'Total Generation'],prop=True, sort_by="Solar")

exemplar_states = ['Texas', 'California', 'Mississippi', 'Delaware', 'Massachusetts', 'US Total']

##################################################


# Exemplar states carbon offset to demo why we picked them
for key in ['carbon_offset_metric_tons_per_panel', 'carbon_offset_metric_tons']:
    state_stats = stats_for_states(combined_df, key)
    plot_state_stats(state_stats, states=exemplar_states, key=key, sort_by='mean')

# Supporting plots (shows energy generation Splits)
state_energy_df = load_state_energy_dat(keys=['Clean','Fossil','Total Generation'], load=False)
energy_gen_bar_plot(state_energy_df,states=exemplar_states, keys=['Clean','Fossil','Total Generation'],prop=True, sort_by="Clean")

state_energy_df = load_state_energy_dat(keys=['Solar', 'Bioenergy', 'Coal','Gas','Hydro','Nuclear','Wind', 'Other Renewables', 'Other Fossil', 'Total Generation'], load=False)
energy_gen_bar_plot(state_energy_df,states=exemplar_states, keys=['Solar', 'Bioenergy', 'Coal','Gas','Hydro','Nuclear','Wind', 'Other Renewables', 'Other Fossil', 'Total Generation'],prop=True, sort_by="Solar")


################# END OF VERY IMPORTANT PLOTS ######################################################3

# Scatter Plot exmple

# scatter_plot(x=combined_df['households_below_poverty_line'].values, y=np.log(combined_df['panel_utilization']), xlabel="Percent below poverty line", ylabel="panel utilization", title=None,fit=[1])
# scatter_plot(x=combined_df['black_prop'], y=combined_df['Median_income'], xlabel="Black proportion of pop", ylabel='Median Income', fit=[1])

# scatter_plot(x=combined_df['carbon_offset_metric_tons_per_capita'], y=np.log(combined_df['Median_income']), xlabel="Carbon Offset per capita", ylabel='Log Median Income', fit=[2])
# scatter_plot(x=combined_df['households_below_poverty_line'], y=np.log(combined_df['Median_income']), xlabel="Households below poverty line", ylabel='Log Median Income', fit=[2])


# Complex scatter plot example with separation for total pop and racial proportions separated by quartiles:
# This section just sets up the bins for each
pop_bins_quartile = quartile_binning(combined_df['Total_Population'].values, 'Total_Population')
white_prop_bins_quartile = quartile_binning(combined_df['white_prop'].values, 'white_prop')
asain_prop_bins_quartile = quartile_binning(combined_df['asian_prop'].values, 'asian_prop')
black_prop_bins_quartile = quartile_binning(combined_df['black_prop'].values, 'black_prop')
income_bins_quartile = quartile_binning(combined_df['Median_income'].values, 'Median_income')

# carbon_offset_outlier_removal = [('carbon_offset_metric_tons_per_capita', (0.01, 200), "carbon offset per capita below 200 and above 0", 'blue')]

# Because we want to run over each one of these binnings we concat them
bins_list = [pop_bins_quartile, white_prop_bins_quartile, asain_prop_bins_quartile, black_prop_bins_quartile, income_bins_quartile]

# Then run them together (fit here is 1 giving a linear fit)
# for bins in bins_list:
#     complex_scatter(combined_df=combined_df, x=combined_df['carbon_offset_metric_tons'], y=combined_df['existing_installs_count'], xlabel="Potential carbon offset (Metric Tons)", ylabel="Existing Installed Panels", title=None, bins=bins, fit=[5])
#     complex_scatter(combined_df=combined_df, x=combined_df['households_below_poverty_line'].values, y=np.log(combined_df['panel_utilization']), xlabel="Percent below poverty line", ylabel="log panel utilization", title=None, bins= bins, fit=[1])
#     # complex_scatter(combined_df=combined_df, x=combined_df['households_below_poverty_line'].values, y=np.log(combined_df['solar_utilization'].values/combined_df['Total_Population'] +1), xlabel="Percent below pverty line", ylabel="Log Log Solar Utilization per capita", title=None, bins=bins, fit=[1])
