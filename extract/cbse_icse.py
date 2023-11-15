import re

def extract_information(text):
    # Define regular expressions for different pieces of information
    roll_number_pattern = re.compile(r'Roll No\. (\d+)')
    unique_id_pattern = re.compile(r'UNIQUE ID (\d+)')
    name_pattern = re.compile(r'Name(?: of Candidate)? (\w+ \w+)')
    school_pattern = re.compile(r'School \d+ ([A-Za-z,\' ]+)')
    school_pattern2 = re.compile(r'of ([A-Za-z,\' ]+)')
    marks_pattern = re.compile(r'(\d{3}) ([A-Z &]+)\n(\d{3}) (\d{2,3})')
    issue_date = re.compile(r'date[a-zA-Z: ]* ((0[1-9]|[12][0-9]|3[01])[-.](0[1-9]|1[0,1,2])[-.](19|20)\d{2})', re.IGNORECASE)

    # Extract information using regular expressions
    roll_number_match = roll_number_pattern.search(text)
    unique_id_match = unique_id_pattern.search(text)
    name_match = name_pattern.search(text)
    school_match = school_pattern.search(text)
    school_match2 = school_pattern2.search(text)
    marks_matches = marks_pattern.findall(text)
    issue_date_match = issue_date.search(text) 

    # Create a dictionary to store extracted information
    extracted_info = {
        'Roll Number / Unique ID': roll_number_match.group(1) if roll_number_match else unique_id_match.group(1) if unique_id_match else None,
        'Name': name_match.group(1) if name_match else None,
        'School': school_match.group(1).strip() if school_match else school_match2.group(1).strip() if school_match2 else None,
        'Marks': {subject: (theory, practical) for theory, subject, practical in marks_matches} if marks_matches else None,
        'Issue date': issue_date_match.group(1) if issue_date_match else None
    }

    return extracted_info

# Read the contents of the first text file
with open('outputs/CBSE.jpg.txt', 'r') as file1:
    text1 = file1.read()

# Extract information from the first text file
result1 = extract_information(text1)

# Read the contents of the second text file
with open('outputs/ICSE.jpg.txt', 'r') as file2:
    text2 = file2.read()

# Extract information from the second text file
result2 = extract_information(text2)

# Print the extracted information
print("Information from CBSE:")
print(result1)
print("\nInformation from ICSE:")
print(result2)
