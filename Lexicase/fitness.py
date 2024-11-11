import pandas as pd
import numpy as np

'''
OBJECTIVES:
From census_zip_usable.csv:
- Racial Equity = white_population/(black_population + white_population + asian_population + native_population)
- Income Equity = per_capita_income
From solar_zip_usable.csv:
- Energy Generation = yearly_sunlight_kwh_kw_threshold_avg
- Carbon Offset = carbon_offset_metric_tons
- Geographic Equity = percent_covered

Fitness scores are determined by the ranking of each zip code in each category.
the returned array will be n x 5, where n is the number of zip codes.
'''

def calculate_fitness(census_file_path, solar_file_path):
    """
    Calculate fitness scores for zip codes based on multiple equity and environmental metrics.
    
    Parameters:
    census_file_path (str): Path to census_zip_usable.csv
    solar_file_path (str): Path to solar_zip_usable.csv
    
    Returns:
    numpy.ndarray: Array of shape (n, 5) containing fitness scores for each zip code
    pandas.DataFrame: DataFrame with zip codes and their corresponding scores
    """
    # Read the data files
    census_df = pd.read_csv(census_file_path)
    solar_df = pd.read_csv(solar_file_path)
    
    # Rename zip code columns for merging
    census_df = census_df.rename(columns={'zcta': 'zip_code'})
    solar_df = solar_df.rename(columns={'region_name': 'zip_code'})
    
    # Merge datasets
    merged_df = pd.merge(census_df, solar_df, on='zip_code', how='inner')
    
    # Calculate Racial Equity
    merged_df['racial_equity'] = merged_df['white_population'] / (
        merged_df['black_population'] + 
        merged_df['white_population'] + 
        merged_df['asian_population'] + 
        merged_df['native_population']
    )
    
    # Create dictionary of metrics and their corresponding columns
    metrics = {
        'racial_equity': 'racial_equity',
        'income_equity': 'per_capita_income',
        'energy_generation': 'yearly_sunlight_kwh_kw_threshold_avg',
        'carbon_offset': 'carbon_offset_metric_tons',
        'geographic_equity': 'percent_covered'
    }
    
    # Calculate rankings for each metric
    rankings = pd.DataFrame(index=merged_df.index)
    rankings['zip_code'] = merged_df['zip_code']
    
    for metric_name, column_name in metrics.items():
        # Rank values (smaller rank = better score)
        rankings[metric_name] = merged_df[column_name].rank(method='min')
        
        # Normalize rankings to [0, 1] range
        rankings[metric_name] = (rankings[metric_name] - 1) / (len(rankings) - 1)
        
        # Invert scores so that 1 is best and 0 is worst
        rankings[metric_name] = 1 - rankings[metric_name]
    
    # Create output array
    fitness_scores = rankings[[
        'racial_equity', 
        'income_equity', 
        'energy_generation', 
        'carbon_offset', 
        'geographic_equity'
    ]].values
    
    return fitness_scores, rankings