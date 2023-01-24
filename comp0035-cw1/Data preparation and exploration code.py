#!/usr/bin/env python
# coding: utf-8

# Data Preparation and Exploration 

# Prepare data

# Import relevant libraries 
import pandas as pd 
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Draw graph on notebook
get_ipython().run_line_magic('matplotlib', 'inline')

# Use ggplot style 
plt.style.use('ggplot')

# Suspress Deprecation and Incorrect Usage Warnings
import warnings 
warnings.filterwarnings('ignore')


# In[2]:


# Load the dataset from Google sheets using the URL and manipulating the URL to get the CSV file
google_sheet_url = 'https://docs.google.com/spreadsheets/d/1JWzBy8775LyIk3-_VwqU9FUeF4sGDs6eyNSP4YEmVt4/edit#gid=911693755'
url = google_sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

df = pd.read_csv(url)


# In[3]:


# Number of row and columns in dataset
df.shape


# In[4]:


# Print column names
print('Initial columns')
print(df.columns)


# In[5]:


# Change column names more simple 
df.rename(columns={'Rented Bike Count':'Count', 'Temperature(蚓)':'Temp',
                   'Humidity(%)':'Humidity', 'Wind speed (m/s)':'Windspeed',
                   'Visibility (10m)':'Visibility', 'Dew point temperature(蚓)':'DP_Temp',
                   'Solar Radiation (MJ/m2)':'Solar_Rad', 'Rainfall(mm)':'Rainfall',
                   'Snowfall (cm)':'Snowfall', 'Functioning Day':'Func_Day'}, inplace=True)


# In[6]:


# Check for missing values 
print(df.isna().any())


# In[7]:


# Date column has to be changed to a date type data
df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")


# In[8]:


# Create year, month, day, day of week columns
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['DayofWeek'] = df['Date'].dt.day_name()


# In[9]:


# Create a column with year and month 
def combine_year_month(date):
    return "{0}-{1}".format(date.year, date.month)

df["Year_Month"] = df["Date"].apply(combine_year_month)


# In[21]:


# Add column for Day and Night
df['Day_Night'] = df['Hour'].apply(lambda x :'Night' if (x>18 or x<6) else('Day'))


# In[10]:


# Check the Data and see if changes were applied
df.head()


# Explore the Data

# In[11]:


# Checking the number of data from 2017 and 2018 
NUM_2017 = (df.Year == 2017).sum()
NUM_2018 = (df.Year == 2018).sum()
print('Number of data from 2017: {}, Number of data from 2018 : {}'.format(NUM_2017, NUM_2018))


# In[12]:


# Bar chart year and month for the number of bike rented
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
fig.set_size_inches(13, 10)
sns.barplot(data=df, x="Year_Month", y="Count", ax=ax1)
sns.barplot(data=df, x="Month", y="Count", ax=ax2)


# In[13]:


# Box plot to explore the data with the number of bicycle
fig, axes = plt.subplots(nrows=2,ncols=2)
fig.set_size_inches(12,10)
sns.boxplot(data=df, y='Count', orient='v', ax=axes[0][0])
sns.boxplot(data=df, y="Count", x="Seasons", orient="v", ax=axes[0][1])
sns.boxplot(data=df, y="Count", x="Func_Day", orient="v", ax=axes[1][0])
sns.boxplot(data=df, y="Count", x="Month", orient="v", ax=axes[1][1])


# In[35]:


# Bar graph of number of bikes rent for each hour
plt.figure(figsize=(13,5))
sns.barplot(data=df, x='Hour', y='Count')


# In[15]:


# Pointplot of Count VS. Bike with other features
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
fig.set_size_inches(13,12)
sns.pointplot(data=df, x='Hour', y='Count', hue='Holiday', ax=ax1)
sns.pointplot(data=df, x='Hour', y='Count', hue='DayofWeek', ax=ax2)


# In[16]:


# Pivot table of number of bikes rented for day of week for holiday and not holiday
df.pivot_table(index=['Holiday', 'DayofWeek'], values=['Count'], 
               aggfunc='sum').sort_values(ascending=False, by='Count')


# In[17]:


# Change Year, Month, Day to object so they don't show up when used describe()
for x in ['Year', 'Month', 'Day']: 
    df[x] = df[x].astype('object')


# In[18]:


# Looking at the stats of the data for numerical variables
df.describe().T


# In[19]:


# Heatmap to understand the correlations between the variables
plt.figure(figsize=(10,10))
sns.heatmap(df.corr("pearson"),
            vmax=1, vmin=-1,
            cmap='coolwarm',
            annot=True)


# In[20]:


# Drop columns that are found to be irrelevant in further understanding
df = df.drop(['DP_Temp'], axis=1)
df = df.drop(['Func_Day'], axis=1)


# In[22]:


# Save the prepared data to CSV
# df.to_csv('C:/Users/sbak0/Downloads/Bike_data_adjusted.csv')


# In[5]:


# Changed dataset 
google_sheet_url = 'https://docs.google.com/spreadsheets/d/19r2fuwp4ypn0X2-7sQzTlKXr7lcnRuMlvyzc7vjUE_c/edit#gid=187305695'
url = google_sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

df_prepared = pd.read_csv(url)

