# Script with functions to extract organization from job postings
# Emilio Lehoucq

######################################### IMPORTING LIBRARIES #########################################
import json
import os
from enrich_world_universities_and_domains import data_world_universities
from functions_helpers import clean_string
from functions_azure import get_response_full_process

######################################### PATHS #########################################
if os.environ.get("PIPELINE_RUN", "0") == "1":
    path_raw_data_folder = "../data/raw/"
    path_prompts_folder = "../prompts/"
else:
    path_raw_data_folder = "data/raw/"
    path_prompts_folder = "prompts/"
path_data_ror = "v1.56-2024-11-19-ror-data.json"
path_data_national_labs = "national_laboratories.json"
path_other_research_orgs = "other_research_organizations.json"
path_prompt = "organization.txt"

######################################### READING DATA #########################################
data_ror = json.load(open(path_raw_data_folder + path_data_ror))
data_national_labs = json.load(open(path_raw_data_folder + path_data_national_labs))
data_other_research_orgs = json.load(open(path_raw_data_folder + path_other_research_orgs))
prompt = open(path_prompts_folder + path_prompt, "r").read()

######################################### FUNCTION DEFINITIONS #########################################

def extract_organization(url, text):
    """
    Function to extract the organization from a job posting.

    Inputs:
        url (str): URL of the job posting.
        text (str): Text of the job posting.
        data (list): List of dictionaries with the data of organizations and their domains.

    Output:
        str: Name of the organization extracted.
    """
    # Check that URL is a string
    if not isinstance(url, str):
        raise ValueError("URL must be a string.")
    
    # Check that text is a string
    if not isinstance(text, str):
        raise ValueError("Text must be a string.")
    
    # Not checking for the data

    # 1) Get the organization from the URL

    # With data_national_labs
    # This one first because list is short
    organization_from_url = extract_organization_from_url(url, data_national_labs, "national_labs")
    if organization_from_url:
        return organization_from_url
    
    # With data_other_research_orgs
    # This one second because list is short
    organization_from_url = extract_organization_from_url(url, data_other_research_orgs, "other_research_orgs")
    if organization_from_url:
        return organization_from_url
    
    # With data_world_universities
    # This one third because list is long
    organization_from_url = extract_organization_from_url(url, data_world_universities, "world_universities")
    if organization_from_url:
        return organization_from_url
    
    # # With data_ror
    # # This slows down the script significantly
    # # It increases the accuracy by a tiny bit, but also introducing errors
    # # Not worth it
    # organization_from_url = extract_organization_from_url(url, data_ror, "ror")
    # if organization_from_url:
    #     return organization_from_url
    
    # 2) Get the organization from the text

    # With data_world_universities
    # This for sure slows down the script
    # Starting with only US universities would be faster
    organization_from_text = extract_organization_from_text(text, data_world_universities)
    if organization_from_text:
        return organization_from_text
    
    # With data_ror
    # This one second because list is long. It slows down the script even more
    # It decreases the accuracy by introducing errors. Don't use it.
    organization_from_text = extract_organization_from_text(text, data_ror, "ror")
    if organization_from_text:
        return organization_from_text
    
    # 3) Using LLM
    # This can be pretty slow, but hopefully at this point there are few organizations to extract
    return extract_organization_from_text(text, None, llm=True)

def extract_organization_from_url(url, data, data_name):
    """
    Function to get an organization name from the URL, if found in the data.

    Inputs:
        url (str): URL of the job posting.
        data (list): List of dictionaries with the data of organizations and their domains.
        data_name (str): Name of the data.
    Output: 
        str: Name of the organization extracted. Otherwise, None.
    """
    # Check that URL is a string
    if not isinstance(url, str):
        raise ValueError("URL must be a string.")
    
    # Not checking for the data

    # Defining keys
    if data_name == "world_universities" or data_name == "national_labs" or data_name == "other_research_orgs":
        key_name = "name"
        key_domains = "domains"
    elif data_name == "ror":
        key_name = "name"
        key_domains = "links"
    
    # Defining variable to store matches
    matching_domains = []

    # Iterate over organizations in data
    for record in data:
        # Iterate over domains of the organization
        for domain in record[key_domains]:
            if data_name == "ror":
                # Clean the URL
                domain = clean_url(url)
            # Check if domain is in the URL
            if domain in url:
                matching_domains.append(domain)

    # If there are matches
    if matching_domains:
        # Find the longest match
        longest_match = max(matching_domains, key=len)

        # Find the organization name corresponding to the longest match
        for record in data:
            for domain in record[key_domains]:
                if data_name == "ror":
                    domain = clean_url(domain)
                if domain == longest_match:
                    return record[key_name]
                
def clean_url(url):
    """
    Function to clean a URL.

    Inputs:
        url (str): URL to clean.

    Output:
        str: Cleaned URL.
    """
    # Check that URL is a string
    if not isinstance(url, str):
        raise ValueError("URL must be a string.")
    
    # Remove http, https, www, etc.

    # Beginnings to remove
    beginnings_to_remove = ["http://www.", "https://www.", "www.", "http://", "https://"]

    # Iterate over beginnings to remove
    for beginning in beginnings_to_remove:
        if url.startswith(beginning):
            url = url.replace(beginning, "")

    # Remove everything after the first slash
    if "/" in url:
        url = url.split("/")[0]

    # If there is more than one dot, remove everything before the first one
    if url.count(".") > 1:
        url = url.split(".", 1)[1]

    return url

def extract_organization_from_text(text, data, data_name=None, llm=False):
    """
    Function to get an organization name from the text, if found in the data.

    Inputs:
        text (str): Text of the job posting.
        data (list): List of dictionaries with the data of organizations and their domains.
        data_name (str): Name of the data.
        llm (bool): Whether to use LLM to extract the organization.

    Output:
        str: Name of the organization extracted. Otherwise, None.
    """
    # Check that text is a string
    if not isinstance(text, str):
        raise ValueError("Text must be a string.")
    
    # Not checking for the data

    # Check that data_name is a string
    if data_name and not isinstance(data_name, str):
        raise ValueError("Data name must be a string.")
    
    # Check that llm is a boolean
    if not isinstance(llm, bool):
        raise ValueError("LLM must be a boolean.")

    # Take the beginning of the text (where the organization name is most likely to be)
    text = extract_beginning_text(text, 20, 1500)

    # If LLM is True
    if llm:
        # Use LLM to extract the organization
        return get_response_full_process(prompt, text, 5, 5, 10, 0.5)

    # Defining variable to store matches
    matching_names = []

    # Iterate over organizations in data
    for record in data:
        # If it's the ROR data
        if data_name == "ror":
            # Clean the name
            record["name"] = clean_ror_name(record["name"])
            # Check if the name of the organization is in the text
            # Not using clean_string here because it led to false matches
            if str(record["name"]) in text:
                matching_names.append(record["name"])
        else:
            # Check if the name of the organization is in the text
            record_name_clean = clean_string(record["name"])
            text_clean = clean_string(text)
            # Checking whether they're not None, because clean_string can return None
            if record_name_clean and text_clean:
                if record_name_clean in text_clean:
                        matching_names.append(record["name"])

    # If there are matches
    if matching_names:
        # Return the longest match 
        # The assumption is that there are a lot of tiny matches that I don't care about (e.g., "42 FR")
        # Not fully sure about this assumption
        return max(matching_names, key=len)

def extract_beginning_text(text, percentage, length):
    """
    Function that returns the maximum of the beginning of a text based on a percentage or a length.

    Inputs:
        text (str): Text to extract the beginning from.
        percentage (int): Percentage of the text to extract.
        length (int): Length of the text to extract (number of characters).

    Output:
        str: Extracted text.
    """
    # Convert text to string
    text = str(text)

    # Check that percentage is an integer
    if not isinstance(percentage, int):
        raise ValueError("Percentage must be an integer.")
    
    # Check that length is an integer
    if not isinstance(length, int):
        raise ValueError("Length must be an integer.")
    
    return text[ :max(int(len(text) * percentage / 100), length)]

def clean_ror_name(name):
    """
    Function to clean a name from the ROR data.
    
    Inputs:
        name (str): Name to clean.
        
    Output:
        str: Cleaned name.
    """
    # Convert to string
    name = str(name)
    
    # If there are parentheses in the name 
    if "(" in name and ")" in name:
        # Remove the parentheses and everything inside
        name = name.split("(", 1)[0] + name.split(")", 1)[1]

    # Remove leading and trailing whitespaces
    name = name.strip()

    # Check that the name is of a certain length
    # This is to avoid matches such as "Engineering", "Software", "Informa", "Biotech", etc.
    if len(name) >= 13:
        # If the name is not a number, return it
        if not name.isdigit():
            return name

if __name__ == "__main__":
    print("Module to extract organization from job postings running as main script.")
    print("Running tests...")

    ##################################################################################
    print("Tests for extract_organization_from_url function:")

    print("Test 1")
    text = "https://www.it.northwestern.edu/departments/it-services-support/research/research-events.html"
    print(extract_organization_from_url(text, data_world_universities, "world_universities"))
    assert extract_organization_from_url(text, data_world_universities, "world_universities") == "Northwestern University"

    print("Test 2")
    text = ""
    print(extract_organization_from_url(text, data_world_universities, "world_universities"))
    assert extract_organization_from_url(text, data_world_universities, "world_universities") == None

    print("Test 3")
    text = "https://talent.stjude.org/careers/jobs/10425?lang=en-us"
    print(extract_organization_from_url(text, data_ror, "ror"))
    assert extract_organization_from_url(text, data_ror, "ror") == "St. Jude Children's Research Hospital"

    ##################################################################################
    print("Tests for extract_organization function:")

    print("Test 1")
    url = "https://www.it.northwestern.edu/departments/it-services-support/research/research-events.html"
    text = ""
    print(extract_organization(url, text))
    assert extract_organization(url, text) == "Northwestern University"

    print("Test 3")
    url = "https://hr.wisc.edu/pvl/	"
    text = ""
    print(extract_organization(url, text))
    assert extract_organization(url, text) == "University of Wisconsin - Madison"

    print("Test 4")
    url = "https://careers.jhuapl.edu/jobs/53940?lang=en-us	"
    text = ""
    print(extract_organization(url, text))
    assert extract_organization(url, text) == "Johns Hopkins University"

    print("Test 5")
    url = "https://jobs.mines.edu/cw/en-us/job/496000/manager-research-infrastructure-services	"
    text = ""
    print(extract_organization(url, text))
    assert extract_organization(url, text) == "Mines & Golden"

    print("Test 6")
    url = "https://jobs.ornl.gov/job/Oak-Ridge-Senior-Research-Software-Engineer-Application-Engineering-TN-37830/898600400/	"
    text = ""
    print(extract_organization(url, text))
    assert extract_organization(url, text) == "Oak Ridge National Laboratory"

    print("Test 7")
    url = "https://gianttiger.wd3.myworkdayjobs.com/gianttiger/job/Ottawa-Home-Office-Ontario-Canada/Manager-of-Data-Sciences_JR112562	"
    text = ""
    print(extract_organization(url, text))
    assert extract_organization(url, text) == "Giant Tiger"

    print("Test 8")
    url = "https://nwu.ci.hr/applicant/index.php?controller=Listings&method=view&listingid=aca9c99c-dd7a-4e1a-8871-4e6844954d43"
    text = ""
    print(extract_organization(url, text))
    assert extract_organization(url, text) == "North-West University"

    print("Test 9")
    url = ""
    text = "(35) PhD Research Software Developer/Senior Scientist | Simon Fraser University | LinkedIn"
    print(extract_organization(url, text))
    assert extract_organization(url, text) == "Simon Fraser University"

    print("Test 10")
    url = ""
    text = "The Alan Turing Institute is great."
    print(extract_organization(url, text))
    assert extract_organization(url, text) == "The Alan Turing Institute"

    # # Commenting this test to not keep sending requests to the API
    # print("Test 11")
    # url = ""
    # text = "Lehoucq Institute is hiring."
    # assert extract_organization(url, text) == "lehoucq institute"

    print("Test 12")
    url = ""
    text = "Simons Foundation is hiring."
    print(extract_organization(url, text))
    assert extract_organization(url, text) == "Simons Foundation"

    # # Commenting this test to not keep sending requests to the API
    # print("Test 13")
    # url = "https://apply.interfolio.com/136320"
    # text = ""
    # print(extract_organization(url, text))
    # # this goes to LLM, which said missing

    ##################################################################################
    print("Tests for clean_url function:")

    print("Test 1")
    url = "https://www.stjude.org/"
    print(clean_url(url))
    assert clean_url(url) == "stjude.org"

    print("Test 2")
    url = "https://talent.stjude.org/careers/jobs/10425?lang=en-us"
    print(clean_url(url))
    assert clean_url(url) == "stjude.org"

    print("Test 3")
    url = "https://jobs.ornl.gov/job/Oak-Ridge-Senior-Research-Software-Engineer-Application-Engineering-TN-37830/898600400/"
    print(clean_url(url))
    assert clean_url(url) == "ornl.gov"

    ##################################################################################
    print("Tests for extract_organization_from_text function:")

    print("Test 1")
    text = "(35) PhD Research Software Developer/Senior Scientist | Simon Fraser University | LinkedIn"
    print(extract_organization_from_text(text, data_world_universities))
    assert extract_organization_from_text(text, data_world_universities) == "Simon Fraser University"

    print("Test 2")
    text = "The Alan Turing Institute is great."
    print(extract_organization_from_text(text, data_ror, "ror"))
    assert extract_organization_from_text(text, data_ror, "ror") == "The Alan Turing Institute"

    # # Commenting this test to not keep sending requests to the API
    # print("Test 3")
    # text = "Northwestern University is hiring."
    # assert extract_organization_from_text(text, None, llm=True) == "northwestern university"

    ##################################################################################
    print("Tests for extract_beginning_text function:")

    print("Test 1")
    text = "This is a test text."
    percentage = 50
    length = 1000
    print(extract_beginning_text(text, percentage, length))
    assert extract_beginning_text(text, percentage, length) == "This is a test text."

    print("Test 2")
    text = "This is a test text."
    percentage = 50
    length = 2
    print(extract_beginning_text(text, percentage, length))
    assert extract_beginning_text(text, percentage, length) == "This is a "

    print("Test 3")
    text = "(35) PhD Research Software Developer/Senior Scientist | Simon Fraser University | LinkedIn"
    percentage = 20
    length = 1500
    print(extract_beginning_text(text, percentage, length))
    assert extract_beginning_text(text, percentage, length) == "(35) PhD Research Software Developer/Senior Scientist | Simon Fraser University | LinkedIn"

    ##################################################################################
    print("Tests for clean_ror_name function:")

    print("Test 1")
    name = "INRA Transfert (France)"
    print(clean_ror_name(name))
    assert clean_ror_name(name) == "INRA Transfert"

    ##################################################################################
    print("All tests passed.")