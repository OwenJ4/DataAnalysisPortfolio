#Python script for analysing Office for National Statistics Census 2021 data 
#Date: 21/03/2024
#Author: Owen Jones

import numpy as np
import pandas as pd

#Age Religion Ethnicity (ARE) England and Wales
AREData = pd.read_csv('custom-filtered-2024-03-20T21_44_18Z.csv')
#Dropping redundant England and Wales Columns
AREData = AREData.drop(['England and Wales Code', 'England and Wales'], axis = 1)

#Checking if data looks correct
#print(AREData) # it does

##Data Cleaning
#Transforming 6 categorical variables into 5: under 25, 25-34, 35-49, 50-64, 65+
AREData['Age (6 categories)'] = AREData['Age (6 categories)'].str.replace('Aged 15 years and under', 'Aged 25 years and under', case=False)
AREData['Age (6 categories)'] = AREData['Age (6 categories)'].str.replace('Aged 16 to 24 years', 'Aged 25 years and under', case=False)
#Transforming 'Does not apply' and 'Not answered' into 'No response' for readability
AREData['Religion (10 categories)'] = AREData['Religion (10 categories)'].str.replace('Does not apply', 'No response', case=False)
AREData['Religion (10 categories)'] = AREData['Religion (10 categories)'].str.replace('Not answered', 'No response', case=False)
AREData = AREData
AREData['Ethnic group (20 categories)'] = AREData['Ethnic group (20 categories)'].str.replace('Does not apply', 'No response', case=False)
AREData['Ethnic group (20 categories)'] = AREData['Ethnic group (20 categories)'].str.replace('Not answered', 'No response', case=False)
#Renaming columns
AREData = AREData.rename(columns = {'Age (6 categories)': 'Age group', 'Religion (10 categories)': 'Religion', 'Ethnic group (20 categories)': 'Ethnic group'})

#Find the total respondents by age
AgeObs = AREData.groupby(['Age group'])['Observation'].sum()
#Grouping variables by Age and Religion
ARGroupData = pd.pivot_table(AREData, index = ['Age group'], columns=['Religion'], values=['Observation'], aggfunc=np.sum)
#print(AgeObs)
#print(ARGroupData)

#Find under 25 for Religion and Ethnicity
REData = AREData.loc[AREData['Age group'] == 'Aged 25 years and under']
EthnicityObs = REData.groupby(['Ethnic group'])['Observation'].sum()
REGroupData = pd.pivot_table(REData, index = ['Ethnic group'], columns=['Religion'], values=['Observation'], aggfunc=np.sum)
#print(EthnicityObs)
#print(REGroupData)

##Converting to percentages/proportion

#Converting to proportions
#Age and Religion
PropARData = ARGroupData.div(ARGroupData.sum(axis=1), axis=0)
print(PropARData)
#Under 25 proportions: Religion by Ethnicity
PropREData = REGroupData.div(REGroupData.sum(axis=1), axis=0)
print(PropREData)

#Converting to proportions to percentages
#Age and Religion
pcARData = PropARData.mul(100, axis = 1)
print(pcARData)
#Under 25: Religion by Ethnicity
pcREData = PropREData.mul(100, axis = 1)
print(pcREData)

#Writing results 
PropARData.to_csv('Proportion of people in England and Wales identifying with a religion by Age.csv', index=True)
pcARData.to_csv('Percent of people in England and Wales identifying with a religion by Age.csv', index = True)
PropREData.to_csv('Proportion of people under 25 years in England and Wales identifying with a religion by ethnicity.csv', index=True)
pcREData.to_csv('Percent of people under 25 years in England and Wales identifying with a religion by ethnicity.csv', index=True)
