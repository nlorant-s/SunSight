import pandas as pd
import numpy as np

'''
OBJECTIVES:
- Racial Equity = 1 - (white_population/(black_population + white_population + asian_population + native_population))
- Income Equity = per_capita_income
- Energy Generation = yearly_sunlight_kwh_kw_threshold_avg
- Carbon Offset = carbon_offset_metric_tons
- Geographic Equity = percent_covered

Fitness scores are determined by the ranking of each zip code in each category.
the returned array will be of shape (n, 5) where n is the number of zip codes.
'''

def calculate_fitness(file):
    """
    Calculate fitness scores for zip codes based on 5 metrics.
    
    Parameters:
    file (str): Path to data_by_zip.csv
    
    Returns:
    numpy.ndarray: Array of shape (n, 5) containing fitness scores for each zip code
    pandas.DataFrame: DataFrame with zip codes and their corresponding scores
    """
    
    df = pd.read_csv(file)

    # Calculate Racial Equity
    df['racial_equity'] = df['white_population']  / (
        df['black_population'] + 
        df['white_population'] + 
        df['asian_population'] + 
        df['native_population']
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
    rankings = pd.DataFrame(index=df.index)
    rankings['zip_code'] = df['zip_code']
    
    for metric_name, column_name in metrics.items():
        # Rank values (smaller rank = better score)
        rankings[metric_name] = df[column_name].rank(method='average')
        
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