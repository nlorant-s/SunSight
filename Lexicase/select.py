from fitness import calculate_fitness
from lexicase import lexicase_selection
from pathlib import Path
import pandas as pd
from pandas import DataFrame as df

def filter_data_by_selection(filepath, selection):
    """
    Filter the data from the CSV file based on zip codes present in the selection dataframe
    
    Parameters:
    filepath (Path): Path to the data_by_zip.csv file
    selection (pandas.DataFrame): DataFrame containing the selected zip codes
    
    Returns:
    pandas.DataFrame: Filtered dataframe containing only the selected zip codes' data
    """
    # Read the original data
    full_data = pd.read_csv(filepath)
    
    # Get the zip codes from the selection dataframe
    selected_zips = selection.iloc[:, 0].values
    
    # Filter the full data to only include rows where the zip code is in the selection
    filtered_data = full_data[full_data.iloc[:, 0].isin(selected_zips)]
    
    return filtered_data

filepath = Path("Visualization") / "Clean_Data" / "data_by_zip.csv"

fitness_array, rankings_df = calculate_fitness(filepath)

# Select the best third of zip codes based on fitness scores
selection = df(lexicase_selection(fitness_array, epsilon=False, elitism=False, num_to_select=len(fitness_array)//3))

print(selection)

selected_data = filter_data_by_selection(filepath, selection)
print(selected_data)