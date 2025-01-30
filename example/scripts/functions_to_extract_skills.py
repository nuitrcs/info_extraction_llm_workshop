# Script with functions to extract skills from job postings
# Emilio Lehoucq

######################################### IMPORTING LIBRARIES #########################################
import re

######################################### PARAMETERS #########################################

CHARACTERS_AROUND_MATCH = 450

KEYWORDS_SKILLS = [
    "competencies",
    "proficiencies",
    "requirements",
    "expertise",
    "capabilities",
    "nice to have",
    "skills",
    "desired",
    "ideal candidate",
    "proven ability",
    "track record",
    "experience",
    "background",
    "qualifications",
    "degree",
    "certif",
    "credentials",
    "required",
    "preferred",
    "abilities",
    "knowledge",
    "education",
    "must have",
    "should have",
    "need to have",
    "must be",
    "should be",
    "need to be",
]

######################################### FUNCTION DEFINITIONS #########################################

def get_matches(list_keywords, text, case_sensitive=False, char_before=CHARACTERS_AROUND_MATCH, char_after=CHARACTERS_AROUND_MATCH, word_boundaries=False):
    """
    Function to get matches if text contains any of the keywords in a list.

    Inputs:
    - list_keywords (list of str) - List of keywords to check.
    - text (str) - Text to check.
    - case_sensitive (bool) - If True, the check is case sensitive.
    - char_before (int) - Number of characters before the match to consider.
    - char_after (int) - Number of characters after the match to consider.

    Output: matches (list of str) - List of matches.
    """
    # Check that the input is a string
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    if word_boundaries:
        # Create a regex pattern for the keywords with word boundaries
        if case_sensitive:
            pattern = re.compile(r"\b(" + r"|".join([re.escape(keyword) for keyword in list_keywords]) + r")\b")
        else:
            pattern = re.compile(r"\b(" + r"|".join([re.escape(keyword) for keyword in list_keywords]) + r")\b", re.IGNORECASE)
    else:
        # Create a regex pattern for the keywords
        if case_sensitive:
            pattern = re.compile(r"|".join([re.escape(keyword) for keyword in list_keywords]))
        else:
            pattern = re.compile(r"|".join([re.escape(keyword) for keyword in list_keywords]), re.IGNORECASE)

    # Find all matches of the keywords
    matches = pattern.finditer(text)

    # Variable to store the matches
    matches_list = []

    # Check if any of the matches are close to the skills keywords
    for match in matches:
        # Extract the characters around the match
        start_index = max(match.start() - CHARACTERS_AROUND_MATCH, 0)
        end_index = min(match.end() + CHARACTERS_AROUND_MATCH, len(text))
        surrounding_text = text[start_index:end_index].lower()

        # Check if any of the skill keywords are in the surrounding text
        if any(keyword in surrounding_text for keyword in KEYWORDS_SKILLS):
            matches_list.append(match.group())
        
    # Return unique elements in alphabetical order
    return sorted(list(set(matches_list)))

def check_phd(text, char_before=CHARACTERS_AROUND_MATCH, char_after=CHARACTERS_AROUND_MATCH):
    """
    Function to check if text makes reference to PhD.

    Input: text (str) - Text of a job posting.
    Output: has_phd (bool) - True if text makes reference to PhD, False otherwise.
    """
    # List of keywords to check
    phd_keywords = ["PhD", "Ph.D", "Ph.D.", "Doctorate", "Doctoral"]

    # Return True if any of the keywords are in the text
    return len(get_matches(phd_keywords, text, case_sensitive=False, char_before=char_before, char_after=char_after)) > 0

def extract_programming_languages(text, char_before=CHARACTERS_AROUND_MATCH, char_after=CHARACTERS_AROUND_MATCH):
    """
    Function to extract programming languages from text.

    Input: text (str) - Text of a job posting.
    Output: programming_languages (list of str) - List of programming languages.
    """
    # List of programming languages (from ChatGPT)
    common_programming_languages_highered_research = [
        "Python",
        "JavaScript",
        "Java",
        "C#",
        "C++",
        " C ",
        " C,",
        "Ruby",
        "PHP",
        "Swift",
        "Kotlin",
        " R ",
        " R,",      
        "Go",
        "TypeScript",
        "Rust",
        "SQL",
        "Perl",
        "Scala",
        "Dart",
        "MATLAB",
        "Shell",
        "Julia",       # Common in scientific computing and research
        "Fortran",     # Still widely used in scientific research
        "SAS",         # Used for statistical analysis
        "SPSS",        # Popular for research and data analysis
        "Stata",       # Statistical software used in research
        "LaTeX",       # For creating technical and scientific documentation
        "Lisp",        # Occasionally used in AI and academic research
        "Prolog"       # Common in logic programming and research
    ]

    matches = get_matches(common_programming_languages_highered_research, text, case_sensitive=True, char_before=char_before, char_after=char_after, word_boundaries=False)

    # Remove any white spaces or commas 
    matches_clean = [match.strip().replace(",", "") for match in matches]

    # Return clean matches
    return sorted(list(set(matches_clean)))

if __name__ == "__main__":
    print("Module to extract skills from job postings running as main script.")
    print("Running tests...")
    
    ##################################################################################
    print("Tests for check_phd function:")

    print("Test 1")
    text = "The candidate must have a PhD."
    print(check_phd(text))
    assert check_phd(text) == True

    print("Test 2")
    text = "The candidate must have a master's degree."
    print(check_phd(text))
    assert check_phd(text) == False

    print("Test 3")
    text = "PhD"
    print(check_phd(text))
    assert check_phd(text) == False

    print("Test 4")
    text = "phd required"
    print(check_phd(text))
    assert check_phd(text) == True

    ##################################################################################
    print("Tests for get_matches function:")

    print("Test 1")
    text = "The ideal candidate should have a proven track record of success."
    print(get_matches(["track record"], text, case_sensitive=False, char_before=CHARACTERS_AROUND_MATCH, char_after=CHARACTERS_AROUND_MATCH))
    assert get_matches(["track record"], text, case_sensitive=False, char_before=CHARACTERS_AROUND_MATCH, char_after=CHARACTERS_AROUND_MATCH) == ["track record"]

    print("Test 2")
    text = "The ideal candidate should have a proven track record of success."
    print(get_matches(["track record", "success"], text, case_sensitive=False, char_before=CHARACTERS_AROUND_MATCH, char_after=CHARACTERS_AROUND_MATCH))
    assert get_matches(["track record", "success"], text, case_sensitive=False, char_before=CHARACTERS_AROUND_MATCH, char_after=CHARACTERS_AROUND_MATCH) == ['success', 'track record']

    print("Test 3")
    text = "The ideal candidate should have a proven track record of success."
    print(get_matches(["R"], text, case_sensitive=True, char_before=CHARACTERS_AROUND_MATCH, char_after=CHARACTERS_AROUND_MATCH))
    assert get_matches(["R"], text, case_sensitive=True, char_before=CHARACTERS_AROUND_MATCH, char_after=CHARACTERS_AROUND_MATCH) == []

    ##################################################################################
    print("Tests for extract_programming_languages function:")

    print("Test 1")
    text = "The candidate must have experience with Python, R, and SQL."
    print(extract_programming_languages(text))
    assert extract_programming_languages(text) == ['Python', 'R', 'SQL']

    print("Test 2")
    text = "The candidate must have experience with Python, r, and SQL."
    print(extract_programming_languages(text))
    assert extract_programming_languages(text) == ["Python", "SQL"]

    print("Test 3")
    text = "The Candidate must have experience with python, r, and sql."
    print(extract_programming_languages(text))
    assert extract_programming_languages(text) == []

    ##################################################################################
    print("All tests passed.")