# Script with functions to extract visa info from job postings
# Emilio Lehoucq

######################################### IMPORTING LIBRARIES #########################################
import os
from functions_azure import get_response_full_process

######################################### PATHS #########################################
if os.environ.get("PIPELINE_RUN", "0") == "1":
    path_prompts_folder = "../prompts/"
else:
    path_prompts_folder = "prompts/"
path_prompt = "visa.txt"

######################################### READING DATA #########################################
prompt = open(path_prompts_folder + path_prompt, "r").read()

######################################### FUNCTION DEFINITIONS #########################################

def extract_visa(text):
    """
    Function to extract visa information from a job posting text.

    Input:
    - text (str): text of the job posting.

    Output:
    - visa (str): visa information extracted from the job posting.
    """
    # Raise an error if the input is not a string
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    # Get response from model
    return get_response_full_process(prompt, text, 5, 5, 10, 0.5)

if __name__ == "__main__":
    print("Module to extract visa information from job postings running as main script.")
    print("Running tests...")

    ##################################################################################
    print("Tests for extract_visa function:")

    # # Commenting this test to not keep sending requests to the API
    # print("Test 1")
    # text = "Visa sponsorship is not available for this position."
    # assert extract_visa(text) == "no"

    ##################################################################################
    print("All tests passed.")