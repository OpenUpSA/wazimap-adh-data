import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport

# Define file location
FILE_LOCATION = "owid-covid-data.csv"
USE_COLS_POPULATION = ['iso_code', 'continent', 'date', 'stringency_index', 'population', 'population_density', 'median_age', 'aged_65_older', 'aged_70_older', 'gdp_per_capita',
                       'extreme_poverty', 'cardiovasc_death_rate', 'diabetes_prevalence', 'female_smokers', 'male_smokers', 'handwashing_facilities', 'hospital_beds_per_thousand',
                       'life_expectancy', 'human_development_index', 'new_tests', 'total_tests', 'positive_rate', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated',
                      'new_vaccinations', 'new_vaccinations_smoothed', 'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred',
                      'total_tests_per_thousand', 'new_tests_per_thousand', 'new_tests_smoothed_per_thousand', 'total_cases_per_million', 'total_deaths_per_million', 'positive_rate']

# Load the Citizen CSV as a pandas dataframe, but only selected columns
owid = pd.read_csv(FILE_LOCATION, delimiter=",", usecols=USE_COLS_POPULATION)

owid['date'] =  pd.to_datetime(owid['date'], format='%Y-%m-%d')
owid = owid.rename(columns={'iso_code': 'Geography', 'date': 'Date'})

owid = owid.replace(to_replace ="OWID_AFR",
                 value ="Africa")
owid = owid.replace(to_replace ="OWID_ASI",
                 value ="Asia")
owid = owid.replace(to_replace ="OWID_EUR",
                 value ="Europe")
owid = owid.replace(to_replace ="OWID_NAM",
                 value ="North America")
owid = owid.replace(to_replace ="OWID_SAM",
                 value ="South America")
owid = owid.replace(to_replace ="OWID_OCE",
                 value ="Oceania")

total_case_pm =owid[["Geography", "Date", "total_cases_per_million"]]
total_case_pm = total_case_pm[total_case_pm["Date"] == "2021-02-23"]
total_case_pm = total_case_pm.drop("Date", 1)

# Transform the population data
total_case_pm = total_case_pm.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

total_case_pm = total_case_pm.replace(to_replace ="total_cases_per_million",
                 value =" per 1,000,000 people")
total_case_pm['Count'] = total_case_pm['Count'].round(2)
total_case_pm.to_csv(r'./output/owid_totalCases_perMillion.csv', index = False, sep=',')

total_deaths_pm =owid[["Geography", "Date", "total_deaths_per_million"]]
total_deaths_pm = total_deaths_pm[total_deaths_pm["Date"] == "2021-02-23"]
total_deaths_pm = total_deaths_pm.drop("Date", 1)

# Transform the population data
total_deaths_pm = total_deaths_pm.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

total_deaths_pm = total_deaths_pm.replace(to_replace ="total_deaths_per_million",
                 value =" per 1,000,000 people")
total_deaths_pm['Count'] = total_deaths_pm['Count'].round(2)

total_deaths_pm = total_deaths_pm[total_deaths_pm['Count'].notna()]
total_deaths_pm.to_csv(r'./output/owid_totalDeaths_perMillion.csv', index = False, sep=',')

# Initial transformation and extraction of the population data
population = owid[["Geography", "Date", "population"]]
population = population[population["Date"] == "2021-02-23"]
population = population.drop("Date", 1)

# Transform the population data
population = population.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

population = population.replace(to_replace ="population",
                 value ="2020")

population = population[population['Count'].notna()]
population.to_csv(r'./output/owid_population.csv', index = False, sep=',')

# Initial transformation and extraction of the population density data
pop_density = owid[["Geography", "Date", "population_density"]]
pop_density = pop_density[pop_density["Date"] == "2021-02-23"]
pop_density = pop_density.drop("Date", 1)

# Transform the data
pop_density = pop_density.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

pop_density = pop_density.replace(to_replace ="population_density",
                 value ="Most recent year available")

pop_density = pop_density[pop_density['Count'].notna()]
pop_density['Count'] = pop_density['Count'].round(2)
pop_density.to_csv(r'./output/owid_populationDensity.csv', index = False, sep=',')

# Initial transformation and extraction of the median age data
median_age = owid[["Geography", "Date", "median_age", "life_expectancy"]]
median_age = median_age[median_age["Date"] == "2021-02-23"]
median_age = median_age.drop("Date", 1)

# Transform the data
median_age = median_age.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

median_age = median_age.replace(to_replace ="median_age",
                 value ="Median age")
median_age = median_age.replace(to_replace ="life_expectancy",
                 value ="Life expectancy")

median_age = median_age[median_age['Count'].notna()]
median_age.to_csv(r'./output/owid_medianAge.csv', index = False, sep=',')

# Initial transformation and extraction of the high risk age groups
high_risk = owid[["Geography", "Date", 'aged_65_older', 'aged_70_older']]
high_risk = high_risk[high_risk["Date"] == "2021-02-23"]
high_risk = high_risk.drop("Date", 1)

# Transform the data
high_risk = high_risk.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

high_risk = high_risk.replace(to_replace ="aged_65_older",
                 value ="% of population 65 years and older")
high_risk = high_risk.replace(to_replace ="aged_70_older",
                 value ="% of population 70 years and older")

high_risk = high_risk[high_risk['Count'].notna()]
high_risk['Count'] = high_risk['Count'].round(2)
high_risk.to_csv(r'./output/owid_highRiskAge.csv', index = False, sep=',')

# Initial transformation and extraction of exterme pverty
poverty = owid[["Geography", "Date", 'extreme_poverty']]
poverty = poverty[poverty["Date"] == "2021-02-23"]
poverty = poverty.drop("Date", 1)

# Transform the data
poverty = poverty.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

poverty = poverty.replace(to_replace ="extreme_poverty",
                 value ="% of population")

# poverty = poverty.astype(object).replace(np.nan, 'Null')

poverty = poverty[poverty['Count'].notna()]
poverty.to_csv(r'./output/owid_poverty.csv', index = False, sep=',')

# Initial transformation and extraction of Death rate from cardiovascular disease
cardiovasc = owid[["Geography", "Date", 'cardiovasc_death_rate']]
cardiovasc = cardiovasc[cardiovasc["Date"] == "2021-02-23"]
cardiovasc = cardiovasc.drop("Date", 1)

# Transform the data
cardiovasc = cardiovasc.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

cardiovasc = cardiovasc.replace(to_replace ="cardiovasc_death_rate",
                 value ="Deaths per 100,000 people")

cardiovasc = cardiovasc[cardiovasc['Count'].notna()]
cardiovasc['Count'] = cardiovasc['Count'].round(2)
cardiovasc.to_csv(r'./output/owid_cardiovasc.csv', index = False, sep=',')

# Initial transformation and extraction of Death rate from cardiovascular disease
diabetes = owid[["Geography", "Date", 'diabetes_prevalence']]
diabetes = diabetes[diabetes["Date"] == "2021-02-23"]
diabetes = diabetes.drop("Date", 1)

# Transform the data
diabetes = diabetes.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

diabetes = diabetes.replace(to_replace ="diabetes_prevalence",
                 value ="% of population aged 20 to 79")

diabetes = diabetes[diabetes['Count'].notna()]
diabetes.to_csv(r'./output/owid_diabetes.csv', index = False, sep=',')

# Initial transformation and extraction of smoking
smoking = owid[["Geography", "Date", 'female_smokers', 'male_smokers']]
smoking = smoking[smoking["Date"] == "2021-02-23"]
smoking = smoking.drop("Date", 1)

# Transform the data
smoking = smoking.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

smoking = smoking.replace(to_replace ="female_smokers",
                 value ="Female")
smoking = smoking.replace(to_replace ="male_smokers",
                 value ="Male")

# smoking = smoking.astype(object).replace(np.nan, 'Null')
smoking = smoking[smoking['Count'].notna()]
smoking.to_csv(r'./output/owid_smoking.csv', index = False, sep=',')

# Initial transformation and extraction of handwashing facilities
handwashing = owid[["Geography", "Date", 'handwashing_facilities']]
handwashing = handwashing[handwashing["Date"] == "2021-02-23"]
handwashing = handwashing.drop("Date", 1)

# Transform the data
handwashing = handwashing.melt(id_vars=["Geography"],
        var_name="Indicator",
        value_name="Count")

handwashing = handwashing.replace(to_replace ="handwashing_facilities",
                 value ="% of population")

handwashing = handwashing[handwashing['Count'].notna()]
handwashing['Count'] = handwashing['Count'].round(2)
handwashing.to_csv(r'./output/owid_handwashing.csv', index = False, sep=',')

# Initial transformation and extraction of total vaccinations per 100 people
vaccinations = owid[["Geography", "Date", "total_vaccinations_per_hundred"]]
vaccinations = vaccinations[vaccinations["Date"] > "2021-02-01"]

vaccinations = vaccinations.pivot(index='Geography', columns='Date')
vaccinations.columns = vaccinations.columns.droplevel(0)
vaccinations['LastValue'] = vaccinations.iloc[:, 1:].ffill(axis=1).iloc[:, -1]
vaccinations.drop(vaccinations.columns.difference(['Geography','LastValue']), 1, inplace=True)

vaccinations['Indicator'] = "per 100 people"
vaccinations.reset_index(level=0, inplace=True)
vaccinations = vaccinations.astype(object).replace(np.nan, 'Null')

vaccinations = vaccinations.rename(columns={'LastValue': 'Count'})
vaccinations = vaccinations[vaccinations['Count'].notna()]
vaccinations.to_csv(r'./output/owid_Vaccinations_perHundred.csv', index = False, sep=',')

# Initial transformation and extraction of vaccinations administered
vac1 = owid[["Geography", "Date", "people_vaccinated"]]
vac1 = vac1[vac1["Date"] > "2021-02-01"]

vac1 = vac1.pivot(index='Geography', columns='Date')
vac1.columns = vac1.columns.droplevel(0)
vac1['LastValue'] = vac1.iloc[:, 1:].ffill(axis=1).iloc[:, -1]
vac1.drop(vac1.columns.difference(['Geography','LastValue']), 1, inplace=True)
vac1['Indicator'] = "At least one vaccine dose"
vac1.reset_index(level=0, inplace=True)
vac1 = vac1.astype(object).replace(np.nan, 'Null')
vac1 = vac1.rename(columns={'LastValue': 'Count'})

vac2 = owid[["Geography", "Date", "people_fully_vaccinated"]]
vac2 = vac2[vac2["Date"] > "2021-02-01"]

vac2 = vac2.pivot(index='Geography', columns='Date')
vac2.columns = vac2.columns.droplevel(0)
vac2['LastValue'] = vac2.iloc[:, 1:].ffill(axis=1).iloc[:, -1]
vac2.drop(vac2.columns.difference(['Geography','LastValue']), 1, inplace=True)
vac2['Indicator'] = "All doses prescribed by the vaccination protocol"
vac2.reset_index(level=0, inplace=True)
vac2 = vac2.astype(object).replace(np.nan, 'Null')
vac2 = vac2.rename(columns={'LastValue': 'Count'})

tmp = [vac1, vac2]
vaccinations_totals = pd.concat(tmp)

vaccinations_totals = vaccinations_totals[vaccinations_totals['Count'].notna()]
vaccinations_totals.to_csv(r'./output/owid_Vaccinations_DosesReceived.csv', index = False, sep=',')

# Works but there is too many countries with 0 values in Africa
tests_tmp = owid[["Geography", "Date", "new_tests_per_thousand"]]
start_date = '2021-01-01'
end_date = '2021-02-19'
mask = (tests_tmp['Date'] > start_date) & (tests_tmp['Date'] <= end_date)
tests_weekly = tests_tmp.loc[mask]

tests_weekly = (tests_weekly.groupby([pd.Grouper(key='Date', freq='W'), 'Geography'])['new_tests_per_thousand']
   .sum().round(0)
   .reset_index())

tests_weekly = tests_weekly.melt(id_vars=["Geography", "Date"],
                                    var_name="Indicator",
                                    value_name="Count")

tests_weekly['Date']= tests_weekly['Date'].dt.strftime('2021-WN%U')

tests_weekly = tests_weekly.drop("Indicator", 1)

tests_weekly = tests_weekly[tests_weekly['Count'].notna()]

tests_weekly.to_csv(r'./output/owid_NewTests_weekly.csv', index = False, sep=',')

# Initial transformation and extraction of total tests per 1000 people
total_tests = owid[["Geography", "Date", "total_tests_per_thousand"]]
total_tests = total_tests[total_tests["Date"] > "2021-02-01"]

total_tests = total_tests.pivot(index='Geography', columns='Date')
total_tests.columns = total_tests.columns.droplevel(0)
total_tests['LastValue'] = total_tests.iloc[:, 1:].ffill(axis=1).iloc[:, -1]
total_tests.drop(total_tests.columns.difference(['Geography','LastValue']), 1, inplace=True)

total_tests['Indicator'] = "per 1,000 people"
total_tests.reset_index(level=0, inplace=True)
total_tests = total_tests.astype(object).replace(np.nan, 'Null')

total_tests = total_tests.rename(columns={'LastValue': 'Count'})
total_tests['Count'] = pd.to_numeric(total_tests['Count'],errors='coerce')
total_tests['Count'] = total_tests['Count'].round(2)
total_tests = total_tests[total_tests['Count'].notna()]
total_tests.to_csv(r'./output/owid_TotalTests_perThousand.csv', index = False, sep=',')

# Initial transformation and extraction of positivity rate
positive_rate = owid[["Geography", "Date", "positive_rate"]]
start_date = '2021-01-01'
end_date = '2021-02-19'
mask = (positive_rate['Date'] > start_date) & (positive_rate['Date'] <= end_date)
positive_rate = positive_rate.loc[mask]

positive_rate = (positive_rate.groupby([pd.Grouper(key='Date', freq='W'), 'Geography'])['positive_rate']
   .mean()
   .reset_index())

positive_rate = positive_rate.melt(id_vars=["Geography", "Date"],
                                    var_name="Indicator",
                                    value_name="Count")

positive_rate['Count'] = (positive_rate['Count']*100).round(2)

positive_rate['Date']= positive_rate['Date'].dt.strftime('2021-WN%U')

positive_rate = positive_rate.drop("Indicator", 1)
# positive_rate = positive_rate.astype(object).replace(np.nan, 'Null')

positive_rate = positive_rate[positive_rate['Count'].notna()]
positive_rate.to_csv(r'./output/owid_Positive_Rate.csv', index = False, sep=',')
