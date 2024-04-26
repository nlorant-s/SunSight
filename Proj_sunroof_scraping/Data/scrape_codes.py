
import pandas as pd

# Load the original CSV into a DataFrame
df = pd.read_csv('../../Visualization/census_zip_usable.csv',dtype=str)
zips = df['zip code tabulation area'].str.zfill(5)
zips.to_csv('new_zips.csv', index=False)

# non_outlier_zips = df.drop(df[df.Median_income < 0].index)['zip code tabulation area']

# # Save the region name to a new CSV
# non_outlier_zips.to_csv('zips.csv', index=False)