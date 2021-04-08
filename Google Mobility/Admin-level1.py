#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pandas_profiling import ProfileReport
import country_converter as coco
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# In[2]:


# Define file location
FILE_LOCATION = "Global_Mobility_Report.csv"

# Load the Citizen CSV as a pandas dataframe, but only selected columns
df = pd.read_csv(FILE_LOCATION, delimiter=",", low_memory=False)
# , usecols=USE_COLS_POPULATION
df['date'] = pd.to_datetime(df['date'], errors='coerce', format= '%Y-%m-%d')
df = df.drop("sub_region_2", 1)
df = df.drop("metro_area", 1)
df = df.drop("iso_3166_2_code", 1)
df = df.drop("census_fips_code", 1)

# Loading Africa Admin Level 1 boundaries
FILE_LOCATION = "africa_admin1.csv"

admin = pd.read_csv(FILE_LOCATION, delimiter=",")
admin = admin.rename(columns={'parent_cod': 'ISO_3'}) 


# In[3]:


df = (df.groupby([pd.Grouper(key='date', freq='MS'), 'country_region_code', 'sub_region_1'])['retail_and_recreation_percent_change_from_baseline', 
                                                    'grocery_and_pharmacy_percent_change_from_baseline', 'parks_percent_change_from_baseline', 
                                                    'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 
                                                    'residential_percent_change_from_baseline'].mean().reset_index())
df['date']= df['date'].dt.strftime('%b %Y')


# In[4]:


# This takes some time to execute

africa = ["DZ", "AO", "BW", "BI", "CM", "CV", "CF", "TD", "KM", "YT", "CG", "CD", "BJ", "GQ", "ET", "ER", "DJ", "GA", "GM", "GH", "GN", "CI", "KE", "LS", "LR", "LY", 
          "MG", "MW", "ML", "MR", "MU", "MA", "MZ", "NA", "NE", "NG", "GW", "RE", "RW", "SH", "ST", "SN", "SC", "SL", "SO", "ZA", "ZW", "SS", "EH", "SD", "SZ", "TG", 
          "TN", "UG", "EG", "TZ", "BF", "ZM"]
df = df[df["country_region_code"].isin(africa)]

df['iso3'] = ""

for i, row in df.iterrows():
    iso2 = row['country_region_code']
    iso3 = coco.convert(names=iso2, to='ISO3')
    df.at[i,'iso3'] = iso3


# In[5]:


admin = admin.rename(columns={'ISO_3': 'iso3'}) 

# Extract Africa Admin1 areas from Google Mobility data
merged_df = df.merge(admin, on='iso3')
merged_df['fuzzy_ratio'] = merged_df.apply(lambda row: fuzz.ratio(row['sub_region_1'], row['name']), axis=1)

mask = (merged_df['fuzzy_ratio']>80)
gm = merged_df[mask]
gm = gm.drop("country_region_code", 1)
gm = gm.drop("sub_region_1", 1)
gm = gm.drop("iso3", 1)
gm = gm.drop("name", 1)
gm = gm.drop("area", 1)
gm = gm.drop("fuzzy_ratio", 1)


# In[6]:


gm = gm.melt(id_vars=["date", "code"], 
        var_name="Indicator", 
        value_name="Count")
gm = gm[gm['Count'].notna()]


# In[7]:


gm = gm.rename({'code': 'Geography', 'date': 'Date'}, axis=1) 

retail = gm[gm['Indicator'] == "retail_and_recreation_percent_change_from_baseline"]
grocery = gm[gm['Indicator'] == "grocery_and_pharmacy_percent_change_from_baseline"]
parks = gm[gm['Indicator'] == "parks_percent_change_from_baseline"]
transit = gm[gm['Indicator'] == "transit_stations_percent_change_from_baseline"]
workplaces = gm[gm['Indicator'] == "workplaces_percent_change_from_baseline"]
residential = gm[gm['Indicator'] == "residential_percent_change_from_baseline"]

retail = retail.drop("Indicator", 1)
grocery = grocery.drop("Indicator", 1)
parks = parks.drop("Indicator", 1)
transit = transit.drop("Indicator", 1)
workplaces = workplaces.drop("Indicator", 1)
residential = residential.drop("Indicator", 1)

retail.to_csv(r'retail_subnational.csv', index = False, sep=',')
grocery.to_csv(r'grocery_subnational.csv', index = False, sep=',')
parks.to_csv(r'parks_subnational.csv', index = False, sep=',')
transit.to_csv(r'transit_subnational.csv', index = False, sep=',')
workplaces.to_csv(r'workplaces_subnational.csv', index = False, sep=',')
residential.to_csv(r'residential_subnational.csv', index = False, sep=',')


# In[ ]:




