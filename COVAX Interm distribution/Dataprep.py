#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pandas_profiling import ProfileReport
import country_converter as coco
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# In[5]:


# Define file location
FILE_LOCATION = "COVAX Facility Interim Distribution Forecast - Data.csv"

# Load the Citizen CSV as a pandas dataframe, but only selected columns
df = pd.read_csv(FILE_LOCATION, delimiter=",", low_memory=False)
df = df.drop("WHO Region", 1)
df = df.drop("Participant", 1)


# In[6]:


df = df.melt(id_vars=["ISO3", "SFP/AMC"], 
        var_name="Indicator", 
        value_name="Count")
df = df[df['Count'].notna()]

df = df.rename(columns={'ISO3': 'Geography', 'SFP/AMC': 'COVAX Participation Status'})
df.head()


# In[8]:


df = df.replace(to_replace ="No. of doses - AZ/SII (indicative distribution)", 
                 value ="AZ/SII (indicative distribution)") 
df = df.replace(to_replace ="No. of doses – AZ/SKBio (indicative distribution)", 
                 value ="AZ/SKBio (indicative distribution)") 
df = df.replace(to_replace ="No. of doses - Pfizer-BioNTech (exceptional allocation)", 
                 value ="Pfizer-BioNTech (exceptional allocation)") 

df = df.replace(to_replace ="SFP", 
                 value ="Self Financing Participant") 
df = df.replace(to_replace ="AMC", 
                 value ="Advance Market Commitment") 

df.to_csv(r'covax_output.csv', index = False, sep=',')


# In[ ]:




