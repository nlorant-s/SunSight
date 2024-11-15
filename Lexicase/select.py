from fitness import calculate_fitness
from lexicase import lexicase_selection
from pathlib import Path
import pandas as pd
from pandas import DataFrame as df

filepath = Path("Visualization") / "Clean_Data" / "data_by_zip.csv"
full_data = pd.read_csv(filepath)

fitness_array, rankings_df = calculate_fitness(filepath)

# Select the best third of zip codes based on fitness scores
selection = df(lexicase_selection(fitness_array, epsilon=False, elitism=False, num_to_select=len(fitness_array) // 3))
