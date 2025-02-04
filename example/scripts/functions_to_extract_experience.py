# Script with functions to extract experience from job postings
# Emilio Lehoucq

######################################### IMPORTING LIBRARIES #########################################
import re

######################################### FUNCTION DEFINITIONS #########################################

def extract_years_experience(text, char_after=50):
    """
    Function to extract years of experience from job postings.

    Input: 
        text (str) - Text of a job posting.
    Output: 
        years_experience (list of str) - List of years of experience.
    """
    # Dictionary to map word numbers to digits
    word_to_num = {
        "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", 
        "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
        "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14",
        "fifteen": "15", "sixteen": "16", "seventeen": "17", "eighteen": "18",
        "nineteen": "19", "twenty": "20"
    }
    # Regex to match numbers 1-20 and ranges
    pattern = r"\b(?:20|1[0-9]|[1-9])\s?(?:to|-|–)\s?(?:20|1[0-9]|[1-9])\b|" \
              r"\b(?:20|1[0-9]|[1-9])\b|" \
              r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|" \
              r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|" \
              r"seventeen|eighteen|nineteen|twenty)\b"

    # Find all matches
    matches = re.finditer(pattern, text, re.IGNORECASE)

    # List to store years of experience
    years_experience = []

    # Iterate over matches
    for match in matches:

        # Get the end of the match
        end = match.end()

        # Get the text after the match
        text_after_match = text[end:end + char_after]

        # Check if the text after the match contains "year" and "experience"
        if "year" in text_after_match and "experience" in text_after_match:

            # Get the year(s) without leading/trailing spaces and convert to lowercase
            year = match.group().strip().lower()
            
            # Convert word-based numbers to digits
            if year in word_to_num:
                year = word_to_num[year]
            
            # Append to list
            years_experience.append(year)

    return sorted(set(years_experience))

if __name__ == "__main__":
    print("Module to extract experience from job postings running as main script.")
    print("Running tests...")
    
    ##################################################################################
    print("Tests for extract_years_experience function:")

    print("Test 1")
    text = "The candidate must have 3 years of experience."
    print(extract_years_experience(text))
    assert extract_years_experience(text) == ["3"]

    print("Test 2")
    text = "The candidate must have 1 year of experience. Preferably 2 years of experience."
    print(extract_years_experience(text))
    assert extract_years_experience(text) == ["1", "2"]

    print("Test 3")
    text = "Research Scientist II : A Master's degree and three (3) years of relevant full-time experience after completion of that degree or A Master's degree and five (5) years of relevant full-time experience after completion of a Bachelor's degree or A Doctoral degree Senior Research Scientist: A Master's degree and seven (7) years of relevant full-time experience after completion of that degree, or A Master's degree and nine (9) years of relevant full-time experience after completion of a Bachelor's degree, or A Doctoral degree and four (4) years of relevant full-time experience after completion of a Bachelor's degree. "
    print(extract_years_experience(text))
    assert extract_years_experience(text) == ['3', '4', '5', '7', '9']

    print("Test 4")
    text = "The candidate must have 1-2 year of experience."
    print(extract_years_experience(text))
    assert extract_years_experience(text) == ["1-2"]

    print("Test 5")
    text = "The candidate must have 20 years of experience."
    print(extract_years_experience(text))
    assert extract_years_experience(text) == ["20"]

    print("Test 6")
    text = "The candidate must have 200 years of experience."
    print(extract_years_experience(text))
    assert extract_years_experience(text) == []

    print("Test 7")
    text = "Careers\n \n Press Control+M to start dragging object\n Back \n Actions \n Previous Job Developer Intermediate \n Next Job Apply for Job Job ID 46234 \n Location Argonne, Illinois \n Add to Favorite Jobs Email this Job \n Department: NSRC - LS-CAT Salary/Grade: ITS/79 Job Summary: This position is available at Argonne National Laboratory, Sector 21 (LS-CAT) of the Advanced Photon Source. We need a programmer interested in working in a collaborative, scientific environment to support current operations, while implementing new hardware and functionality. LS-CAT is a highly productive macromolecular crystallography beamline that has been hosting scientific users for over 15 years. We are in an exciting time with the Advanced Photon Source undergoing an $800 million dollar upgrade in April 2023. This provides a rare opportunity to revisit our current control systems to optimize and expanded them to take advantage of the vastly improved X-ray beam. Excellent if you have experience in PostgreSQL and Python, but any strong background in coding would be extremely valuable. Much of the work entails taking the lead in developing and managing complex projects, but the APS is a vibrant scientific community open to collaboration. Develops, codes, tests, and debugs new software or enhancements to existing software. Typically works with senior staff, but may coordinate smaller or less complex projects independently. Designs and implements basic technical solutions ensuring that business needs and requirements are met. Performs basic system integration tasks. Provides estimation for assigned tasks. Specific Responsibilities : Strategic Planning Provides application development leadership for new and existing software applications. Partners with user in designing features for technology. Provides recommendation on how to enhance system for future growth. Advises/recommends project and activities as related to system/architectural direction and strategy. Administration Develops and implements procedures for data security, management and compliance Creates and maintains code documentation. Creates ad hoc administrative reports. Delivers system presentations and overviews. Evaluates feature/upgrade/change requests and recommends action. Researches new technologies to enhance current system. Development Provides technical leadership on projects. Acts as subject matter expert (SME) in appropriate technologies and business domain. Designs, codes, tests, debugs and documents all phases of applications development. Codes software applications adhering to designs supporting internal business requirements or external user. Troubleshoots complex, difficult issues. Designs databases and data structures. Provides recommendations on how to enhance system to meet full business requirements. Determines project feasibility and how to integrate with current system. Minimum Qualifications: Successful completion of a full 4-year course of study in an accredited college or university leading to a bachelor's or higher degree in a major such as computer science, information technology, or related; OR appropriate combination of education and experience. 2 years relevant experience required. Infrastructure (extends across applications) Code Repositories (Git, Subversion) GlobusOnline LDAP Linux Operating System SQL/MySQL/Postgres Programming Languages and Frameworks PL/SQL Python Shell Scripting Analytical database design/ data structure Debugging Troubleshooting Project Code documentation collaboration and teamwork Minimum Competencies: (Skills, knowledge, and abilities.) Proven programming capability in Python, C, or a related language Database management and experience with SQL/MySQL/Postgres/Redis Knowledge of UNIX/LINUX systems administration Hardware and software engineering Preferred Qualifications: Experience with motion control systems Synchrotron X-ray instrumentation Protein crystallography, X-ray scattering, and X-ray spectroscopy Configuration management systems User interface design Preferred Competencies: (Skills, knowledge, and abilities) EPICS (Experimental Physics and Industrial Control System). Motion control systems (e.g. PMAC, Galil, Newport). Robotics automation and integration (e.g. EPSON, Kuka). Data acquisition systems (e.g. VME, NI). PLC Systems (Schneider, Siemens, Pilz). Networking and IT infrastructure. Benefits: At Northwestern, we are proud to provide meaningful, competitive, high-quality health care plans, retirement benefits, tuition discounts and more! Visit us at https://www.northwestern.edu/hr/benefits/index.html to learn more. Work-Life and Wellness: Northwestern offers comprehensive programs and services to help you and your family navigate life’s challenges and opportunities, and adopt and maintain healthy lifestyles. We support flexible work arrangements where possible and programs to help you locate and pay for quality, affordable childcare and senior/adult care. Visit us at https://www.northwestern.edu/hr/benefits/work-life/index.html to learn more. Professional Growth & Development: Northwestern supports employee career development in all circumstances whether your workspace is on campus or at home. If you’re interested in developing your professional potential or continuing your formal education, we offer a variety of tools and resources. Visit us at https://www.northwestern.edu/hr/learning/index.html to learn more . Northwestern requires all staff and faculty to be vaccinated against COVID-19, subject to limited exceptions. For more information, please visit our COVID-19 and Campus Updates website. The Northwestern campus sits on the traditional homelands of the people of the Council of Three Fires, the Ojibwe, Potawatomi, and Odawa as well as the Menominee, Miami and Ho-Chunk nations. We acknowledge and honor the original people of the land upon which Northwestern University stands, and the Native people who remain on this land today. Northwestern University is an Equal Opportunity, Affirmative Action Employer of all protected classes, including veterans and individuals with disabilities. Women, racial and ethnic minorities, individuals with disabilities, and veterans are encouraged to apply. Click for information on EEO is the Law."
    print(extract_years_experience(text))
    assert extract_years_experience(text) == ["2"]

    print("Test 8")
    text = "Apply - Interfolio\n \n undefined page loaded\n Skip to Main Content\n \n Already have an account?\n \n Sign In\n \n Assistant Professor, Tenure Track, in Informatics\n University of Washington: Academic Personnel: Information School\n \n Location\n \n Seattle, WA\n \n Open Date\n \n Jul 18, 2024\n \n Description\n \n The University of Washington Information School (iSchool) is accepting applications for two tenure-track faculty positions at the Assistant Professor level starting September 1, 2025. \n \n The Information School is committed to the values of equity, diversity, inclusion, tribal sovereignty, and accessibility. We welcome individuals who are excited by, able to thrive in, and eager to contribute to our interdisciplinary environment. \n This position will be expected to engage in excellence in research and teaching that supports the growth of our Informatics program. At the Information School, Informatics includes the study, design, and development of information technology for the good of people, organizations, and society. Relevant disciplinary training can include, but is not limited to, computer and information science, the social sciences, or engineering. Research areas of interest for this position include, but are not limited to artificial intelligence, data science, and human-computer interaction. \n \n The position is a full-time 9-month tenure track appointment at the rank of Assistant Professor, with an anticipated start date of September 1, 2025. All University of Washington faculty engage in teaching, research, and service. This position will be expected to: \n \n Conduct high-quality research \n Acquire extramural funding for research\n Engage with the University of Washington Information School’s strategic commitments to one or more of the following areas: 1. Promote equity in health & wellbeing; 2. Encourage environmental sustainability and resilience; 3. Foster a more informed, just, and equitable democratic society. For more information please see https://ischool.uw.edu/about/information-impact \n Teach undergraduate and graduate courses in their area of specialization, as well as advance the school’s undergraduate Informatics curriculum. \n Perform service that furthers the mission of the Information School and the University of Washington more broadly.\n About the iSchool \n The UW Information School is dedicated to hiring faculty who will enhance our inclusion, diversity, equity, access, and sovereignty (IDEAS) mission and vision through their research, teaching, and service. As information systems and institutions serve increasingly diverse and global constituencies, it is vital to understand the ways in which differences in gender, class, race, ethnicity, religious affiliation, national and cultural boundaries, national origin, worldview, intellectual origin, ability, and other identities can both divide us and offer us better ways of thinking and working. The Information School faculty are committed to preparing professionals who work in an increasingly diverse global society by promoting equity and justice for all individuals, actively working to eliminate barriers and obstacles created by institutional discrimination. \n \n The successful candidate will join a broad-based, inclusive information school, whose faculty members pursue their scholarship, teaching, and service across multiple degree programs. The University of Washington is an institution that encourages inclusive research and community outreach, situated between the Puget Sound and Lake Washington, in the city of Seattle, on the traditional territories of the Coast Salish people. Seattle is a rapidly growing, dynamic, and diverse metropolitan area with a leading technology sector and vibrant civic sector. Applicants may find further information about the Information School at: ischool.uw.edu. \n \n The base salary for this position will be $12,000 - $14,500 per month ($108,000 - $130,500 per 9-month academic year), commensurate with experience and qualifications, or as mandated by a U.S. Department of Labor prevailing wage determination.\n Qualifications\n \n \n Applicants must have a PhD (or foreign equivalent) in Information Science or a relevant field by date of appointment.\n Application Instructions\n \n Review of applications will begin immediately and continue until the position is filled. Preference will be given to applications submitted by October 20, 2024. Selected candidates will be invited for phone interviews and campus visits. \n \n Application packages should include the following elements (please note the strict page limit for each component): \n CV\n Letter of intent [1 page]\n Introduce your research agenda, your areas of expertise for teaching at the iSchool, and how your work fits into one of the school’s strategic areas (see above). \n Research statement [3 pages maximum]\n Describe your current research agenda, major contributions to date, and future research plans including potential topics and avenues of research funding. \n At the top of the first page provide 3-5 keywords that represent your research expertise (e.g. Human Computer Interaction, Ethics, Artificial Intelligence, Information Retrieval, etc)\n Teaching statement [2 pages maximum]\n Describe your approach to and experience teaching at the undergraduate or graduate level. Where appropriate, please include any experience designing courses, instructional materials, or curriculum development. \n Diversity statement [2 page maximum] \n See extended directions below\n Two sample publications or scholarly works that exemplify your current research agenda \n Names and contact information for three references. Shortlisted candidates will be contacted for letters of reference. \n Please contact Dr. Nicholas Weber or Dr. Emma Spiro - co-chairs of the Tenure Track Search Committee, with questions ( iApply@uw.edu ). \n \n iSchool Diversity Statement Guidelines \n \n Inclusion, diversity, equity, accessibility, and sovereignty (IDEAS) are core values of the University of Washington’s Information School, as described on our website: https://ischool.uw.edu/diversity . The Diversity Statement provides an opportunity for applicants to reflect on their research, teaching, and service accomplishments and goals that contribute to those values. The Diversity Statement should describe your commitment to these values, as reflected in teaching, research, and service experiences.\n Application Process\n \n This institution is using Interfolio's Faculty Search to conduct\n this search. Applicants to this position receive a free Dossier\n account and can send all application materials, including\n confidential letters of recommendation, free of charge.\n \n Apply Now\n \n Equal Employment Opportunity Statement\n \n University of Washington is an affirmative action and equal opportunity employer. All qualified applicants will receive consideration for employment without regard to race, color, creed, religion, national origin, sex, sexual orientation, marital status, pregnancy, genetic information, gender identity or expression, age, disability, or protected veteran status. \n Benefits Information \n A summary of benefits associated with this title/rank can be found at https://hr.uw.edu/benefits/benefits-orientation/benefit-summary-pdfs/ . Appointees solely employed and paid directly by a non-UW entity are not UW employees and are not eligible for UW or Washington State employee benefits. \n Commitment to Diversity \n The University of Washington is committed to building diversity among its faculty, librarian, staff, and student communities, and articulates that commitment in the UW Diversity Blueprint ( http://www.washington.edu/diversity/diversity-blueprint /). Additionally, the University’s Faculty Code recognizes faculty efforts in research, teaching and/or service that address diversity and equal opportunity as important contributions to a faculty member’s academic profile and responsibilities ( https://www.washington.edu/admin/rules/policies/FCG/FCCH24.html#2432 ). \n Privacy Notice \n Review the University of Washington Privacy Notice for Demographic Data of Job Applicants and University Personnel to learn how your demographic data are protected, when the data may be used, and your rights. \n Disability Services \n To request disability accommodation in the application process, contact the Disability Services Office at 206-543-6450 or dso@uw.edu ."
    print(extract_years_experience(text))
    assert extract_years_experience(text) == []

    ##################################################################################
    print("All tests passed.")