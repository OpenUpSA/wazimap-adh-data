import numpy as np
from pandas_profiling import ProfileReport

# Loading Johns Hopkins University data
FILE_LOCATION_GLOBAL = "./output/Global_Admin0_Daily.csv"
FILE_LOCATION_AFRICA = "./output/Africa_Admin1_Daily.csv"
FILE_LOCATION_CONTINENTS = "./output/Continents_Daily.csv"

continents = pd.read_csv(FILE_LOCATION_CONTINENTS, delimiter=",")
admin0 = pd.read_csv(FILE_LOCATION_GLOBAL, delimiter=",")
admin1 = pd.read_csv(FILE_LOCATION_AFRICA, delimiter=",")

# Concatenate admin0 and admin1
df = [continents, admin0, admin1]
covid = pd.concat(df)
covid['Date'] = pd.to_datetime(covid['Date'], errors='coerce')

covid = covid.replace(to_replace ="OWID_AFR",
                 value ="Africa")
covid = covid.replace(to_replace ="OWID_ASI",
                 value ="Asia")
covid = covid.replace(to_replace ="OWID_EUR",
                 value ="Europe")
covid = covid.replace(to_replace ="OWID_NAM",
                 value ="North America")
covid = covid.replace(to_replace ="OWID_SAM",
                 value ="South America")
covid = covid.replace(to_replace ="OWID_OCE",
                 value ="Oceania")

# Calculate totals per monthly and transform data into wazi format
covid_monthly = (covid.groupby([pd.Grouper(key='Date', freq='MS'), 'Geography'])['Cases', 'Deaths', 'Recoveries']
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

cases_monthly.to_csv(r'./output/wazimap/cases_monthly.csv', index = False, sep=',')
deaths_monthly.to_csv(r'./output/wazimap/deaths_monthly.csv', index = False, sep=',')
recoveries_monthly.to_csv(r'./output/wazimap/recoveries_monthly.csv', index = False, sep=',')

# Calculate average per week from January 2021 and transform data into wazi format
start_date = '2021-01-01'
end_date = '2021-02-23'
mask = (covid['Date'] > start_date) & (covid['Date'] <= end_date)
covid_weekly = covid.loc[mask]

cases_weekly = covid_weekly[["Date", "Geography", "Cases"]]
cases_weekly = cases_weekly[cases_weekly['Cases'].notna()]
cases_weekly = (cases_weekly.groupby([pd.Grouper(key='Date', freq='W'), 'Geography'])['Cases']
   .sum()
   .reset_index())

cases_weekly = cases_weekly.melt(id_vars=["Geography", "Date"],
                                    var_name="Indicator",
                                    value_name="Count")

cases_weekly['Date']= cases_weekly['Date'].dt.strftime('2021-WN%U'')
cases_weekly = cases_weekly.drop("Indicator", 1)
cases_weekly.to_csv(r'./output/wazimap/cases_weekly.csv', index = False, sep=',')


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

cases_weekly.to_csv(r'./output/wazimap/cases_weekly.csv', index = False, sep=',')
deaths_weekly.to_csv(r'./output/wazimap/deaths_weekly.csv', index = False, sep=',')
recoveries_weekly.to_csv(r'./output/wazimap/recoveries_weekly.csv', index = False, sep=',')

# Calculate totals per monthly and transform data into wazi format
cases_monthly = covid[["Date", "Geography", "Cases"]]
cases_monthly = cases_monthly[cases_monthly['Cases'].notna()]
cases_monthly = (cases_monthly.groupby([pd.Grouper(key='Date', freq='MS'), 'Geography'])['Cases']
   .sum()
   .reset_index())

cases_monthly = cases_monthly.melt(id_vars=["Geography", "Date"],
                                    var_name="Indicator",
                                    value_name="Count")

cases_monthly['Date']= cases_monthly['Date'].dt.strftime('%b %Y')
cases_monthly = cases_monthly.drop("Indicator", 1)
cases_monthly.to_csv(r'./output/wazimap/cases_monthly.csv', index = False, sep=',')


deaths_monthly = covid[["Date", "Geography", "Deaths"]]
deaths_monthly = deaths_monthly[deaths_monthly['Deaths'].notna()]
deaths_monthly = (deaths_monthly.groupby([pd.Grouper(key='Date', freq='MS'), 'Geography'])['Deaths']
   .sum()
   .reset_index())

deaths_monthly = deaths_monthly.melt(id_vars=["Geography", "Date"],
                                    var_name="Indicator",
                                    value_name="Count")

deaths_monthly['Date']= deaths_monthly['Date'].dt.strftime('%b %Y')
deaths_monthly = deaths_monthly.drop("Indicator", 1)
deaths_monthly.to_csv(r'./output/wazimap/deaths_monthly.csv', index = False, sep=',')


recoveries_monthly = covid[["Date", "Geography", "Recoveries"]]
recoveries_monthly = recoveries_monthly[recoveries_monthly['Recoveries'].notna()]
recoveries_monthly = (recoveries_monthly.groupby([pd.Grouper(key='Date', freq='MS'), 'Geography'])['Recoveries']
   .sum()
   .reset_index())

recoveries_monthly = recoveries_monthly.melt(id_vars=["Geography", "Date"],
                                    var_name="Indicator",
                                    value_name="Count")

recoveries_monthly['Date']= recoveries_monthly['Date'].dt.strftime('%b %Y')
recoveries_monthly = recoveries_monthly.drop("Indicator", 1)
recoveries_monthly.to_csv(r'./output/wazimap/recoveries_monthly.csv', index = False, sep=',')
