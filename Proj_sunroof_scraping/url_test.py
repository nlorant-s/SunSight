from urllib.request import urlopen
import urllib
import ast
import csv
import pandas as pd



code_dict = {'B01003_001E': 'Total_Population',
                    'B11001_001E': 'total_households',
                    'B19013_001E': 'Median_income',
                    'B19301_001E': 'per_capita_income',
                    'B17001_002E': 'households_below_poverty_line', 
                    'B02001_003E': 'black_population',
                    'B02001_002E': 'white_population',  
                    'B02001_005E' : 'asian_population', 
                    'B02001_004E': 'native_population'}

# 'B01003_001E,B11001_001E,B19013_001E,B19301_001E,B17001_002E,B02001_003E,B02001_002E,B02001_005E,B02001_004E'
code_keys = str(code_dict.keys())
url = "https://api.census.gov/data/2022/acs/acs5?get="+code_keys +"&for="

ZCTA = 'zip code tabulation area'
url = url + urllib.parse.quote(ZCTA) + ":*"


url = url.replace("dict_keys(", "").replace(")", "").replace("[", "").replace("]", "").replace("'","").replace(" ","")
print(url)

f = urlopen(url)
myfile = f.read().decode("utf-8").replace("null","-1")
res = ast.literal_eval(myfile)

df = pd.DataFrame(res[1:],columns=res[0])
df.rename(columns=code_dict)
df.to_csv("test.csv", index=False)


