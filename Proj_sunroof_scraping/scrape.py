import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tabulate import tabulate


df_state = pd.read_csv('https://storage.googleapis.com/project-sunroof/csv/latest/project-sunroof-state.csv')
df_city = pd.read_csv('https://storage.googleapis.com/project-sunroof/csv/latest/project-sunroof-city.csv')
df_zip = pd.read_csv('https://storage.googleapis.com/project-sunroof/csv/latest/project-sunroof-postal_code.csv')

# df_electricity = pd.read_excel('https://www.eia.gov/electricity/sales_revenue_price/xls/table5_a.xlsx', engine='xlrd')

df_state.to_csv('Data/state.csv', index=False)  
df_city.to_csv('Data/city.csv', index=False)  
df_zip.to_csv('Data/zip.csv', index=False)  


df_state.info()
df_city.info()