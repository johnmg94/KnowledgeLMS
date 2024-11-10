import re
import csv
import string

def write_csv_file():
    # Read the content from the file
    file_path = "final_questions/generated_questions.txt"

    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
    # print(data)
    # Use re.finditer to find all matches of the pattern in the data
    matches = re.finditer(r"(?<=Question:)(.*?)(?=refusal)", data, re.DOTALL)
    count = 0
    for match in matches:
        count += 1
        print(match)
    print(count)

    # Prepare a translation table to remove special characters
    # translator = str.maketrans('', '', string.punctuation)

    # Open the CSV file once, outside the loops
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Optionally, write a header row
        writer.writerow(['Question', 'Option A', 'Option B', 'Option C', 'Option D'])

        for match in matches:
            print(match)
            content = match.group(1)

            # Split the content by 'Question:' to get individual questions
            questions = [q.strip() for q in content.split('Question:') if q.strip()]

            for q in questions:
                print(q)
                # Replace '\n\n' with commas
                q = q.replace('\n\n', ', ') 
                print(q)
                
                # Remove special characters from the entire question block
                cleaned_q = q.strip()
                print(cleaned_q)
                # Split the cleaned question block by commas to get individual fields
                fields = [field.strip() for field in cleaned_q.split(',')]

                # Write the fields to the CSV file
                writer.writerow(fields)

    print("Data has been written to 'output.csv' successfully.")

# Call the function
write_csv_file()
