import pandas as pd
from os.path import exists
import numpy as np
import json
import pgeocode

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
def load_solar_dat(zip_codes, load_dir="Clean_Data/solar_zip_usable.csv"):

    # If we have already cleaned data then we load that instead of processing
    if load_dir is not None and exists(load_dir):
        return pd.read_csv(load_dir)

    zip_codes = list(map(int, zip_codes))
    # df = pd.read_csv('solar_zip_usable.csv')
    df = pd.read_csv('../Data/solar_by_zip.csv')
    df = df[df["region_name"].isin(zip_codes)]
    df = df.drop_duplicates(subset=['region_name'], keep='first')
    df = df[['region_name','state_name','yearly_sunlight_kwh_kw_threshold_avg','number_of_panels_total','install_size_kw_buckets_json','existing_installs_count','percent_covered','carbon_offset_metric_tons','count_qualified']]
    solar_size_json = df['install_size_kw_buckets_json']

    # Potential solar panels are saved as a json of different sizes, we use combine counts to get a single square-footage number of potential solar panel area
    counts = combine_counts(solar_size_json.values)
    df['square_footage'] = counts

    # We have to scale by "percent covered" as that is the percent of the zipcode area that has data, but census dat attempts to cover 100% of population
    df['number_of_panels_total'] *= (100/ df['percent_covered']) 
    df['square_footage'] *= (100/ df['percent_covered']) 
    df['carbon_offset_metric_tons'] *= (100/ df['percent_covered']) 
    df['existing_installs_count'] *= (100/ df['percent_covered']) 

    # This metric for solar potential is somewhat arbitrary, it is simply the avg amount of solar energy produced if all possibe solar panels were built
    df['solar_potential'] = df['square_footage'] * df['yearly_sunlight_kwh_kw_threshold_avg']
    
    df.to_csv("Clean_Data/solar_zip_usable.csv", index=False)

    return df

def stats_by_state(df, key, state):
    '''
    calculates the mean, std, and median of a particular coloumn of df (denoted by "key")
    does this only for rows from the given state
    '''

    df = df[df['state_name'] == state] 
    df = df[df[key].notna()]
    vals = df[key].values 
    if key in ['solar_utilization', 'carbon_offset_metric_tons','existing_install_count']:
        vals /= df['Total_Population']

    stats = {'state_name' : [state], 'mean' : [np.mean(vals)], 'std': [np.std(vals)], 'median' : [np.median(vals)]}

    return pd.DataFrame(stats)

def stats_for_states(df, key):
    '''
    Calculates the mean, std, and median of the key col of df
    outputs a df witheach row corresponding to a state and cols : mean, std, median
    '''

    print("calculating statistics of states on:", key)


    pr_mask = df['state_name'].isin(['Aguadilla', 'Arecibo', 'Dorado', 'Hormigueros', 'Moca', 'Mayagüez', 'Ponce',
    'Canóvanas', 'Corozal', 'San Juan', 'Toa Baja', 'Toa Alta', 'Bayamón', 'Cataño',
    'Guaynabo', 'Trujillo Alto', 'Carolina'])
    states = df[~pr_mask]['state_name'].unique()

    stats = stats_by_state(df, key, states[0])

    for state in states[1:]:
        stats = pd.concat([stats, stats_by_state(df, key, state)])

    stats = stats[stats['mean'] != 0]

    return stats

# Loads Cenus data for given zipcodes, also cleans and calculates new values
def load_census_dat(zip_codes, load_dir="Clean_Data/census_zip_usable.csv"):

    # If we have already cleaned data then we load that instead of processing
    if load_dir is not None and exists(load_dir):
        return pd.read_csv(load_dir)

    zip_codes = list(map(int, zip_codes))
    df = pd.read_csv('../Data/census_by_zip.csv')
    df = df[df["zcta"].isin(zip_codes)]

    # Removes bad data, should be already removed from the zip.csv, but this to be certain.
    mask = df['Median_income'] <= 0
    df = df[~mask]

    # Also removes duplicates (which happen for some reason even when there are no duplicates in zips)
    df = df.drop_duplicates(subset=['zcta'], keep='first')
    df = df.sort_values('zcta')
    df.to_csv("Clean_Data/census_zip_usable.csv", index=False)

    return df

def get_clean_zips():
    if exists("Clean_Data/zips_usable.csv"):
        zips = pd.read_csv('Clean_Data/zips_usable.csv',dtype=str) 
        zips = zips.drop_duplicates(subset=['zcta'], keep='first')
        return zips['zcta'].values
    else:
        zips = pd.read_csv('../Data/zips.csv',dtype=str) 
        zips = zips.drop_duplicates(subset=['zcta'], keep='first')
        zip_codes = zips['zcta'].values
        solar_df = load_solar_dat(zip_codes)
        census_df = load_census_dat(zip_codes, None)

        # Remove all zips not in solar data
        z_temp = zips[zips['zcta'].isin( solar_df['region_name'].astype(str).str.zfill(5))]
        # Remove all zips not in census data (including median income outliers)
        z_temp2 = z_temp[z_temp['zcta'].isin(census_df['zcta'].astype(str).str.zfill(5))]

        # Save this new zip list
        z_temp2.to_csv("Clean_Data/zips_usable.csv", index=False)

        return z_temp2['zcta'].values
    


# Loads both the census and solar data across all zips and returns both dfs, it is necessary to have already created the solar_by_zip and census_by_zip data under the Data folder though
def load_data():
    print("Loading Data")
    # Loads Zip Codes from Data Folder
    # zips = pd.read_csv('../Data/zips.csv',dtype=str) 
    # zips = zips.drop_duplicates(subset=['zcta'], keep='first')
    # zip_codes = zips['zcta'].values

    zip_codes = get_clean_zips() 

    print("number of zip codes:", len(zip_codes))
    solar_df = load_solar_dat(zip_codes)
    print("number of zip codes with solar data:", len(solar_df))
    census_df = load_census_dat(zip_codes)
    print("number of zip codes with census data:", len(census_df))

    solar_df['solar_potential_per_capita'] = solar_df['solar_potential'] / census_df['Total_Population']
    solar_df = solar_df.sort_values('region_name')
    solar_df.to_csv("Clean_Data/solar_zip_usable.csv", index=False)

    nomi = pgeocode.Nominatim('us')

    edf = pd.DataFrame()
    edf['Latitude'] = (nomi.query_postal_code(zip_codes).latitude)
    edf['Longitude'] = (nomi.query_postal_code(zip_codes).longitude)
    edf['zip_code'] = zip_codes

    return zip_codes, solar_df, census_df, edf