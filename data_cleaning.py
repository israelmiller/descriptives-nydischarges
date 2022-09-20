#load in dependencies
import pandas as pd
import numpy as np
#import the dataframe

SPARCS = pd.read_csv('data/Hospital_Inpatient_Discharges__SPARCS_De-Identified___2016.csv')

##Cleaning up the columns

#Check the column names and dataframe size 
SPARCS.columns
##SPARCS = SPARCS.head(100)
SPARCS.shape

#Normalize the column names by removing spaces, symbols and lowercase using regex
SPARCS.columns = SPARCS.columns.str.replace('[^A-Za-z0-9]+', '_', regex=True)
SPARCS.columns = SPARCS.columns.str.lower()

#Drop uneeded columns for this analysis
SPARCS.drop({
    'operating_certificate_number',
    'facility_id',
    'discharge_year',
    'payment_typology_2',
    'payment_typology_3',
    'zip_code_3_digits',
}, inplace=True, axis=1)


#rename some columns for clarity

SPARCS.rename(columns=({
    'health_service_area' : 'service_area',
    'apr_drg_description' : 'drg_description',
    'apr_drg_code' : 'drg_code',
    'apr_mdc_description' : 'mdc_description',
    'apr_severity_of_illness_code' : 'severity_of_illness_code', 
    'apr_severity_of_illness_description' : 'severity_of_illness_description',
    'apr_risk_of_mortality' : 'risk_of_mortality',
    'apr_medical_surgical_description' : 'medical_surgical_description',
    'payment_typology_1' : 'insurance',
    'abortion_edit_indicator' : 'abortion',
    'emergency_department_indicator' : 'emergency_dept',
}), inplace=True)

##Cleaning up the rows and data types

#Remove special characters from the data

SPARCS['total_costs'] = SPARCS['total_costs'].str.replace(',', '')
SPARCS['total_charges'] = SPARCS['total_charges'].str.replace(',', '')

#Check Data Types

SPARCS.dtypes

#normalize the data in some columns so that a more effiecient data type can be used

SPARCS['length_of_stay'] = np.where(SPARCS['length_of_stay']==('120 +'), '120', SPARCS['length_of_stay'])


SPARCS['emergency_dept'] = np.where(SPARCS['emergency_dept'] == 'Y', True, False)
SPARCS['abortion'] = np.where(SPARCS['abortion'] == 'Y', True, False)

##Change the data types to the correct format

#ints
SPARCS['length_of_stay'] = SPARCS['length_of_stay'].astype('int')
SPARCS['birth_weight'] = SPARCS['birth_weight'].astype('int')

#floats
SPARCS['total_costs'] = SPARCS['total_costs'].astype(float)
SPARCS['total_charges'] = SPARCS['total_charges'].astype(float)

#bools
SPARCS['emergency_dept'] = SPARCS['emergency_dept'].astype(bool)
SPARCS['abortion'] = SPARCS['abortion'].astype(bool)

for column in SPARCS.columns:
    if SPARCS[column].dtype == 'object':
        SPARCS[column] = SPARCS[column].astype('category')

SPARCS.to_csv('data/cleaned_SPARCS_2016.csv')

exit()