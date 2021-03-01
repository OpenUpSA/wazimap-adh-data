import pandas as pd
import numpy as np
import country_converter as coco
from pandas_profiling import ProfileReport
import re

# Define file location
FILE_LOCATION = "Dataset.csv"
# USE_COLS = ['DATE', 'REGION', 'CONTAMINES', 'DECES', 'GUERIS', 'CONTAMINES_FEMME', 'CONTAMINES_HOMME', 'CONTAMINES_GENRE_NON_SPECIFIE']

# Load the CSV as a pandas dataframe, but only selected columns
df = pd.read_csv(FILE_LOCATION, delimiter=",", low_memory=False)
# , usecols=USE_COLS)
df = df.drop("Country", 1)
df = df.drop("Source", 1)
df.head()

df['Geography'] = ""

for i, row in df.iterrows():
    iso2 = row['Country code']
    iso3 = coco.convert(names=iso2, to='ISO3')
    df.at[i,'Geography'] = iso3

cases = df[["Geography", "Cases (% male)", "Cases (% female)"]]
cases = cases.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

cases['Count'].replace('%','',regex=True,inplace=True)

cases = cases.replace(to_replace ="Cases (% male)",
                 value ="Male")
cases = cases.replace(to_replace ="Cases (% female)",
                 value ="Female")

cases = cases.astype(object).replace(np.nan, 'Null')
cases.to_csv(r'./output/Gender_Cases.csv', index = False, sep=',')

deaths = df[["Geography", "Deaths (% male)", "Deaths (% female)"]]
deaths = deaths.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

deaths['Count'].replace('%','',regex=True,inplace=True)

deaths = deaths.replace(to_replace ="Deaths (% male)",
                 value ="Male")
deaths = deaths.replace(to_replace ="Deaths (% female)",
                 value ="Female")

deaths = deaths.astype(object).replace(np.nan, 'Null')
deaths.to_csv(r'./output/Gender_Deaths.csv', index = False, sep=',')

ratio = df[["Geography", "Proportion of deaths in confirmed cases (Male:female ratio)"]]
ratio = ratio.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

ratio = ratio.replace(to_replace ="Proportion of deaths in confirmed cases (Male:female ratio)",
                 value ="Male:female ratio")

ratio = ratio.astype(object).replace(np.nan, 'Null')
ratio.to_csv(r'./output/Gender_Ratio.csv', index = False, sep=',')
