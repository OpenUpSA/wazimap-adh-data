import pandas as pd
import glob
import numpy as np
from pandas_profiling import ProfileReport
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Loading HERA data
path = r'./hera/' # use your path
USE_COLS = ['ISO_3', 'DATE', 'REGION', 'CONTAMINES', 'DECES', 'GUERIS', 'CONTAMINES_FEMME', 'CONTAMINES_HOMME', 'CONTAMINES_GENRE_NON_SPECIFIE']

all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0, delimiter=";", usecols=USE_COLS)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

# Loading Africa Admin Level 1 boundaries
FILE_LOCATION = "africa_admin1.csv"

admin = pd.read_csv(FILE_LOCATION, delimiter=",")
admin = admin.rename(columns={'parent_cod': 'ISO_3'})

# Loading COVID19za data
FILE_LOCATION_ZA_CASES = "./covid19za/covid19za_provincial_cumulative_timeline_confirmed.csv"
FILE_LOCATION_ZA_DEATHS = "./covid19za/covid19za_provincial_cumulative_timeline_deaths.csv"
FILE_LOCATION_ZA_RECOVERIES = "./covid19za/covid19za_provincial_cumulative_timeline_recoveries.csv"

cases_za = pd.read_csv(FILE_LOCATION_ZA_CASES, delimiter=",", low_memory=False)
deaths_za = pd.read_csv(FILE_LOCATION_ZA_DEATHS, delimiter=",", low_memory=False)
recoveries_za = pd.read_csv(FILE_LOCATION_ZA_RECOVERIES, delimiter=",", low_memory=False)

# HERA - Convert text to GADM code
merged_df = frame.merge(admin, on='ISO_3')
merged_df['fuzzy_ratio'] = merged_df.apply(lambda row: fuzz.ratio(row['REGION'], row['name']), axis=1)

mask = (merged_df['fuzzy_ratio']>80)
hera = merged_df[mask]
hera

# HERA - Standardize the column names and drop unused columns
hera['DATE'] = pd.to_datetime(hera['DATE'], errors='coerce', format= '%d/%m/%Y')
hera = hera.rename(columns={'CONTAMINES': 'Cases', 'DECES': 'Deaths', 'GUERIS': 'Recoveries', 'DATE': 'Date', 'CONTAMINES_FEMME': 'Cases_Female',
                            'CONTAMINES_HOMME': 'Cases_Male', 'CONTAMINES_GENRE_NON_SPECIFIE': 'Cases_NonSpecific', 'code' : 'Geography'})

hera = hera.drop("ISO_3", 1)
hera = hera.drop("REGION", 1)
hera = hera.drop("name", 1)
hera = hera.drop("area", 1)
hera = hera.drop("fuzzy_ratio", 1)

hera_gender = hera[['Date', 'Geography', 'Cases_Female', 'Cases_Male', 'Cases_NonSpecific']]

hera = hera.drop("Cases_Female", 1)
hera = hera.drop("Cases_Male", 1)
hera = hera.drop("Cases_NonSpecific", 1)
hera['Deaths'] = pd.to_numeric(hera['Deaths'],errors='coerce')
hera.dtypes

cases_za = cases_za.rename(columns={'date': 'Date'})
deaths_za = deaths_za.rename(columns={'date': 'Date'})
recoveries_za = recoveries_za.rename(columns={'date': 'Date'})

# Basic formatting of ZA data
cases_za['Date'] = pd.to_datetime(cases_za['Date'], errors='coerce', format= '%d-%m-%Y')
deaths_za['Date'] = pd.to_datetime(deaths_za['Date'], errors='coerce', format= '%d-%m-%Y')
recoveries_za['Date'] = pd.to_datetime(recoveries_za['Date'], errors='coerce', format= '%d-%m-%Y')

cases_za = cases_za.drop("YYYYMMDD", 1)
cases_za = cases_za.drop("source", 1)
cases_za = cases_za.drop("total", 1)
deaths_za = deaths_za.drop("YYYYMMDD", 1)
deaths_za = deaths_za.drop("source", 1)
deaths_za = deaths_za.drop("total", 1)
recoveries_za = recoveries_za.drop("YYYYMMDD", 1)
recoveries_za = recoveries_za.drop("source", 1)
recoveries_za = recoveries_za.drop("total", 1)

# Convert from cumulative to daily values
cases_za['EC'] = cases_za['EC'].diff().fillna(cases_za['EC'])
cases_za['FS'] = cases_za['FS'].diff().fillna(cases_za['FS'])
cases_za['GP'] = cases_za['GP'].diff().fillna(cases_za['GP'])
cases_za['KZN'] = cases_za['KZN'].diff().fillna(cases_za['KZN'])
cases_za['LP'] = cases_za['LP'].diff().fillna(cases_za['LP'])
cases_za['MP'] = cases_za['MP'].diff().fillna(cases_za['MP'])
cases_za['NC'] = cases_za['NC'].diff().fillna(cases_za['NC'])
cases_za['NW'] = cases_za['NW'].diff().fillna(cases_za['NW'])
cases_za['WC'] = cases_za['WC'].diff().fillna(cases_za['WC'])
cases_za['UNKNOWN'] = cases_za['UNKNOWN'].diff().fillna(cases_za['UNKNOWN'])

deaths_za['EC'] = deaths_za['EC'].diff().fillna(deaths_za['EC'])
deaths_za['FS'] = deaths_za['FS'].diff().fillna(deaths_za['FS'])
deaths_za['GP'] = deaths_za['GP'].diff().fillna(deaths_za['GP'])
deaths_za['KZN'] = deaths_za['KZN'].diff().fillna(deaths_za['KZN'])
deaths_za['LP'] = deaths_za['LP'].diff().fillna(deaths_za['LP'])
deaths_za['MP'] = deaths_za['MP'].diff().fillna(deaths_za['MP'])
deaths_za['NC'] = deaths_za['NC'].diff().fillna(deaths_za['NC'])
deaths_za['NW'] = deaths_za['NW'].diff().fillna(deaths_za['NW'])
deaths_za['WC'] = deaths_za['WC'].diff().fillna(deaths_za['WC'])
deaths_za['UNKNOWN'] = deaths_za['UNKNOWN'].diff().fillna(deaths_za['UNKNOWN'])

recoveries_za['EC'] = recoveries_za['EC'].diff().fillna(recoveries_za['EC'])
recoveries_za['FS'] = recoveries_za['FS'].diff().fillna(recoveries_za['FS'])
recoveries_za['GP'] = recoveries_za['GP'].diff().fillna(recoveries_za['GP'])
recoveries_za['KZN'] = recoveries_za['KZN'].diff().fillna(recoveries_za['KZN'])
recoveries_za['LP'] = recoveries_za['LP'].diff().fillna(recoveries_za['LP'])
recoveries_za['MP'] = recoveries_za['MP'].diff().fillna(recoveries_za['MP'])
recoveries_za['NC'] = recoveries_za['NC'].diff().fillna(recoveries_za['NC'])
recoveries_za['NW'] = recoveries_za['NW'].diff().fillna(recoveries_za['NW'])
recoveries_za['WC'] = recoveries_za['WC'].diff().fillna(recoveries_za['WC'])
recoveries_za['UNKNOWN'] = recoveries_za['UNKNOWN'].diff().fillna(recoveries_za['UNKNOWN'])

# Transform the data to fit the other formats
cases_za = cases_za.melt(id_vars=["Date"],
        var_name="Geography",
        value_name="Cases")

cases_za.dtypes

deaths_za = deaths_za.melt(id_vars=["Date"],
        var_name="Geography",
        value_name="Deaths")

recoveries_za = recoveries_za.melt(id_vars=["Date"],
        var_name="Geography",
        value_name="Recoveries")

tmp = pd.merge(cases_za, deaths_za, how='left', on=['Date','Geography'])
covid_za = pd.merge(tmp, recoveries_za, how='left', on=['Date','Geography'])

covid_za = covid_za.replace(to_replace ="GP",
                 value ="GT")
covid_za = covid_za.replace(to_replace ="LP",
                 value ="LIM")

covid_za.dtypes

# Concatenate HERA and COVID19ZA data
covid_Africa = [covid_za, hera]
covid_Africa = pd.concat(covid_Africa)
# covid_Africa = covid_Africa.astype(object).replace(np.nan, 'Null')
# covid_Africa.to_csv(r'covid_Africa.csv', index = False, sep=',')
covid_Africa.dtypes

covid_Africa.to_csv(r'./output/Africa_Admin1_Daily.csv', index = False, sep=',')
