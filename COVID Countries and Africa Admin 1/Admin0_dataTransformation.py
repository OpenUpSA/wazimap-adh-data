import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport

# Loading Johns Hopkins University data
FILE_LOCATION_CSSE_CASES = "./owid/owid-covid-data.csv"
USE_COLS = ['iso_code', 'continent', 'date', 'new_cases', 'new_deaths']

owid = pd.read_csv(FILE_LOCATION_CSSE_CASES, delimiter=",", usecols=USE_COLS)

owid = owid.rename(columns={'iso_code': 'Geography', 'date': 'Date', 'new_cases': 'Cases', 'new_deaths': 'Deaths'})
owid['Date'] = pd.to_datetime(owid['Date'], errors='coerce')

# Create df with the continent information
continent_covid = owid
continent_covid['Date'] = pd.to_datetime(continent_covid['Date'], errors='coerce')

continent_cases = continent_covid.groupby(['continent', 'Date'])['Cases'].agg(['sum'])
continent_deaths = continent_covid.groupby(['continent', 'Date'])['Deaths'].agg(['sum'])

continent_cases = continent_cases.reset_index()
continent_deaths = continent_deaths.reset_index()

continent_cases = continent_cases.rename(columns={'continent': 'Geography', 'sum': 'Cases'})
continent_deaths = continent_deaths.rename(columns={'continent': 'Geography', 'sum': 'Deaths'})

continent_cmb = pd.merge(continent_cases, continent_deaths, how='left', on=['Date','Geography'])

column_names = ["Date", "Geography", "Cases", "Deaths"]
continent_cmb = continent_cmb.reindex(columns=column_names)

continent_cmb.to_csv(r'./output/Continents_Daily.csv', index = False, sep=',')

owid = owid.drop("continent", 1)

column_names = ["Date", "Geography", "Cases", "Deaths"]
owid = owid.reindex(columns=column_names)

owid.to_csv(r'./output/Global_Admin0_Daily.csv', index = False, sep=',')
