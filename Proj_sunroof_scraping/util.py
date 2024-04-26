# Required Libraries
from census import Census
from us import states

import pandas as pd
import csv

from geopy.geocoders import Nominatim # For address to lat/long
from uszipcode import SearchEngine
from tqdm import tqdm


# BY BUILDING (lat/long) SOLAR DATA
def get_building_stats(lat=0,long=0,label='test',API_key=''):
    lat = 37.4450
    long = -122.1390
    link = 'https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude=' +str(lat)+'&location.longitude='+str(long)+'&requiredQuality=HIGH&key='+str(API_key)

    df = pd.read_json(link).drop('roofSegmentStats').drop('solarPanelConfigs').drop('financialAnalyses').drop('solarPanels').to_csv('Data/test/'+label+".csv")

    print(df)

# with open('../API_keys/Sunroof_API_key.txt', 'r') as file:
#     sunroof_api_key = file.read().rstrip()

#     get_building_stats(40.7410861, -73.9896298241625, API_key=sunroof_api_key)

# BY ZIP LIST SOLAR DATA
def get_solar_data_by_zips(zip_codes, save=None):

    zip_codes = list(map(int, zip_codes))
    df = pd.read_csv('Data/solar_by_zip.csv')

    df = df[df['region_name'].isin(zip_codes)]
    df = df[['yearly_sunlight_kwh_kw_threshold_avg','number_of_panels_total',]]

    if save is not None:
        df.to_csv(save+".csv", index=False)


    return df

# ONE ZIP CODE (and census object) TO CENSUS DEMO DATA
def get_census_info_with_area_code(zip_code, c):

    # Define Search engine
    search = SearchEngine()

    # Search zipcode
    zipcode = search.by_zipcode(zip_code)

    if zipcode is None:
        return None

    # extract zip code state and county details
    state_fips = zipcode.state



    # Including total population (B01003_001E), 
    # median household income (B19013_001E), 
    # and % of people below poverty level (B17001_002E)
    demographic_data = c.acs5.state_zipcode(('B01003_001E', 'B11001_001E', 'B19013_001E', 'B19301_001E', 'B17001_002E', 'B02001_005E', 'B02001_003E' ),  {'for': 'state'.format(state_fips)}, zip_code)
    # demographic_data = c.acs5.get(('NAME','B01003_001E','B19013_001E', 'B17001_002E'), {'for': 'state_zipcode(fields, state_fips, zip5)'})

    # Convert to pandas DataFrame
    df = pd.DataFrame(demographic_data)
    df = df.rename(columns={'B01003_001E': 'Total_Population','B11001_001E':'total_households', 'B19013_001E': 'Median_income','B19301_001E': 'per_capita_income', 'B17001_002E': 'households_below_poverty_line', 'B02001_003E': 'black_households','B02001_003E': 'House_heating_fuel',  'B02001_005E' : 'asian_households'})
    return df

# LIST OF ZIP CODES TO CENSUS DEMOGRAPHIC INFO
def get_census_info_by_zip_codes(code_list):
    
    # Create a census object using the stored API key
    with open('../API_keys/Census_API_key.txt', 'r') as file:
        census_api_key = file.read().rstrip()
    c = Census(census_api_key)

    df = get_census_info_with_area_code(code_list[0], c)
    for code in tqdm(code_list[1:]):
        new =  get_census_info_with_area_code(code, c)
        if new is not None:
            df = pd.concat([df, new])

    return df


def address_to_lat_long(address, geolocator=Nominatim(user_agent="Cooper Proj")):
    try:
        location = geolocator.geocode(address)
        return (location.latitude, location.longitude)
    except:
        return None

# address = "175 5th Avenue NYC"
# print(address_to_lat_long(address))  # (40.7410861, -73.9896298241625)

def get_zip_info(zip_codes, save=None):
    census_df = get_census_info_by_zip_codes(zip_codes)
    # solar_df = get_solar_data_by_zips(zip_codes)
    # combined = pd.concat([census_df, solar_df], axis=1)
    # combined['Solar_potential'] = (combined['yearly_sunlight_kwh_kw_threshold_avg'] * combined['number_of_panels_total']) / combined['Total_Population'] 

    if save is not None:
        census_df.to_csv(save+".csv", index=False)

    return census_df
    # return combined


zips = pd.read_csv('Data/new_zips.csv',dtype=str)
zip_codes = zips['zips'].values

print(len(zip_codes))

combined_df = get_solar_data_by_zips(zip_codes, save="solar_by_zip")

print(len(combined_df))





