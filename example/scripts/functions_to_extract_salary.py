# Script with functions to extract salary from job postings
# Emilio Lehoucq

######################################### IMPORTING LIBRARIES #########################################
import re

######################################### FUNCTION DEFINITIONS #########################################

def get_salary_flag(text):
    """
    Function to check if a job posting seems to contain salary information.

    Input: text (str) - job posting text
    Output: info_found (str) or None

    Dependencies: re
    """
    # Check that the input is a string
    if not isinstance(text, str):
        return 'input_is_not_string'
    
    # Lowercase the text
    text = text.lower()
    
    # Check if the text mentions keywords
    if 'salary' in text or 'compensation' in text or 'pay' in text:
        # Pattern for money sign and digits
        pattern = r'[€£$]\s?\d{1,6}'
        # Check if the pattern is found in the text
        flag = re.search(pattern, text)
        # If the pattern is found, return 'money_sign_digits'
        if flag:
            return 'money_sign_digits'
        
        # Pattern for numbers that look like salary
        pattern = r'\b\d{1,3}[,.]?\d{3}\b'
        # Check if the pattern is found in the text
        flag = re.search(pattern, text)
        # If the pattern is found, return 'keyword_numbers'
        if flag:
            return 'keyword_numbers'
        
def extract_salary(text):
    """
    Function to extract salary from the text of a job posting.

    Input: text (str) - Text of a job posting.
    Output: salary_info (list) - List of salary information extracted from the text.

    Dependencies: check_salary_keywords, find_matches, check_hour
    """
    # Check that the input is a string
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    
    # Check if the text contains a keyword indicating that there's salary information
    if not check_salary_keywords(text):
        return None
    
    # Check for various possible patterns
    
    # $30,000 - $40,000
    regex_1 = r'[€£$]\s?\d{1,3}[,.]?\d{3}(?:\.\d{2})?\s?(?:-|–|up to|to|and)\s?[€£$]?\s?\d{1,3}[,.]?\d{3}(?:\.\d{2})?'
    salary_info_1 = find_matches(text, regex_1)

    # $30k - $40k
    regex_2 = r'[€£$]\s?\d{1,3}[kK]?\s?(?:-|–|up to|to|and)\s?[€£$]?\s?\d{1,3}[kK]?'
    salary_info_2 = find_matches(text, regex_2)

    # 30,000 - 40,000
    regex_3 = r'\d{2,3}[,.]?\d{3}(?:\.\d{2})?\s?(?:-|–|up to|to|and)\s?\d{2,3}[,.]?\d{3}(?:\.\d{2})?'
    salary_info_3 = find_matches(text, regex_3)

    # $30,000
    regex_4 = r'[€£$]\s?\d{2,3}[,.]?\d{3}(?:\.\d{2})?'
    salary_info_4 = find_matches(text, regex_4)

    # 30,000
    regex_5 = r'\d{2,3},?\d{3}\.\d{2}'
    salary_info_5 = find_matches(text, regex_5)

    # $3,000
    regex_6 = r'[€£$]\s?\d{1,2}[,.]?\d{3}(?:\.\d{2})?'
    salary_info_6 = find_matches(text, regex_6)

    # 3,000
    regex_7 = r'\d{1,2},?\d{3}\.\d{2}'
    salary_info_7 = find_matches(text, regex_7)

    # $10 - $20
    # regex_8 = r'[€£$]\s?\d{2}(?:\.\d{2})?\s?(?!\s?M)\s?(?:-|–|up to|to|and)\s?[€£$]\s?\d{2}(?:\.\d{2})?\s?(?!\s?M)'
    regex_8 = r'[€£$]\s?\d{2}(?:\.\d{2})?\s?(?!\s?M)\s?(?:-|–|up to|to|and)\s?[€£$]\s?\d{2}(?:\.\d{2})?(?!\s?M)'
    salary_info_8 = find_matches(text, regex_8)

    # $10 
    # regex_9 = r'[€£$]\s?\d{2}(?:\.\d{2})?\b\s?(?!\s?M)'
    regex_9 = r'[€£$]\s?\d{2}(?:\.\d{2})?\b(?!\s?M)'
    salary_info_9 = find_matches(text, regex_9)

    # Return desired results

    if salary_info_1: # $30,000 - $40,000
        if salary_info_4: # $30,000
            return combine_lists(salary_info_1, salary_info_4)
        else:
            return sorted(list(set(salary_info_1)))

    if salary_info_3: # 30,000 - 40,000
        if salary_info_5: # 30,000
            return combine_lists(salary_info_3, salary_info_5)
        else:
            return sorted(list(set(salary_info_3)))
        
    if salary_info_2: # $30k - $40k
        return sorted(list(set(salary_info_2)))
    
    if salary_info_4: # $30,000
        return sorted(list(set(salary_info_4)))
    
    if salary_info_5: # 30,000
        return sorted(list(set(salary_info_5)))
    
    if salary_info_6: # $3,000
        if not check_harvard(text):
            return sorted(list(set(salary_info_6)))
    
    if salary_info_7: # 3,000
        return sorted(list(set(salary_info_7)))
    
    # Check that the text talks about hour
    if check_hour(text):

        if salary_info_8: # $10 - $20
            return sorted(list(set(salary_info_8)))
        
        if salary_info_9: # $10
            if not check_harvard(text):
                return sorted(list(set(salary_info_9)))

def check_salary_keywords(text):
    """
    Function to check if the text contains keywords indicating that there's salary information.

    Input: text (str) - Text of a job posting.
    Output: has_salary_keywords (bool) - True if the text contains salary keywords, False otherwise.
    """
    # Check that the input is a string
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    
    # List of keywords indicating that there's salary information
    salary_keywords = ["salary", "compensation", "pay", "remuneration", "wage", "hiring range", "offer"]
    
    # Check if the text contains any of the keywords
    has_salary_keywords = any(keyword in text.lower() for keyword in salary_keywords)
    
    return has_salary_keywords

def find_matches(text, regex):
    """
    Function to find all matches of a regular expression in a text.

    Input: text (str) - Text to search for matches.
           regex (str) - Regular expression to search for.
    Outputs: matches (list) - List of matches found in the text.

    Dependencies: re
    """
    # Check that the input is a string
    if not isinstance(text, str) or not isinstance(regex, str):
        raise TypeError("Input must be a string.")
        
    # Find all matches of the regular expression in the text
    matches = re.findall(regex, text)

    # Return matches if there are
    if len(matches) > 0:
        return matches

def check_hour(text):
    """
    Function to check if the text contains keywords indicating that there's hourly salary information.

    Input: text (str) - Text of a job posting.
    Output: has_hour_keywords (bool) - True if the text contains hourly salary keywords, False otherwise.
    """
    # Check that the input is a string
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    
    # List of keywords indicating that there's hourly salary information
    hour_keywords = ["hour", "hr", "/hr"]
    
    # Check if the text contains any of the keywords
    has_hour_keywords = any(keyword in text.lower() for keyword in hour_keywords)
    
    return has_hour_keywords

def combine_lists(list1, list2):
    """
    Combines two lists by:
    1. Keeping items in list2 only if they're not in one of the items in list1.
    2. Combining the two lists.
    3. Removing duplicates and sorting.

    Inputs: list1 (list) - First list.
            list2 (list) - Second list.

    Outputs: combined_list (list) - Combined list.
    """
    # Check that the inputs are lists
    if not isinstance(list1, list) or not isinstance(list2, list):
        raise TypeError("Inputs must be lists.")

    # If the lists are empty, return an empty list
    if len(list1) == 0 and len(list2) == 0:
        return []

    # If one of the lists is empty, return the other list
    if len(list1) == 0:
        return list2
    if len(list2) == 0:
        return list1

    # Remove None from the lists
    list1 = [item for item in list1 if item is not None]
    list2 = [item for item in list2 if item is not None]

    # Check that the items in the lists are strings
    if not all(isinstance(item, str) for item in list1) or not all(isinstance(item, str) for item in list2):
        raise TypeError("Items in the lists must be strings.")

    # Keep items in list2 only if they're not in one of the items in list1
    filtered_list2 = [item for item in list2 if not any(item in s1 for s1 in list1)]

    # Combine the two lists
    combined_list = list1 + filtered_list2

    # Remove duplicates and sort
    return sorted(list(set(combined_list)))

def check_harvard(text):
    """
    Function to check if the text contains "Harvard" and "$5,250" or "$40 per class".

    Input: text (str) - Text of a job posting.
    Output: has_harvard (bool) - True if "Harvard University" and $5,250 in text, False otherwise.
    """
    # Check that the input is a string
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    
    # Check if the text contains "Harvard" and "$5,250" or "$40 per class"
    has_harvard = "Harvard" in text and ("$5,250" in text or "$40 per class" in text)
    
    return has_harvard

if __name__ == "__main__":
    print("Module to extract salary from job postings running as main script.")
    print("Running tests...")

    ##################################################################################
    print("Tests for check_salary_keywords function:")

    print("Test 1")
    text = "We offer a competitive salary."
    print(check_salary_keywords(text))
    assert check_salary_keywords(text) == True

    print("Test 2")
    text = "Bad luck"
    print(check_salary_keywords(text))
    assert check_salary_keywords(text) == False

    ##################################################################################
    print("Tests for find_matches function:")

    print("Test 1")
    text = "The salary is $100,000 per year."
    regex = r"\$\d+"
    print(find_matches(text, regex))
    assert find_matches(text, regex) == ["$100"]

    print("Test 2")
    text = "The salary is $100,000 per year. The salary is $200,000 per year."
    regex = r"\$\d+"
    print(find_matches(text, regex))
    assert find_matches(text, regex) == ["$100", "$200"]

    ##################################################################################
    print("Tests for check_hour function:")

    print("Test 1")
    text = "The salary is $100 per hour."
    print(check_hour(text))
    assert check_hour(text) == True

    print("Test 2")
    text = "The salary is $100 per year."
    print(check_hour(text))
    assert check_hour(text) == False

    ##################################################################################
    print("Tests for combine_lists function:")

    print("Test 1")
    list1 = ["$100", "$200"]
    list2 = ["$300", "$400"]
    print(combine_lists(list1, list2))
    assert combine_lists(list1, list2) == ["$100", "$200", "$300", "$400"]

    print("Test 2")
    list1 = ["$100", "$200"]
    list2 = ["$200", "$300"]
    print(combine_lists(list1, list2))
    assert combine_lists(list1, list2) == ["$100", "$200", "$300"]

    print("Test 3")
    list1 = ["$100", "$200"]
    list2 = ["$200", "$300", None]
    print(combine_lists(list1, list2))
    assert combine_lists(list1, list2) == ["$100", "$200", "$300"]

    print("Test 4")
    list1 = ["$100", "$200"]
    list2 = []
    print(combine_lists(list1, list2))
    assert combine_lists(list1, list2) == ["$100", "$200"]

    print("Test 5")
    list1 = []
    list2 = ["$200", "$300"]
    print(combine_lists(list1, list2))
    assert combine_lists(list1, list2) == ["$200", "$300"]

    ##################################################################################
    print("Tests for check_harvard function:")

    print("Test 1")
    text = "Harvard University is a great place to work $5,250 $40 per class."
    print(check_harvard(text))
    assert check_harvard(text) == True

    print("Test 2")
    text = "Harvard university is a great place to work $5,250 $40 per class."
    print(check_harvard(text))
    assert check_harvard(text) == True

    print("Test 3")
    text = "Salary $5,250 $40 per class"
    print(check_harvard(text))
    assert check_harvard(text) == False

    print("Test 4")
    text = "Tuition Assistance Program (TAP): $40 per class at the Harvard Extension Scho"
    print(check_harvard(text)) 
    assert check_harvard(text) == True

    print("Test 5")
    text = "Senior Research Software Engineer | Harvard University\n O p p o r t u n i t y a w a i t s . . .\n http://sjobs.brassring.com/TGnewUI/Search/home/HomeWithPreLoad?partnerid=25240&siteid=5341&PageType=JobDetails&jobid=1959428&codes=IND\n Skip to main content\n Search for Jobs \n Harvard Human Resources Frequently Asked Questions Equal Employment Opportunity Diversity & Inclusion \n Sign In\n Dark mode Light Mode\n Share\n 11-Oct-2022\n Senior Research Software Engineer\n Harvard University Information Technology \n 58822BR\n Position Description \n This is a fully benefited, full-time Harvard University position that has been funded for one year. There is the possibility of renewal, contingent on funding, university priorities and satisfactory job performance. Harvard University Information Technology (HUIT) is a community of Information Technology professionals committed to delivering service and technological solutions in support of teaching, learning, research and administration. We are recruiting an IT workforce that has both breadth in their ability to collaborate and innovate across disciplines – and depth in specific areas of expertise. HUIT offers opportunities for IT professionals to learn and work in a unique technology landscape and service-focused environment. If you are a technically proficient, nimble, user-focused, and accountable IT professional who also connects with the importance of collaborating well in a team environment, we are looking for you! Founded in 1839, the Harvard College Observatory (HCO) carries on a broad program of research in astronomy and astrophysics, collaborating with the Smithsonian Astrophysical Observatory (SAO) at the Harvard-Smithsonian Center for Astrophysics (CfA) and providing substantial support to Harvard's Department of Astronomy. This position closely collaborates with project leaders in the CfA’s John G. Wolbach Library. The Wolbach Library houses both HCO and SAO collections, forming one of the world’s preeminent astronomical collections. Wolbach’s special collection holdings include primary sources associated with the institution’s history, as well as archival publications, papers, and objects created by observatories worldwide. The Wolbach Library is also the home of Harvard's Astronomical Photographic Glass Plate Collection. The Senior Research Software Engineer (RSE) supports researchers' data and software engineering needs at the Harvard College Observatory, which includes refactoring the data processing pipelines, front-end, and the codebase of the DASCH (Digital Access to a Sky Century at Harvard) project. Researchers at CfA utilize the DASCH platform to digitize the Harvard Astronomical Plate Collection, which provides the capability for a systematic study of the sky on 100-year time scales. This position works within the Research Software Engineering team and reports to the Associate Director of Research Software Engineering. A successful candidate will be able to develop and implement systems and data services that can efficiently process data at scale. Harvard University is looking for candidates with diverse backgrounds and new perspectives to work in University Research Computing and Data for the DASCH project. *For those interested in remote work, this role can be primarily remote. We also have beautiful on-campus space in the heart of Harvard Square for employees who choose to be on-site.*\n Basic Qualifications \n Minimum of seven years’ post-secondary education or relevant work experience\n Additional Qualifications and Skills \n The following Additional Qualifications are strongly preferred. If you meet some, but not all, you are still encouraged to apply; we value employees with a willingness to learn. Knowledge of data structures, data modeling, data aggregation, and data storage. Professional experience building and optimizing data processing pipelines and architectures. Proficient in database language and tools (PostgreSQL, MySQL, MongoDB). Advanced programming skills (Python is preferred). Professional experience with front-end development is a PLUS. Experience with Linux and distributed computing (MPI is preferred) is a PLUS. Basic familiarity with astronomy and its associated data structures is a PLUS. Comfortable working with version control systems such as git. Strong project management and organizational skills. Demonstrated success in working in a cross-functional team in an agile environment.\n Certificates and Licenses \n Completion of Harvard IT Academy specified foundational courses (or external equivalent) preferred\n Working Conditions \n Interview and onboarding activity for this position may be conducted via telephone & Zoom video conferencing, based on the department’s current presence on campus. This position will be a hybrid role with the option to work on campus or remotely as often as desired, with the expectation of attending in-person meeting and collaborative sessions when the opportunity presents itself. HUIT actively supports hybrid work where business and team needs allow. Additional detail will be discussed during the interview process. All remote work must be performed in a state in which Harvard is registered to do business (CA, CT, MA, MD, ME, NH, NY, RI, and VT). The University requires all Harvard community members to be fully vaccinated against COVID-19 and remain up to date with COVID-19 vaccine boosters, as detailed in Harvard’s Vaccine & Booster Requirements . Individuals may claim exemption from the vaccine requirement for medical or religious reasons. More information regarding the University’s COVID vaccination requirement, exemptions, and verification of vaccination status may be found at the University’s “COVID-19 Vaccine Information” webpage: http://www.harvard.edu/coronavirus/covid-19-vaccine-information/ . Harvard continues to place the highest priority on the health, safety and wellbeing of its faculty, staff and students, as well as the wider community. Information and details can be found via Harvard’s Coronavirus Workplace Policies website: https://hr.harvard.edu/corona-virus-workplace-policies .\n Additional Information \n Please provide a cover letter with your application. Please note: Harvard University requires pre-employment reference and background screening. We are unable to provide work authorization and/or visa sponsorship. This position has a 180-day orientation and review period. More about HUIT: Harvard University Information Technology (HUIT) is responsible for the strategy, planning, and delivery of information technology across the University. Our mission is to assure Harvard’s leadership in IT. We strive to make it easier for faculty, students, and staff to teach, research, learn and work through the effective use of information technology. HUIT’s core values are User Focused, Collaborative, Innovative and Open. IT Academy (designed for IT Staff): HUIT’s IT Academy aims to enable each IT staff person to grow professionally and become a trusted partner to her or his team. The IT Academy is built on the belief that every IT staff member across the University (including technology employees at each school and campus) can grow in her or his area of expertise as well as building strong people and project management skills. Learn more here: https://itacademy.harvard.edu/ Total Rewards: Harvard’s Total Rewards Program is designed to attract, retain, and reward the performance of talented employees. As a Harvard staff member, you enjoy many perks that come with working for one of the top employers in Massachusetts, including: Paid Time Off: 3 - 4 weeks accrued vacation days, 12 accrued sick days, 12.5 paid holidays plus winter recess, and 3 personal days awarded each calendar year. Medical/Dental/Vision: We offer a variety of excellent medical plans, dental & vision plans. Retirement: University-funded retirement plan with full vesting after 3 years of service. Tuition Assistance Program (TAP): $40 per class at the Harvard Extension School and discounted options through participating Harvard grad schools. Harvard University Employees Credit Union: Our employees credit union provides a complete line of services for all your financial needs. https://huecu.org Transportation: 50% discounted MBTA pass as well as additional options to assist employees in their daily commute. Wellness options: A variety of programs and classes at little or no cost, including stress management, massages, nutrition, meditation and complimentary health services. Access to athletic facilities, libraries, campus events and many discounts throughout metro Boston. Learn more: https://hr.harvard.edu/totalrewards Accessibility: Harvard University IT plays an important role in supporting Harvard's commitment by seeking to create, procure and deploy technologies that are accessible to all, including and especially those who live with disability. Harvard welcomes individuals with disabilities to apply for positions and participate in its programs and activities. If you would like to request accommodations or have questions about the physical access provided, please contact our University Disability Resources Department.\n Job Function \n Information Technology \n Location \n USA - MA - Cambridge \n Job Code \n I1258P IT RC Software/Data Prof IV \n Sub-Unit \n ------------ \n Department \n University Research Computing\n Time Status \n Full-time \n Salary Grade \n 058\n Union \n 00 - Non Union, Exempt or Temporary \n Pre-Employment Screening \n Identity \n Commitment to Equity, Diversity, Inclusion, and Belonging \n Harvard University views equity, diversity, inclusion, and belonging as the pathway to achieving inclusive excellence and fostering a campus culture where everyone can thrive. We strive to create a community that draws upon the widest possible pool of talent to unify excellence and diversity while fully embracing individuals from varied backgrounds, cultures, races, identities, life experiences, perspectives, beliefs, and values.\n EEO Statement \n We are an equal opportunity employer and all qualified applicants will receive consideration for employment without regard to race, color, religion, sex, national origin, disability status, protected veteran status, gender identity, sexual orientation, pregnancy and pregnancy-related conditions, or any other characteristic protected by law.\n Senior Research Software Engineer | Harvard University\n \n Apply to job \n Save \n Send to friend\n Reasonable Accommodations\n Frequently Asked Questions\n Contact Us\n Digital Accessibility\n Diversity & Inclusion \n Privacy Statement\n Technical Support \n Harvard Schools\n Infinite Talent Privacy Statement"
    print(check_harvard(text))
    assert check_harvard(text) == True

    ##################################################################################
    print("Tests for extract_salary function:")

    print("Test 1")
    text = "salary: $30,000 - $40,000 per year"
    print(extract_salary(text))
    assert extract_salary(text) == ["$30,000 - $40,000"]

    print("Test 2")
    text = "We offer a competitive salary."
    print(extract_salary(text))
    assert extract_salary(text) == None

    print("Test 3")
    text = "salary: $30k - $40k per year"
    print(extract_salary(text))
    assert extract_salary(text) == ["$30k - $40k"]

    print("Test 4")
    text = "salary: 30,000 - 40,000 per year"
    print(extract_salary(text))
    assert extract_salary(text) == ["30,000 - 40,000"]

    print("Test 5")
    text = "salary: $30,000 per year"
    print(extract_salary(text))
    assert extract_salary(text) == ["$30,000"]

    print("Test 6")
    text = "salary: 30,000.00 per year"
    print(extract_salary(text))
    assert extract_salary(text) == ["30,000.00"]

    print("Test 7")
    text = "salary: $3,000 per month"
    print(extract_salary(text))
    assert extract_salary(text) == ["$3,000"]

    print("Test 8")
    text = "salary: 3,000.00 per month"
    print(extract_salary(text))
    assert extract_salary(text) == ["3,000.00"]

    print("Test 9")
    text = "The salary is $10 per hour."
    print(extract_salary(text))
    assert extract_salary(text) == ["$10"]

    print("Test 10")
    text = "The salary is $10 - $20 per hour."
    print(extract_salary(text))
    assert extract_salary(text) == ["$10 - $20"]

    print("Test 11")
    text = "Pay depends on experience. Lower range is $50,000 and higher range is $60,000."
    print(extract_salary(text))
    assert extract_salary(text) == ['$50,000', '$60,000']

    print("Test 12")
    text = "Pay depends on experience. Lower range is $50/hr and higher range is $60/hr."
    print(extract_salary(text))
    assert extract_salary(text) == ['$50', '$60']

    print("Test 13")
    text = "Early career finalist can expect an annual salary of $60,000 - $80,000, mid-career $75,000 - $100,000, and advanced $90,000 or more"
    print(extract_salary(text))
    assert extract_salary(text) == ['$60,000 - $80,000', '$75,000 - $100,000', '$90,000']

    print("Test 14")
    text = "This is not a salary: 217.333.2137"
    print(extract_salary(text))
    assert extract_salary(text) == None

    print("Test 15")
    text = "Renumeration Package $137,322 - $145,480 per annum incl"
    print(extract_salary(text))
    assert extract_salary(text) == None

    print("Test 16")
    text = "de 9 (Hiring Range $73,08.00 to $100,402.00 annually)"
    print(extract_salary(text))
    assert extract_salary(text) == ["$100,402.00"]

    print("Test 17")
    text = "$5,250 not salary but reimbursement at Harvard University $40 per class"
    print(extract_salary(text))
    assert extract_salary(text) == None

    print("Test 18")
    text = "Tuition Assistance Program (TAP): $40 per class at the Harvard Extension Scho"
    print(extract_salary(text))
    assert extract_salary(text) == None

    print("Test 19")
    text = "Senior Research Software Engineer | Harvard University\n O p p o r t u n i t y a w a i t s . . .\n http://sjobs.brassring.com/TGnewUI/Search/home/HomeWithPreLoad?partnerid=25240&siteid=5341&PageType=JobDetails&jobid=1959428&codes=IND\n Skip to main content\n Search for Jobs \n Harvard Human Resources Frequently Asked Questions Equal Employment Opportunity Diversity & Inclusion \n Sign In\n Dark mode Light Mode\n Share\n 11-Oct-2022\n Senior Research Software Engineer\n Harvard University Information Technology \n 58822BR\n Position Description \n This is a fully benefited, full-time Harvard University position that has been funded for one year. There is the possibility of renewal, contingent on funding, university priorities and satisfactory job performance. Harvard University Information Technology (HUIT) is a community of Information Technology professionals committed to delivering service and technological solutions in support of teaching, learning, research and administration. We are recruiting an IT workforce that has both breadth in their ability to collaborate and innovate across disciplines – and depth in specific areas of expertise. HUIT offers opportunities for IT professionals to learn and work in a unique technology landscape and service-focused environment. If you are a technically proficient, nimble, user-focused, and accountable IT professional who also connects with the importance of collaborating well in a team environment, we are looking for you! Founded in 1839, the Harvard College Observatory (HCO) carries on a broad program of research in astronomy and astrophysics, collaborating with the Smithsonian Astrophysical Observatory (SAO) at the Harvard-Smithsonian Center for Astrophysics (CfA) and providing substantial support to Harvard's Department of Astronomy. This position closely collaborates with project leaders in the CfA’s John G. Wolbach Library. The Wolbach Library houses both HCO and SAO collections, forming one of the world’s preeminent astronomical collections. Wolbach’s special collection holdings include primary sources associated with the institution’s history, as well as archival publications, papers, and objects created by observatories worldwide. The Wolbach Library is also the home of Harvard's Astronomical Photographic Glass Plate Collection. The Senior Research Software Engineer (RSE) supports researchers' data and software engineering needs at the Harvard College Observatory, which includes refactoring the data processing pipelines, front-end, and the codebase of the DASCH (Digital Access to a Sky Century at Harvard) project. Researchers at CfA utilize the DASCH platform to digitize the Harvard Astronomical Plate Collection, which provides the capability for a systematic study of the sky on 100-year time scales. This position works within the Research Software Engineering team and reports to the Associate Director of Research Software Engineering. A successful candidate will be able to develop and implement systems and data services that can efficiently process data at scale. Harvard University is looking for candidates with diverse backgrounds and new perspectives to work in University Research Computing and Data for the DASCH project. *For those interested in remote work, this role can be primarily remote. We also have beautiful on-campus space in the heart of Harvard Square for employees who choose to be on-site.*\n Basic Qualifications \n Minimum of seven years’ post-secondary education or relevant work experience\n Additional Qualifications and Skills \n The following Additional Qualifications are strongly preferred. If you meet some, but not all, you are still encouraged to apply; we value employees with a willingness to learn. Knowledge of data structures, data modeling, data aggregation, and data storage. Professional experience building and optimizing data processing pipelines and architectures. Proficient in database language and tools (PostgreSQL, MySQL, MongoDB). Advanced programming skills (Python is preferred). Professional experience with front-end development is a PLUS. Experience with Linux and distributed computing (MPI is preferred) is a PLUS. Basic familiarity with astronomy and its associated data structures is a PLUS. Comfortable working with version control systems such as git. Strong project management and organizational skills. Demonstrated success in working in a cross-functional team in an agile environment.\n Certificates and Licenses \n Completion of Harvard IT Academy specified foundational courses (or external equivalent) preferred\n Working Conditions \n Interview and onboarding activity for this position may be conducted via telephone & Zoom video conferencing, based on the department’s current presence on campus. This position will be a hybrid role with the option to work on campus or remotely as often as desired, with the expectation of attending in-person meeting and collaborative sessions when the opportunity presents itself. HUIT actively supports hybrid work where business and team needs allow. Additional detail will be discussed during the interview process. All remote work must be performed in a state in which Harvard is registered to do business (CA, CT, MA, MD, ME, NH, NY, RI, and VT). The University requires all Harvard community members to be fully vaccinated against COVID-19 and remain up to date with COVID-19 vaccine boosters, as detailed in Harvard’s Vaccine & Booster Requirements . Individuals may claim exemption from the vaccine requirement for medical or religious reasons. More information regarding the University’s COVID vaccination requirement, exemptions, and verification of vaccination status may be found at the University’s “COVID-19 Vaccine Information” webpage: http://www.harvard.edu/coronavirus/covid-19-vaccine-information/ . Harvard continues to place the highest priority on the health, safety and wellbeing of its faculty, staff and students, as well as the wider community. Information and details can be found via Harvard’s Coronavirus Workplace Policies website: https://hr.harvard.edu/corona-virus-workplace-policies .\n Additional Information \n Please provide a cover letter with your application. Please note: Harvard University requires pre-employment reference and background screening. We are unable to provide work authorization and/or visa sponsorship. This position has a 180-day orientation and review period. More about HUIT: Harvard University Information Technology (HUIT) is responsible for the strategy, planning, and delivery of information technology across the University. Our mission is to assure Harvard’s leadership in IT. We strive to make it easier for faculty, students, and staff to teach, research, learn and work through the effective use of information technology. HUIT’s core values are User Focused, Collaborative, Innovative and Open. IT Academy (designed for IT Staff): HUIT’s IT Academy aims to enable each IT staff person to grow professionally and become a trusted partner to her or his team. The IT Academy is built on the belief that every IT staff member across the University (including technology employees at each school and campus) can grow in her or his area of expertise as well as building strong people and project management skills. Learn more here: https://itacademy.harvard.edu/ Total Rewards: Harvard’s Total Rewards Program is designed to attract, retain, and reward the performance of talented employees. As a Harvard staff member, you enjoy many perks that come with working for one of the top employers in Massachusetts, including: Paid Time Off: 3 - 4 weeks accrued vacation days, 12 accrued sick days, 12.5 paid holidays plus winter recess, and 3 personal days awarded each calendar year. Medical/Dental/Vision: We offer a variety of excellent medical plans, dental & vision plans. Retirement: University-funded retirement plan with full vesting after 3 years of service. Tuition Assistance Program (TAP): $40 per class at the Harvard Extension School and discounted options through participating Harvard grad schools. Harvard University Employees Credit Union: Our employees credit union provides a complete line of services for all your financial needs. https://huecu.org Transportation: 50% discounted MBTA pass as well as additional options to assist employees in their daily commute. Wellness options: A variety of programs and classes at little or no cost, including stress management, massages, nutrition, meditation and complimentary health services. Access to athletic facilities, libraries, campus events and many discounts throughout metro Boston. Learn more: https://hr.harvard.edu/totalrewards Accessibility: Harvard University IT plays an important role in supporting Harvard's commitment by seeking to create, procure and deploy technologies that are accessible to all, including and especially those who live with disability. Harvard welcomes individuals with disabilities to apply for positions and participate in its programs and activities. If you would like to request accommodations or have questions about the physical access provided, please contact our University Disability Resources Department.\n Job Function \n Information Technology \n Location \n USA - MA - Cambridge \n Job Code \n I1258P IT RC Software/Data Prof IV \n Sub-Unit \n ------------ \n Department \n University Research Computing\n Time Status \n Full-time \n Salary Grade \n 058\n Union \n 00 - Non Union, Exempt or Temporary \n Pre-Employment Screening \n Identity \n Commitment to Equity, Diversity, Inclusion, and Belonging \n Harvard University views equity, diversity, inclusion, and belonging as the pathway to achieving inclusive excellence and fostering a campus culture where everyone can thrive. We strive to create a community that draws upon the widest possible pool of talent to unify excellence and diversity while fully embracing individuals from varied backgrounds, cultures, races, identities, life experiences, perspectives, beliefs, and values.\n EEO Statement \n We are an equal opportunity employer and all qualified applicants will receive consideration for employment without regard to race, color, religion, sex, national origin, disability status, protected veteran status, gender identity, sexual orientation, pregnancy and pregnancy-related conditions, or any other characteristic protected by law.\n Senior Research Software Engineer | Harvard University\n \n Apply to job \n Save \n Send to friend\n Reasonable Accommodations\n Frequently Asked Questions\n Contact Us\n Digital Accessibility\n Diversity & Inclusion \n Privacy Statement\n Technical Support \n Harvard Schools\n Infinite Talent Privacy Statement"
    print(extract_salary(text))
    assert extract_salary(text) == None

    ##################################################################################
    print("Tests for extract_salary_info function:")

    text = 'The salary for this position is $30,000 - $40,000 per year.'
    print("Test 1")
    print(get_salary_flag(text))
    assert get_salary_flag(text) == 'money_sign_digits'

    text = 'The salary for this position is $30k - $40k per year.'
    print("Test 3")
    print(get_salary_flag(text))
    assert get_salary_flag(text) == 'money_sign_digits'

    text = 'The salary for this position is $30,000 per year.'
    print("Test 4")
    print(get_salary_flag(text))
    assert get_salary_flag(text) == 'money_sign_digits'

    text = 'The salary for this position is $10 per hour.'
    print("Test 6")
    print(get_salary_flag(text))
    assert get_salary_flag(text) == 'money_sign_digits'

    text = 'The salary for this position is $10 - $20 per hour.'
    print("Test 7")
    print(get_salary_flag(text))
    assert get_salary_flag(text) == 'money_sign_digits'

    text = 'The salary for this position is ten per hour.'
    print("Input text:", text)
    print(get_salary_flag(text))
    assert get_salary_flag(text) == None

    text = 30000
    print("Test 9")
    print(get_salary_flag(text))
    assert get_salary_flag(text) == 'input_is_not_string'

    ##################################################################################
    print("All tests passed.")