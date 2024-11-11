from fitness import calculate_fitness
from lexicase import lexicase_selection
from pathlib import Path

census_file_path = Path("Visualization") / "Clean_Data" / "census_zip_usable.csv"
solar_file_path = Path("Visualization") / "Clean_Data" / "solar_zip_usable.csv"

fitness_array, rankings_df = calculate_fitness(census_file_path, solar_file_path)

select = lexicase_selection(fitness_array, epsilon=True, elitism=False)

