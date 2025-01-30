# Script to extract information from the text of job postings 
# Emilio Lehoucq

######################################### IMPORTING LIBRARIES #########################################
import pandas as pd
from functions_to_extract_salary import extract_salary
from functions_to_extract_organization import extract_organization
from functions_to_extract_job_title import extract_job_title
from functions_to_extract_visa import extract_visa
from functions_to_extract_location import extract_location
from functions_to_extract_education import extract_education
import os

######################################### FILE PATHS #########################################

if os.environ.get("PIPELINE_RUN", "0") == "1":
    path_processed_data = "../data/processed/"
else:
    path_processed_data = "data/processed/"
file_name_input_data = "data_to_test_accuracy_info_extraction_11_18_24.csv"
file_name_output_data = "data_information_extracted_test.csv"

######################################### READING DATA #########################################

df = pd.read_csv(path_processed_data + file_name_input_data)

######################################### EXTRACTING INFORMATION #########################################

# Iterate over the rows of the dataframe
# for i, row in df.iterrows():
for i, row in df.sample(50).iterrows(): # TODO: comment this line and uncomment the one above to run the whole dataset

    # Create variable with text making sure it is a string
    text = str(row['text'])

    # Create variable with URL making sure it is a string
    url = str(row['url_job_post'])

    # # Salary
    # df.at[i, 'salary_extracted'] = extract_salary(text)

    # # Organization
    # df.at[i, 'organization_extracted'] = extract_organization(url, text)

    # # Job title
    # df.at[i, 'job_title_extracted'] = extract_job_title(text)

    # # Location
    # df.at[i, 'location_extracted'] = extract_location(text)

    # # Visa
    # df.at[i, 'visa_extracted'] = extract_visa(text)

    # Education
    df.at[i, 'education_extracted'] = extract_education(text)

######################################### SAVING DATA #########################################

df.to_csv(path_processed_data + file_name_output_data, index=False)