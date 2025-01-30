# Script with functions to extract location from job postings
# Emilio Lehoucq

######################################### IMPORTING LIBRARIES #########################################
import os
import pandas as pd
import re
from functions_azure import get_response_full_process

######################################### PATHS #########################################
if os.environ.get("PIPELINE_RUN", "0") == "1":
    path_processed_data_folder = "../data/processed/"
    path_prompts_folder = "../prompts/"
else:
    path_processed_data_folder = "data/processed/"
    path_prompts_folder = "prompts/"
path_data_us_cities = "uscities_processed.csv"
path_data_university_cities = "university_cities.csv"
path_prompt = "location.txt"

######################################### READING DATA #########################################
us_cities = pd.read_csv(path_processed_data_folder + path_data_us_cities)
cities = us_cities["city"].tolist()
cities_ascii = us_cities['city_ascii'].to_list()
state_abbreviations = us_cities["state_id"].tolist()
state_full_name = us_cities["state_name"].tolist()
assert len(cities) == len(cities_ascii) == len(state_abbreviations) == len(state_full_name), "Lengths of lists do not match."
# # Commenting this out because I'm not searching only for cities
# university_cities = pd.read_csv(path_processed_data_folder + path_data_university_cities)
# university_cities = university_cities["city"].unique().tolist()
prompt = open(path_prompts_folder + path_prompt, "r").read()

######################################### REGULAR EXPRESSIONS #########################################

# 1) Regex for all US cities

# Precompile patterns
common_pattern = r"[.,:;!?'\"(){}\[\]\-\—_…\s]"

# Build regex for all city, state combinations
city_state_patterns = [
    fr"{re.escape(city)}(?:,\s|\s){re.escape(state)}"
    for city, state in zip(cities_ascii, state_full_name)
] + [
    fr"{re.escape(city)}(?:,\s|\s){re.escape(state)}"
    for city, state in zip(cities, state_abbreviations)
]

# # Commenting this out because 1) it slows down the script and 2) introduces more errors than it solves because it
# # matches too many false positives (University, Institute, etc.). There could be a way to deal with this (e.g., 
# # deleting city names that are common words), but leaving it aside for now to try other alternatives.
# # Build regex for just cities and states
# city_only_patterns = [fr"(?<={common_pattern}){re.escape(city)}(?={common_pattern})" for city in cities_ascii + cities]
# state_only_patterns = [fr"(?<={common_pattern}){re.escape(state)}(?={common_pattern})" for state in state_full_name + state_abbreviations]

# Combine all patterns into a single regex
full_pattern = "|".join(city_state_patterns)
# full_pattern = "|".join(city_state_patterns + city_only_patterns + state_only_patterns)

# # 2) Regex for university cities

# # Commenting this out since I'm not searching only for cities
# city_only_patterns_university_cities = [fr"(?<={common_pattern}){re.escape(city)}(?={common_pattern})" for city in university_cities]
# full_pattern_university_cities = "|".join(city_only_patterns_university_cities)

######################################### FUNCTION DEFINITIONS #########################################

def extract_location(text):
    """
    Function to extract location from a job posting text.

    Input:
    - text (str): text of the job posting.

    Output:
    - location (str): location extracted from the job posting.
    """
    # Raise an error if the input is not a string
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    # 1) Using list of US cities, search for city, state combinations
    location = extract_uscities(text)
    if location:
        return location

    # # Commenting this out because it didn't improve the accuracy and, particularly bad, added a lot of false positives
    # # 2) Using list of cities where there are universities in the US, search for only city or state
    # location = extract_university_cities(text)
    # if location:
    #     return location

    # 3) Use LLM
    return get_response_full_process(prompt, text, 5, 5, 10, 0.5)

def extract_uscities(text):
    """
    Function to extract US cities from a job posting text.
    
    Input:
    - text (str): Text of the job posting.
    
    Output:
    - location (str): Location extracted from the job posting or None if not found.

    ChatGPT helped me optimize the function I had written.
    """
    # Validate input
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Search the text once
    match = re.search(full_pattern, text)
    if match:
        return match.group()
    return None

# Commenting this out because I'm not searching only for cities
# def extract_university_cities(text):
#     """
#     Function to extract university cities from a job posting text.

#     Input:
#     - text (str): Text of the job posting.

#     Output:
#     - location (str): Location extracted from the job posting or None if not found.
#     """
#     # Validate input
#     if not isinstance(text, str):
#         raise ValueError("Input must be a string.")
    
#     # Search the text
#     match = re.search(full_pattern_university_cities, text)
#     if match:
#         return match.group()
#     return None

if __name__ == "__main__":
    print("Module to extract location from job postings running as main script.")
    print("Running tests...")

    ##################################################################################
    print("Tests for extract_location function:")

    # Commenting this out since I'd send a request to Azure
    # print("Test 1")
    # text = ""
    # print(extract_location(text))
    # assert extract_location(text) == None

    print("Test 2")
    text = "The position is in-person in Evanston, Illinois, in the Northwestern campus."
    print(extract_location(text))
    assert extract_location(text) == "Evanston, Illinois"

    print("Test 3")
    text = "The position is in-person in Evanston, IL, in the Northwestern campus."
    print(extract_location(text))
    assert extract_location(text) == "Evanston, IL"

    print("Test 7")
    text = "The position is in Evanston IL."
    print(extract_location(text))
    assert extract_location(text) == "Evanston IL"

    # # Commenting this out because I'm not searching only for cities
    # print("Test 8")
    # text = "The position is in Evanston."
    # print(extract_location(text))
    # assert extract_location(text) == "Evanston"

    # # Commenting this out to not keep sending requests to Azure
    # print("Test 8")
    # text = "The position is location in Vienna, Austria."
    # assert extract_location(text) == "vienna, austria"

    ##################################################################################
    print("Tests for extract_uscities function:")

    print("Test 1")
    text = ""
    print(extract_uscities(text))
    assert extract_uscities(text) == None

    print("Test 2")
    text = "The position is in-person in Evanston, Illinois, in the Northwestern campus."
    print(extract_uscities(text))
    assert extract_uscities(text) == "Evanston, Illinois"

    print("Test 3")
    text = "The position is in-person in Evanston, IL, in the Northwestern campus."
    print(extract_uscities(text))
    assert extract_uscities(text) == "Evanston, IL"

    # print("Test 4")
    # text = "The position is in-person in Evanston, in the Northwestern campus."
    # print(extract_uscities(text))
    # assert extract_uscities(text) == "Evanston"

    # print("Test 5")
    # text = "The position is in-person in Illinois, in the Northwestern campus."
    # print(extract_uscities(text))
    # assert extract_uscities(text) == "Illinois"

    # print("Test 6")
    # text = "The position is in-person in IL, in the Northwestern campus."
    # print(extract_uscities(text))
    # assert extract_uscities(text) == "IL"

    ##################################################################################
    # # Commenting this out because I'm not searching only for cities
    # print("Tests for extract_university_cities function:")

    # print("Test 1")
    # text = ""
    # print(extract_university_cities(text))
    # assert extract_university_cities(text) == None

    # print("Test 2")
    # text = "The position is in Evanston IL."
    # print(extract_university_cities(text))
    # assert extract_university_cities(text) == "Evanston"

    ##################################################################################
    print("All tests passed.")