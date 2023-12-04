import re
import os
import json

def extract_information(text):
    # Define regular expressions for different pieces of information
    roll_number_pattern = re.compile(r'Roll No[.:-]? (\d+)')
    unique_id_pattern = re.compile(r'UNIQUE ID[.:-]? (\d+)')
    name_pattern = re.compile(r'Name(?: of Candidate)?[.-: ]? (\w+ \w+)')
    school_pattern = re.compile(r'\nSchool[.:-]?[\']?[ ]*[a-zA-z ]*[:]?\d*([A-Za-z,:\' ]+)')
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

folder_path = "outputs"
file_list = os.listdir(folder_path)

for path in file_list:
    if "ICSE" in path.upper() or "CBSE" in path.upper():
        with open(folder_path + "/" + path, 'r') as file:
            text = file.read()
            info = extract_information(text)
            print(info)

            output_folder = "parsed"
            out_path = output_folder + "/" + path + ".json"
            with open(out_path, "w") as file:
                pass
            with open(out_path, "a") as file:
                json.dump(info, file, sort_keys = True, indent = 4, ensure_ascii = False)