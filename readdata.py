import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib
matplotlib.use('TkAgg')  # Use the TkAgg backend for interactive plots
import matplotlib.pyplot as plt

df = pd.read_csv('owid-covid-data.csv')

print(df.columns)

print(df.head())

print(df.isnull().sum())


#data cleaning

countries_of_interest = ['Kenya', 'USA', 'India']
df_filtered = df[df['location'].isin(countries_of_interest)]

df_filtered = df_filtered.dropna(subset=['date', 'total_cases', 'total_deaths'])

df_filtered['date'] = pd.to_datetime(df_filtered['date'])

df_filtered['total_cases'] = df_filtered['total_cases'].fillna(0)
df_filtered['total_deaths'] = df_filtered['total_deaths'].fillna(0)


#data analysis


# Plot total cases over time for selected countries
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    plt.plot(df_filtered[df_filtered['location'] == country]['date'],
             df_filtered[df_filtered['location'] == country]['total_cases'],
             label=country)
plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.show()

# Plot total deaths over time
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    plt.plot(df_filtered[df_filtered['location'] == country]['date'],
             df_filtered[df_filtered['location'] == country]['total_deaths'],
             label=country)
plt.title('Total COVID-19 Deaths Over Time')
plt.xlabel('Date')
plt.ylabel('Total Deaths')
plt.legend()
plt.show()

# Calculate the death rate
df_filtered['death_rate'] = df_filtered['total_deaths'] / df_filtered['total_cases']


#visualization of data
# Plot cumulative vaccinations over time for selected countries
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    plt.plot(df_filtered[df_filtered['location'] == country]['date'],
             df_filtered[df_filtered['location'] == country]['total_vaccinations'],
             label=country)
plt.title('Cumulative Vaccinations Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.legend()
plt.show()

# Compare % vaccinated population
df_filtered['vaccination_rate'] = df_filtered['total_vaccinations'] / df_filtered['population'] * 100


#visualization using a chlorophleth map

# Prepare a dataframe with iso_code, total_cases for the latest date
latest_data = df_filtered[df_filtered['date'] == df_filtered['date'].max()]
fig = px.choropleth(latest_data,
                    locations='iso_code',
                    locationmode='ISO-3',
                    color='total_cases',
                    hover_name='location',
                    color_continuous_scale=px.colors.sequential.Plasma)
fig.update_geos(showcoastlines=True, coastlinecolor="Black")
fig.show()
