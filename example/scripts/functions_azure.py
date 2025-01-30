# Script with functions to interact with Azure services
# Emilio Lehoucq

######################################### IMPORTING LIBRARIES #########################################
from dotenv import load_dotenv
import os
from openai import AzureOpenAI
from time import sleep

######################################### PATHS #########################################
if os.environ.get("PIPELINE_RUN", "0") == "1":
    path_prompts_folder = "../prompts/"
else:
    path_prompts_folder = "prompts/"
path_system_message = "system.txt"

######################################### READING DATA #########################################
system_message = open(path_prompts_folder + path_system_message, "r").read()

######################################### PARAMETERS #########################################
# Get endpoint and API key from .env file
load_dotenv()
azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
azure_key = os.getenv('AZURE_OPENAI_API_KEY')

# Other variables
api_version = "2024-06-01" # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference
# deployment_name = "gpt-35-turbo-0125"
deployment_name = "gpt-4o"

# Initialize client
client = AzureOpenAI(azure_endpoint=azure_endpoint, api_key=azure_key, api_version=api_version)

# Sleep time
sleep_time = 2

######################################### FUNCTIONS #########################################
def get_model_response(user_message, num_retries_failure):
    """
    Function to get a response from an OpenAI model.

    Input:
    - message (str): string with the message to send to the model.
    - num_retries (int): number of retries allowed if there's a problem getting the response.

    Output:
    - response_content (str): string with the response from the model.
    """
    # Check if the input message is a string
    if not isinstance(user_message, str):
        raise TypeError("The input message must be a string.")
    
    # Check if the number of retries is an integer
    if not isinstance(num_retries_failure, int):
        raise TypeError("The number of retries must be an integer.")
    
    # Check if the number of retries is positive
    if num_retries_failure < 0:
        raise ValueError("The number of retries must be a positive integer.")
        
    # Iterate over the number of retries
    for i in range(num_retries_failure):

        try:
    
            # Get response
            response = client.chat.completions.create(
                model=deployment_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                    ]
                )

            # Get the response content
            response_content = response.choices[0].message.content

            return response_content
        
        except Exception as e:

            print("Error:", e)
            sleep(sleep_time)

def get_model_response_with_text(prompt, text, num_retries_failure):
    """
    Function to get a response from an OpenAI model with a text.

    Inputs:
    - prompt (str): string with the prompt to send to the model.
    - text (str): string with the text to send to the model.
    - num_retries_failure (int): number of retries allowed if there's a problem getting the response.

    Output:
    - response_content (str): string with the response from the model.
    """
    # Check if the input prompt is a string
    if not isinstance(prompt, str):
        raise TypeError("The input prompt must be a string.")
    
    # Check if the input text is a string
    if not isinstance(text, str):
        raise TypeError("The input text must be a string.")
    
    # Check if the number of retries is an integer
    if not isinstance(num_retries_failure, int):
        raise TypeError("The number of retries must be an integer.")
    
    # Check if the number of retries is positive
    if num_retries_failure < 0:
        raise ValueError("The number of retries must be a positive integer.")
    
    return get_model_response(prompt + "\n\n" + text, num_retries_failure)

def check_correct_format(response):
    """
    Check if the response from a model is in the correct format.

    The correct format is defined as starting with "Reasoning:" and containing "My answer is: ".

    Input:
    - response (str): The response to check.

    Output:
    - bool: True if the response is in the correct format, False otherwise.
    """
    # Check if the input is a string
    if not isinstance(response, str):
        raise TypeError("Response must be a string.")
    
    # Check if the string starts with "Reasoning:" and contains "My answer is: "
    return response[:10] == "Reasoning:" and "My answer is: " in response

def get_response_checking_format(prompt, text, num_retries_failure, num_retries_format):
    """
    Function to get a response from an OpenAI model and check if the response is correct.

    Inputs:
    - prompt (str): string with the prompt to send to the model.
    - text (str): string with the text to send to the model.
    - num_retries_failure (int): number of retries allowed if there's a problem getting the response.
    - num_retries (int): number of retries to get a correct response.

    Output:
    - response_content (str): string with the response from the model.
    """
    # Check if the input prompt is a string
    if not isinstance(prompt, str):
        raise TypeError("The input prompt must be a string.")
    
    # Check if the input text is a string
    if not isinstance(text, str):
        raise TypeError("The input text must be a string.")
    
    # Check if the number of retries is an integer
    if not isinstance(num_retries_failure, int):
        raise TypeError("The number of retries must be an integer.")
    
    # Check if the number of retries is positive
    if num_retries_failure < 0:
        raise ValueError("The number of retries must be a positive integer.")
    
    # Check if the number of retries is an integer
    if not isinstance(num_retries_format, int):
        raise TypeError("The number of retries must be an integer.")
    
    # Check if the number of retries is positive
    if num_retries_format < 0:
        raise ValueError("The number of retries must be a positive integer.")
    
    # Iterate over the number of retries
    for i in range(num_retries_format):

        # Get response
        response = get_model_response_with_text(prompt, text, num_retries_failure)
        
        # Check if the response is in the correct format
        if check_correct_format(response):
            return get_relevant_part_response(response)
        
        # Sleep
        sleep(sleep_time)
        
    return "problem_with_response"

def get_relevant_part_response(response):
    """
    Get the relevant part of the response.

    Input:
    - response (str): The response to check.

    Output:
    - relevant_part (str): The relevant part of the response.
    """
    # Check if the input is a string
    if not isinstance(response, str):
        raise TypeError("Response must be a string.")
    
    # Check if the response is in the correct format
    if not check_correct_format(response):
        raise ValueError("The response is not in the correct format.")
    
    # Get the relevant part of the response
    # The relevant part is the part after "My answer is: " and before "." (if there is)
    response = response.split("My answer is: ")[1].split(".")[0]

    # Remove leading and trailing whitespaces
    response = response.strip()

    return response

def get_multiple_responses(prompt, text, num_retries_failure, num_retries_format, num_responses):
    """
    Function to get multiple responses from an OpenAI model and check if the responses are correct.

    Inputs:
    - prompt (str): string with the prompt to send to the model.
    - text (str): string with the text to send to the model.
    - num_retries (int): number of retries to get a correct response.
    - num_responses (int): number of responses to get.

    Output:
    - responses (list): list with the responses from the model.
    """
    # Check if the input prompt is a string
    if not isinstance(prompt, str):
        raise TypeError("The input prompt must be a string.")
    
    # Check if the input text is a string
    if not isinstance(text, str):
        raise TypeError("The input text must be a string.")
    
    # Check if the number of retries is an integer
    if not isinstance(num_retries_failure, int):
        raise TypeError("The number of retries must be an integer.")
    
    # Check if the number of retries is positive
    if num_retries_failure < 0:
        raise ValueError("The number of retries must be a positive integer.")
    
    # Check if the number of retries is an integer
    if not isinstance(num_retries_format, int):
        raise TypeError("The number of retries must be an integer.")
    
    # Check if the number of retries is positive
    if num_retries_format < 0:
        raise ValueError("The number of retries must be a positive integer.")
    
    # Check if the number of responses is an integer
    if not isinstance(num_responses, int):
        raise TypeError("The number of responses must be an integer.")
    
    # Check if the number of responses is positive
    if num_responses < 0:
        raise ValueError("The number of responses must be a positive integer.")
    
    # Initialize list to store responses
    responses = []

    # Iterate over the number of responses
    for i in range(num_responses):

        # Get response
        response = get_response_checking_format(prompt, text, num_retries_failure, num_retries_format)
        
        # Append response to list of responses
        responses.append(response)

        # Sleep
        sleep(sleep_time)

    return responses

def get_majority_response(responses, prop_majority):
    """
    Function to get the majority response from a list of responses.

    Inputs:
    - responses (list): list with the responses to check.
    - prop_majority (float): proportion of responses that must match.

    Output:
    - majority_response (str): string with the majority response.
    """
    # Check if the input responses is a list
    if not isinstance(responses, list):
        raise TypeError("Responses must be a list.")
    
    # Check if the input proportion is a number
    if not isinstance(prop_majority, (int, float)):
        raise TypeError("The proportion must be a number.")
    
    # Check if the input proportion is between 0 and 1
    if prop_majority < 0 or prop_majority > 1:
        raise ValueError("The proportion must be between 0 and 1.")
    
    # Initialize dictionary to store the count of each response
    response_count = {}

    # Iterate over the responses
    for response in responses:

        # Clean response
        response_clean = clean_response_string(response)

        # Check if the cleaned response is in the dictionary
        if response_clean in response_count:
            response_count[response_clean] += 1
        else:
            response_count[response_clean] = 1

    # Get the response with the highest count
    majority_response = max(response_count, key=response_count.get)

    # Check if the proportion of the majority response is greater than the input proportion
    if response_count[majority_response] / len(responses) >= prop_majority:
        return majority_response

def clean_response_string(response):
    """
    Function to clean a response string.

    Inputs:
    - response (str): string with the response to clean.

    Output:
    - response (str): string with the cleaned response.
    """
    # Check if the input is a string
    if not isinstance(response, str):
        raise TypeError("Response must be a string.")
    
    # Remove leading and trailing whitespaces
    response = response.strip()

    # Lowercase 
    response = response.lower()

    return response

def get_response_full_process(prompt, text, num_retries_failure, num_retries_format, num_responses, prop_majority):
    """
    Function to get a response from an OpenAI model and check if the response is correct.

    Inputs:
    - prompt (str): string with the prompt to send to the model.
    - text (str): string with the text to send to the model.
    - num_retries_failure (int): number of retries allowed if there's a problem getting the response.
    - num_retries (int): number of retries to get a correct response.
    - num_responses (int): number of responses to get.
    - prop_majority (float): proportion of responses that must match.

    Output:
    - response_content (str): string with the response from the model.
    """
    # Check if the input prompt is a string
    if not isinstance(prompt, str):
        raise TypeError("The input prompt must be a string.")
    
    # Check if the input text is a string
    if not isinstance(text, str):
        raise TypeError("The input text must be a string.")

    # Check if the number of retries is an integer
    if not isinstance(num_retries_failure, int):
        raise TypeError("The number of retries must be an integer.")
    
    # Check if the number of retries is positive
    if num_retries_failure < 0:
        raise ValueError("The number of retries must be a positive integer.")
    
    # Check if the number of retries is an integer
    if not isinstance(num_retries_format, int):
        raise TypeError("The number of retries must be an integer.")
    
    # Check if the number of retries is positive
    if num_retries_format < 0:
        raise ValueError("The number of retries must be a positive integer.")
    
    # Check if the number of responses is an integer
    if not isinstance(num_responses, int):
        raise TypeError("The number of responses must be an integer.")
    
    # Check if the number of responses is positive
    if num_responses < 0:
        raise ValueError("The number of responses must be a positive integer.")
    
    # Check if the input proportion is a number
    if not isinstance(prop_majority, (int, float)):
        raise TypeError("The proportion must be a number.")
    
    # Check if the input proportion is between 0 and 1
    if prop_majority < 0 or prop_majority > 1:
        raise ValueError("The proportion must be between 0 and 1.")
    
    # Get multiple responses
    responses = get_multiple_responses(prompt, text, num_retries_failure, num_retries_format, num_responses)
    
    # Get majority response
    majority_response = get_majority_response(responses, prop_majority)

    return majority_response

if __name__ == "__main__":
    print("Module with functions to interact with Azure services running as main.")
    print("Running tests...")

    ##################################################################################
    print("Tests for check_correct_format function:")

    print("Test 1")
    response = "Reasoning: My answer is: 42."
    print(check_correct_format(response))
    assert check_correct_format(response) == True

    print("Test 2")
    response = "Reasoning: My answer is:42."
    print(check_correct_format(response))
    assert check_correct_format(response) == False

    ##################################################################################
    print("Tests for clean_response_string function:")

    print("Test 1")
    response = " 42 "
    print(clean_response_string(response))
    assert clean_response_string(response) == "42"

    print("Test 2")
    response = "CAPITAL"
    print(clean_response_string(response))
    assert clean_response_string(response) == "capital"

    ##################################################################################
    print("Tests for get_majority_response function:")

    print("Test 1")
    responses = ["42", "42", "42", "43"]
    prop_majority = 0.5
    print(get_majority_response(responses, prop_majority))
    assert get_majority_response(responses, prop_majority) == "42"

    print("Test 2")
    responses = ["42  ", "42         ", "42", "43"]
    prop_majority = 0.5
    print(get_majority_response(responses, prop_majority))
    assert get_majority_response(responses, prop_majority) == "42"

    print("Test 3")
    responses = ["HELLO", "hello", "Hello", "hello"]
    prop_majority = 1.0
    print(get_majority_response(responses, prop_majority))
    assert get_majority_response(responses, prop_majority) == "hello"

    ##################################################################################
    # print("Tests for get_model_response function:")

    # print("Test 1")
    # user_message = "What is the capital of France?"
    # num_retries_failure = 2
    # assert "paris" in get_model_response(user_message, num_retries_failure).lower()

    ##################################################################################
    # print("Tests for get_model_response_with_text function:")

    # print("Test 1")
    # prompt = "What is the capital of France?"
    # text = "The capital of France is Paris."
    # num_retries_failure = 2
    # assert "paris" in get_model_response_with_text(prompt, text, num_retries_failure).lower()

    ##################################################################################
    print("Tests for get_relevant_part_response function:")

    print("Test 1")
    response = "Reasoning: My answer is: 42  "
    print(get_relevant_part_response(response))
    assert get_relevant_part_response(response) == "42"

    print("Test 2")
    response = "Reasoning: My answer is: 42."
    print(get_relevant_part_response(response))
    assert get_relevant_part_response(response) == "42"

    print("Test 3")
    response = "Reasoning: My answer is:       42    . "
    print(get_relevant_part_response(response))
    assert get_relevant_part_response(response) == "42"

    ##################################################################################
    # print("Tests for get_response_checking_format function:")

    # print("Test 1")
    # prompt = "What is the capital of France?"
    # text = "The capital of France is Paris."
    # num_retries_failure = 2
    # num_retries_format = 2
    # assert get_response_checking_format(prompt, text, num_retries_failure, num_retries_format).lower() == "paris"

    ##################################################################################
    # print("Tests for get_multiple_responses function:")

    # print("Test 1")
    # prompt = "What is the capital of France?"
    # text = "The capital of France is Paris."
    # num_retries_failure = 2
    # num_retries_format = 2
    # num_responses = 5
    # assert [response.lower() for response in get_multiple_responses(prompt, text, num_retries_failure, num_retries_format, num_responses)] == ["paris"] * num_responses

    ##################################################################################
    # print("Tests for get_response_full_process function:")

    # print("Test 1")
    # prompt = "What is the capital of France?"
    # text = "The capital of France is Paris."
    # num_retries_failure = 2
    # num_retries_format = 2
    # num_responses = 5
    # prop_majority = 0.5
    # assert get_response_full_process(prompt, text, num_retries_failure, num_retries_format, num_responses, prop_majority) == "paris"
    
    ##################################################################################
    print("All tests passed.")