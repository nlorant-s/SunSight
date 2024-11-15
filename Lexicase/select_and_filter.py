from fitness import calculate_fitness
from lexicase import lexicase_selection
from pathlib import Path
import pandas as pd
from pandas import DataFrame as df

def filter(selection_df, full_data, rankings_df):
    # Get the indices from the first column of selection
    indices = selection_df.iloc[:, 0].tolist()
    # Get corresponding zip codes from rankings_df using these indices
    zip_codes = rankings_df.loc[indices, 'zip_code'].tolist()
    
    # Debug
    print("\nIndices selected:")
    print(indices[:5])
    print("Corresponding zip codes:")
    print(zip_codes[:5])
    
    # Filter main DataFrame based on zip codes
    filtered_df = full_data[full_data['zip_code'].isin(zip_codes)]
    
    return filtered_df

filepath = Path("Visualization") / "Clean_Data" / "data_by_zip.csv"
full_data = pd.read_csv(filepath)

fitness_array, rankings_df = calculate_fitness(filepath)

# print("Fitness rankings:")
# print(rankings_df)

# Select the best third of zip codes based on fitness scores
selection = df(lexicase_selection(fitness_array, epsilon=False, elitism=False, num_to_select=len(fitness_array) // 3))

# print("\nSelection DataFrame head:")
# print(selection.head())
# print(selection.shape)

selected_data = filter(selection, full_data, rankings_df)