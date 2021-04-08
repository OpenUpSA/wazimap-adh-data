#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pandas_profiling import ProfileReport
import country_converter as coco
import numpy as np


# In[2]:


# Define file location
FILE_LOCATION = "Global_Mobility_Report.csv"

# Load the Citizen CSV as a pandas dataframe, but only selected columns
df = pd.read_csv(FILE_LOCATION, delimiter=",", low_memory=False)
# , usecols=USE_COLS_POPULATION
df['date'] = pd.to_datetime(df['date'], errors='coerce', format= '%Y-%m-%d')

gm = df[df['sub_region_1'].isna()]

gm = gm.drop("sub_region_1", 1)
gm = gm.drop("sub_region_2", 1)
gm = gm.drop("metro_area", 1)
gm = gm.drop("iso_3166_2_code", 1)
gm = gm.drop("census_fips_code", 1)


# In[3]:


gm = (gm.groupby([pd.Grouper(key='date', freq='MS'), 'country_region_code', 'country_region'])['retail_and_recreation_percent_change_from_baseline', 
                                                    'grocery_and_pharmacy_percent_change_from_baseline', 'parks_percent_change_from_baseline', 
                                                    'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 
                                                    'residential_percent_change_from_baseline'].mean().reset_index())
gm.head()


# In[4]:


gm['iso3'] = ""

for i, row in gm.iterrows():
    iso2 = row['country_region_code']
    iso3 = coco.convert(names=iso2, to='ISO3')
    gm.at[i,'iso3'] = iso3
    
gm.head()


# In[5]:


gm = gm.drop("country_region_code", 1)
gm = gm.drop("country_region", 1)

df2 = gm.melt(id_vars=["date", "iso3"], 
        var_name="Indicator", 
        value_name="Count")


# In[6]:


df2 = df2.rename({'iso3': 'Geography', 'date': 'Date'}, axis=1) 
df2['Date']= df2['Date'].dt.strftime('%b %Y')

retail = df2[df2['Indicator'] == "retail_and_recreation_percent_change_from_baseline"]
grocery = df2[df2['Indicator'] == "grocery_and_pharmacy_percent_change_from_baseline"]
parks = df2[df2['Indicator'] == "parks_percent_change_from_baseline"]
transit = df2[df2['Indicator'] == "transit_stations_percent_change_from_baseline"]
workplaces = df2[df2['Indicator'] == "workplaces_percent_change_from_baseline"]
residential = df2[df2['Indicator'] == "residential_percent_change_from_baseline"]


# In[7]:


retail = retail.drop("Indicator", 1)
grocery = grocery.drop("Indicator", 1)
parks = parks.drop("Indicator", 1)
transit = transit.drop("Indicator", 1)
workplaces = workplaces.drop("Indicator", 1)
residential = residential.drop("Indicator", 1)


# In[9]:


retail.to_csv(r'retail.csv', index = False, sep=',')
grocery.to_csv(r'grocery.csv', index = False, sep=',')
parks.to_csv(r'parks.csv', index = False, sep=',')
transit.to_csv(r'transit.csv', index = False, sep=',')
workplaces.to_csv(r'workplaces.csv', index = False, sep=',')
residential.to_csv(r'residential.csv', index = False, sep=',')


# In[ ]:




