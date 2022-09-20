#import the dependencies
from codecs import ignore_errors
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import tabulate
from tableone import TableOne

#load in the dataframe
SPARCS = pd.read_csv('data/cleaned_SPARCS_2016.csv', index_col=0)

for column in SPARCS.columns:
    if SPARCS[column].dtype == 'object':
        SPARCS[column] = SPARCS[column].astype('category')

#double check dtypes, column names, and dataframe size.
SPARCS.dtypes
SPARCS.shape

###Descriptive Statistics of ALL of the data.
#Below is a bar graph of the average length of stay for each age group.
data = SPARCS.groupby('age_group')['length_of_stay'].mean()
fig, ax = plt.subplots()

ax.bar(data.index, data.values)
ax.set_title('Average Length of Stay for Each Age Group')
ax.set_xlabel('Age Group')
ax.set_ylabel('Average Length of Stay')

plt.show()

#Below is a pie chart of the relative % of discharges for each service area.

data = SPARCS['service_area'].value_counts()
fig, ax = plt.subplots()

ax.set_title('Relative % of Discharges for Each Service Area')
ax.pie(data.values, labels=data.index, autopct='%1.0f%%')
plt.show()

#Below is a box plot of the average total charges for each service area.
fig, ax = plt.subplots()
SPARCS.boxplot(
    column='total_charges', by='service_area', ax=ax, 
    showfliers=False, patch_artist=True, 
    medianprops={'linewidth': 2, 'color': 'purple'},
    meanprops={'linewidth': 2, 'color': 'red'})

fig.set_dpi(130)
fig.set_size_inches(20, 10)

ax.set_title('Average Total Charges for Each Service Area')
ax.set_xlabel('Service Area')
ax.set_ylabel('Average Total Charges')
ax.autoscale()


plt.show() 

#Pie chart of ethnicity 

data = SPARCS['ethnicity'].value_counts()
data
fig, ax = plt.subplots()
ax.pie(data.values, labels=data.index, autopct='%1.0f%%')

plt.show()

##Table for overall data
table = TableOne(
    SPARCS, 
    columns=['length_of_stay', 'total_costs', 'risk_of_mortality', 'race', 'insurance', 'type_of_admission'], 
    categorical=['risk_of_mortality', 'race','insurance', 'type_of_admission'], 
    groupby='age_group'
)

table.to_excel('SPARCS_table_Overall.xlsx')

###Descriptive Stats for a specific service area
SPARCS['service_area'].value_counts()

area = 'Long Island'
SPARCS_AREA = SPARCS[SPARCS['service_area'] == area]
SPARCS_AREA.shape
SPARCS_AREA.dtypes

#Below is a box plot of the average length of stay based on race for the given service area.
fig, ax = plt.subplots()
SPARCS_AREA.boxplot(
    column='length_of_stay', by='race', ax=ax, 
    showfliers=False, patch_artist=True, 
    medianprops={'linewidth': 2, 'color': 'purple'},
    meanprops={'linewidth': 2, 'color': 'red'})

fig.set_dpi(130)
fig.set_size_inches(20, 10)

ax.autoscale()
ax.set_title('Average Length of Stay by ethnicity for ' + area)

plt.show() 

#Pie chart of ethnicity 
data = SPARCS_AREA['ethnicity'].value_counts()
fig, ax = plt.subplots()

ax.set_title('Ethnicity')
ax.pie(data.values, labels=data.index, autopct='%1.0f%%')

plt.show()

#Pie Chart of emergency admissions vs non-emergency
data = SPARCS_AREA['emergency_dept'].value_counts()
fig, ax = plt.subplots()

ax.set_title('Emergency Admissions vs Non-Emergency Admissions')
ax.pie(data.values, labels=('ER', 'Other'), autopct='%1.1f%%')

plt.show()

#A table using the tableone package to show the most common risk factors for mortality in the given service area.

table = TableOne(
    SPARCS_AREA, 
    columns=['length_of_stay', 'total_costs', 'risk_of_mortality', 'race', 'insurance', 'type_of_admission'], 
    categorical=['risk_of_mortality', 'race','insurance', 'type_of_admission'], 
    groupby='age_group'
)

table.to_excel('SPARCS_table_LI.xlsx')