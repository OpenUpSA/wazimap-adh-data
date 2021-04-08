#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd
import glob
import numpy as np
from pandas_profiling import ProfileReport
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Loading Mozambique Admin Level 1 boundaries
data = pd.read_excel ('mozambique-covid-19-cases.xlsx', engine='openpyxl') 
df = pd.DataFrame(data)
df = df.iloc[1:]

# Loading Africa Admin Level 1 boundaries
FILE_LOCATION = "africa_admin1.csv"

admin = pd.read_csv(FILE_LOCATION, delimiter=",")
admin = admin.rename(columns={'parent_cod': 'ISO_3'})


# In[28]:


# Convert text to GADM code
df['ISO_3'] = 'MOZ'

merged_df = df.merge(admin, on='ISO_3')
merged_df['fuzzy_ratio'] = merged_df.apply(lambda row: fuzz.ratio(row['Province'], row['name']), axis=1)

mask = (merged_df['fuzzy_ratio']>80)
moz = merged_df[mask]

moz = moz.drop("ISO_3", 1)
moz = moz.drop("Province", 1)
moz = moz.drop("name", 1)
moz = moz.drop("area", 1)
moz = moz.drop("fuzzy_ratio", 1)

moz = moz.rename(columns={'Positive Cases': 'Cases', 'Recovered': 'Recoveries', 'code' : 'Geography'})


# In[15]:


# Calculate totals per monthly and transform data into wazi format
covid_monthly = (moz.groupby([pd.Grouper(key='Date', freq='MS'), 'Geography'])['Cases', 'Deaths', 'Recoveries']
   .sum()
   .reset_index())

covid_monthly = covid_monthly.melt(id_vars=["Geography", "Date"], 
                                    var_name="Indicator", 
                                    value_name="Count")

covid_monthly['Date']= covid_monthly['Date'].dt.strftime('%b %Y')
# covid_monthly = covid_monthly.astype(object).replace(np.nan, 'Null')

cases_monthly = covid_monthly[covid_monthly["Indicator"].isin(['Cases'])]
deaths_monthly = covid_monthly[covid_monthly["Indicator"].isin(['Deaths'])]
recoveries_monthly = covid_monthly[covid_monthly["Indicator"].isin(['Recoveries'])]

cases_monthly = cases_monthly.drop("Indicator", 1)
deaths_monthly = deaths_monthly.drop("Indicator", 1)
recoveries_monthly = recoveries_monthly.drop("Indicator", 1)

cases_monthly = cases_monthly[cases_monthly['Count'].notna()]
deaths_monthly = deaths_monthly[deaths_monthly['Count'].notna()]
recoveries_monthly = recoveries_monthly[recoveries_monthly['Count'].notna()]

cases_monthly.to_csv(r'./output/moz_cases_monthly.csv', index = False, sep=',')
deaths_monthly.to_csv(r'./output/moz_deaths_monthly.csv', index = False, sep=',')
recoveries_monthly.to_csv(r'./output/moz_recoveries_monthly.csv', index = False, sep=',')


# In[30]:


moz['Date'] = pd.to_datetime(moz['Date'], errors='coerce')
moz['Cases'] = pd.to_numeric(moz['Cases'],errors='coerce')
moz['Deaths'] = pd.to_numeric(moz['Deaths'],errors='coerce')
moz['Recoveries'] = pd.to_numeric(moz['Recoveries'],errors='coerce')

# Calculate average per week from January 2021 and transform data into wazi format
start_date = '2021-01-01'
end_date = '2021-04-08'
mask = (moz['Date'] > start_date) & (moz['Date'] <= end_date)
covid_weekly = moz.loc[mask]

cases_weekly = covid_weekly[["Date", "Geography", "Cases"]]
cases_weekly = cases_weekly[cases_weekly['Cases'].notna()]              
cases_weekly = (cases_weekly.groupby([pd.Grouper(key='Date', freq='W'), 'Geography'])['Cases']
   .sum()
   .reset_index())

cases_weekly = cases_weekly.melt(id_vars=["Geography", "Date"], 
                                    var_name="Indicator", 
                                    value_name="Count")

cases_weekly['Date']= cases_weekly['Date'].dt.strftime('2021-WN%U')
cases_weekly = cases_weekly.drop("Indicator", 1)
cases_weekly.to_csv(r'./output/moz_cases_weekly.csv', index = False, sep=',')


                                                       
                                                       
covid_weekly = (covid_weekly.groupby([pd.Grouper(key='Date', freq='W'), 'Geography'])['Cases', 'Deaths', 'Recoveries']
   .mean().round(0)
   .reset_index())

covid_weekly = covid_weekly.melt(id_vars=["Geography", "Date"], 
                                    var_name="Indicator", 
                                    value_name="Count")

covid_weekly['Date']= covid_weekly['Date'].dt.strftime('2021-WN%U')
# covid_weekly = covid_weekly.astype(object).replace(np.nan, 'Null')

cases_weekly = covid_weekly[covid_weekly["Indicator"].isin(['Cases'])]
deaths_weekly = covid_weekly[covid_weekly["Indicator"].isin(['Deaths'])]
recoveries_weekly = covid_weekly[covid_weekly["Indicator"].isin(['Recoveries'])]

cases_weekly = cases_weekly.drop("Indicator", 1)
deaths_weekly = deaths_weekly.drop("Indicator", 1)
recoveries_weekly = recoveries_weekly.drop("Indicator", 1)

cases_weekly = cases_weekly[cases_weekly['Count'].notna()]
deaths_weekly = deaths_weekly[deaths_weekly['Count'].notna()]
recoveries_weekly = recoveries_weekly[recoveries_weekly['Count'].notna()]

cases_weekly.to_csv(r'./output/moz_cases_weekly.csv', index = False, sep=',')
deaths_weekly.to_csv(r'./output/moz_deaths_weekly.csv', index = False, sep=',')
recoveries_weekly.to_csv(r'./output/moz_recoveries_weekly.csv', index = False, sep=',')


# In[ ]:




