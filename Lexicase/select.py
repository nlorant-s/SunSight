from fitness import calculate_fitness
from lexicase import lexicase_selection
from pathlib import Path

filepath = Path("Visualization") / "Clean_Data" / "data_by_zip.csv"

fitness_array, rankings_df = calculate_fitness(filepath)

# Select the best third of zip codes based on fitness scores
select = lexicase_selection(fitness_array, epsilon=False, elitism=False, num_to_select=len(fitness_array)//3)

print(select)