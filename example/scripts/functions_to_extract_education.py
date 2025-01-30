# Script with functions to extract education from job postings
# Emilio Lehoucq

######################################### IMPORTING LIBRARIES #########################################
import os
from functions_azure import get_response_full_process

######################################### PATHS #########################################
if os.environ.get("PIPELINE_RUN", "0") == "1":
    path_prompts_folder = "../prompts/"
else:
    path_prompts_folder = "prompts/"
path_prompt = "education.txt"

######################################### READING DATA #########################################
prompt = open(path_prompts_folder + path_prompt, "r").read()

######################################### FUNCTION DEFINITIONS #########################################

def extract_education(text):
    """
    Function to extract education from a job posting text.

    Input:
    - text (str): text of the job posting.

    Output:
    - education (str): education extracted from the job posting.
    """
    # Raise an error if the input is not a string
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    # Get response from model
    return get_response_full_process(prompt, text, 5, 5, 10, 0.5)

if __name__ == "__main__":
    print("Module to extract education from job postings running as main script.")
    print("Running tests...")

    ##################################################################################
    print("Tests for extract_education function:")

    # Commenting this test to not keep sending requests to the API
    print("Test 1")
    text = "A bachelor degree is required for this position."
    assert extract_education(text) == "bachelor"

    ##################################################################################
    print("All tests passed.")