import pandas as pd
import csv
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from os.path import exists
import json


# This code is used to combine the Json of solar installation sizes into a total sq footage
def combine_counts(solar_size_json):
    counts = []
    for zip in solar_size_json:
        count = 0
        if type(zip) == str:
            lzip = json.loads(zip)
            for elem in lzip:
                count += elem[0] * elem[1]
        counts.append(count)

    return counts

# Loads Solar data for given zipcodes, also cleans and calculates new values
def load_solar_dat(zip_codes, load_dir="/Clean_Data/census_zip_usable.csv"):

    if exists(load_dir):
        return pd.read_csv(load_dir)

    zip_codes = list(map(int, zip_codes))
    # df = pd.read_csv('solar_zip_usable.csv')
    df = pd.read_csv('../Proj_sunroof_scraping/Data/solar_by_zip.csv')
    df = df[df["region_name"].isin(zip_codes)]
    df = df.drop_duplicates(subset=['region_name'], keep='first')
    df = df[['yearly_sunlight_kwh_kw_threshold_avg','number_of_panels_total','install_size_kw_buckets_json','existing_installs_count','percent_covered']]
    solar_size_json = df['install_size_kw_buckets_json']
    counts = combine_counts(solar_size_json.values)
    df['square_footage'] = counts
    df['number_of_panels_total'] * (100/ df['percent_covered']) 
    df['square_footage'] * (100/ df['percent_covered']) 
    df['solar_potential'] = df['square_footage'] * df['yearly_sunlight_kwh_kw_threshold_avg']
    
    df.to_csv("solar_zip_usable.csv", index=False)

    return df

# Loads Cenus data for given zipcodes, also cleans and calculates new values
def load_census_dat(zip_codes, load_dir="/Clean_Data/solar_zip_usable.csv"):

    if exists(load_dir):
        return pd.read_csv(load_dir)

    zip_codes = list(map(int, zip_codes))
    df = pd.read_csv('../Proj_sunroof_scraping/Data/census_by_zip.csv')
    df = df[df["zip code tabulation area"].isin(zip_codes)]

    mask = df['Median_income'] <= 0
    df = df[~mask]

    a_mask = df['asian_households'] / df['total_households'] > 0.5
    df['asian_households']  = df['asian_households'] * a_mask * (1/100)

    df = df.drop_duplicates(subset=['zip code tabulation area'], keep='first')
    df.to_csv("census_zip_usable.csv", index=False)
    return df

print("Loading Data")

# Loads Zip Codes from Data Folder
zips = pd.read_csv('../Proj_sunroof_scraping/Data/zips.csv',dtype=str)
zips = zips.drop_duplicates(subset=['zips'], keep='first')
zip_codes = zips['zips'].values

print("number of zip codes:", len(zip_codes))
solar_df = load_solar_dat(zip_codes)
print("number of zip codes with solar data:", len(solar_df))
census_df = load_census_dat(zip_codes)
print("number of zip codes with census data:", len(census_df))

solar_df['solar_potential_per_capita'] = solar_df['solar_potential'] / census_df['Total_Population']
solar_df.to_csv("solar_zip_usable.csv", index=False)

print("Plotting")


import pandas as pd
import matplotlib.pyplot as plt
import pgeocode
import geopandas as gpd
from shapely.geometry import Point
from geopandas import GeoDataFrame
import plotly.graph_objects as go

nomi = pgeocode.Nominatim('us')

scl = [0,"rgb(150,0,90)"],[0.125,"rgb(0, 0, 200)"],[0.25,"rgb(0, 25, 255)"],\
[0.375,"rgb(0, 152, 255)"],[0.5,"rgb(44, 255, 150)"],[0.625,"rgb(151, 255, 0)"],\
[0.75,"rgb(255, 234, 0)"],[0.875,"rgb(255, 111, 0)"],[1,"rgb(255, 0, 0)"]

Hot_color_scale = ["rgb(255, 0, 0)","rgb(255, 111, 0)","rgb(255, 234, 0)","rgb(151, 255, 0)","rgb(44, 255, 150)","rgb(0, 152, 255)","rgb(0, 25, 255)","rgb(0, 0, 200)","rgb(150,0,90)"]
scl =["rgb(150,0,90)","rgb(0, 0, 200)","rgb(0, 25, 255)","rgb(0, 152, 255)","rgb(44, 255, 150)","rgb(151, 255, 0)","rgb(255, 234, 0)","rgb(255, 111, 0)","rgb(255, 0, 0)"]

# color scales : "hot", "deep", 'rainbow'    ## Add _r to reverse

'''
Full list:
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

def scatter_plot(x, y, xlabel, ylabel, title=None):

    dat = pd.DataFrame()
    dat['x'] = x
    dat['y'] = y
    dat = dat.dropna(axis=0)

    plt.scatter(dat['x'], dat['y'])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if title is None:
        plt.title(ylabel + " versus " + xlabel)
    else:
        plt.title(title)
    plt.show()

def geo_plot(dat, color_scale, title, edf=None, zipcodes=None):

    if edf is None:
        if zipcodes is None:
            print("invalid Geo Plotting, you must include an EDF or zipcode list")
            return -1
        else:
            edf = pd.DataFrame()
            edf['Latitude'] = (nomi.query_postal_code(zip_codes).latitude)
            edf['Longitude'] = (nomi.query_postal_code(zip_codes).longitude)
            edf['zip_code'] = zip_codes

    dat_range = max(dat) - min(dat)
    edf['dat'] = dat
    clean_dat = edf.dropna(axis=0)

    fig = go.Figure(data=go.Scattergeo(
            lon = clean_dat['Longitude'],
            lat = clean_dat['Latitude'],
            mode = 'markers',
            marker = dict(
            color = clean_dat['dat'],
            colorscale = color_scale,
            reversescale = True,
            opacity = 0.6,
            size = 10,
            colorbar = dict(
                titleside = "right",
                outlinecolor = "rgba(68, 68, 68, 0)",
                ticks = "outside",
                showticksuffix = "last",
                dtick = dat_range/15
            )
            )))

    fig.update_layout(
            title = title,
            geo_scope='usa',
        )
    fig.show()



asian_prop = (census_df['asian_households'].values / census_df['total_households'].values + 0.001)
log_solar_pot = np.log((solar_df['solar_potential_per_capita'].values + 0.001))
log_solar_util = np.log((solar_df['solar_potential_per_capita'].values * solar_df['existing_installs_count']) + 0.001)

edf = pd.DataFrame()
edf['Latitude'] = (nomi.query_postal_code(zip_codes).latitude)
edf['Longitude'] = (nomi.query_postal_code(zip_codes).longitude)
edf['zip_code'] = zip_codes

geo_plot(log_solar_pot,'hot', "log solar potential per capita", edf)
geo_plot(census_df['Median_income'], 'mint', "Median income", edf)
geo_plot(log_solar_util,'hot', "log solar utilization", edf)
geo_plot(np.log(asian_prop),'rainbow', "Log Asian Household Proportion", edf)

scatter_plot(asian_prop, solar_df['solar_potential_per_capita'].values, xlabel="Proportional of household which are asian", ylabel="Solar Potential Per Capita")
scatter_plot(census_df['Median_income'], solar_df['solar_potential_per_capita'].values, xlabel="Median Income", ylabel="Solar Potential Per Capita")
scatter_plot(census_df['House_heating_fuel'], solar_df['solar_potential_per_capita'].values, xlabel="House Heating Fuel", ylabel="Solar Potential Per Capita")


