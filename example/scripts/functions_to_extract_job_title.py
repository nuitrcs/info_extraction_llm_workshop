# Script with functions to the job title from job postings
# Emilio Lehoucq

######################################### IMPORTING LIBRARIES #########################################
import os
from functions_azure import get_response_full_process

######################################### PATHS #########################################
if os.environ.get("PIPELINE_RUN", "0") == "1":
    path_prompts_folder = "../prompts/"
else:
    path_prompts_folder = "prompts/"
path_prompt = "job_title.txt"

######################################### READING DATA #########################################
prompt = open(path_prompts_folder + path_prompt, "r").read()

######################################### FUNCTION DEFINITIONS #########################################

def extract_job_title(text):
    """
    Function to extract the job title from a job posting text.

    Input:
    - text (str): text of the job posting.

    Output:
    - job_title (str): job title extracted from the job posting.
    """
    # Raise an error if the input is not a string
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    # Get response from model
    return get_response_full_process(prompt, text, 5, 5, 10, 0.5)

if __name__ == "__main__":
    print("Module to extract job title from job postings running as main script.")
    print("Running tests...")

    ##################################################################################
    print("Tests for extract_job_title function:")

    # # Commenting this test to not keep sending requests to the API
    # print("Test 1")
    # text = "We are looking for a Data Scientist to join our team."
    # assert extract_job_title(text) == "data scientist"

    ##################################################################################
    print("All tests passed.")