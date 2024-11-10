from openai import OpenAI
import os
from dotenv import load_dotenv
import re
import csv

def file_count():
    input_path = '../second_round/Text Files'
    count = 0
    numerator_average = 0
    for filename in os.listdir(input_path):
        input_file_path = os.path.join(input_path, filename)
        print(str(input_file_path))
        if not os.path.isfile(input_file_path):
            continue
        try:
            with open(input_file_path, 'r', encoding='utf-8') as file:
                length = sum(len(line) for line in file)
                numerator_average += length
                print("Numerator Average: ", str(numerator_average))
                count += 1
            print("Total count: ", str(count))
            print("Total Numerator Average: ", str(numerator_average))
            # Need to divide numerator average by count to get the average file length
            # Average = 5062
        except:
            print("Could not open file")

# Called this function first to get the average length of the files that will be input into openai's chat api
# x = file_count()
# print(x)


class GPT():
    def __init__(self):
        load_dotenv()
        api_key = os.environ.get('OPENAI_API_KEY')
        project_id = os.environ.get('$PROJECT_ID')

        self.client = OpenAI(
            # This is the default and can be omitted
            project = project_id,
            api_key = api_key
        )

    def chat_gpt_func(self, prompt, text_content):
        # Combine the prompt and text content into a single string
        full_content = f"{prompt}\n\n{text_content}"
        chat_completion = None
        # Correct the messages parameter
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": full_content,
                    },
                ],
                model="gpt-3.5-turbo",
            )
        except Exception as e:
            print(f"An error occurred: {e}")
        questions = chat_completion
        with open('generated_questions.txt', 'a', encoding='utf-8') as file:
            file.write(str(questions))

def gpt_call():
    prompt = f"""You are an expert test creator who generates multiple-choice questions.

                Based on the following content, create multiple-choice test questions.

            For each question, follow this format exactly:

            Question: [Your question here]

            A. [Correct answer]

            B. [Incorrect answer]

            C. [Incorrect answer]

            D. [Incorrect answer]

            Ensure that option A is always the correct answer. Provide 3 questions, ensuring they are high-quality and relevant to the content."""

    prompt_5 = f"""You are an expert test creator who generates multiple-choice questions.

                Based on the following content, create multiple-choice test questions.

            For each question, follow this format exactly:

            Question: [Your question here]

            A. [Correct answer]

            B. [Incorrect answer]

            C. [Incorrect answer]

            D. [Incorrect answer]

            Ensure that option A is always the correct answer. Provide 5 questions, ensuring they are high-quality and relevant to the content."""
    x = GPT()
    input_path = '../second_round/Text Files'
    for filename in os.listdir(input_path):
        input_file_path = os.path.join(input_path, filename)
        print(str(input_file_path))
        if not os.path.isfile(input_file_path):
            continue
        try:
            with open(input_file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
                length = sum(len(line) for line in file)
                # In my use case, average file length = 5062
                if length > 7500:
                    try:
                        x.chat_gpt_func(prompt_5, text_content)
                    except Exception as e:
                        print(e)
                        break
                else:
                    try:
                        x.chat_gpt_func(prompt, text_content)
                    except Exception as e:
                        print(e)
                        break
        except:
            print("Could not open file")
# Call gpt_call to generate test questions
# x = gpt_call()

def write_csv_file():
    # Will work if questions and answers are saved to single text file
    # Read the content from the file
    file_path = f"final_questions/generated_questions.txt"

    # Read the content from the file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()

    arr = []
    outer_arr = []
    # Using count to check the total number of questions with count/5
    count = 0
    question = r'Question: '
    end_string = r'\"\, refusal=None, role=\\\'assistant\'\,'
    a = r'A\. '
    b = r'B\. '
    c = r'C\. '
    d = r'D\. '
    match = re.finditer(r"(Question:(.*?)\\n\\n[^ABC].(.*?)\\n\\nQ(Q)|Question:(.*?)',)", data, re.DOTALL)      
    if match:
        count = 0
        for matched in match:
            content = matched.group(1)
            out = re.split(r"\\n\\n\\n|\\n\\n|\\n", content)

            for q in out:
                if re.search(question, q):
                    q = q.strip(question)
                if re.search(end_string, q):
                    q = q.strip(end_string)
                if re.search(a, q):
                    q = q.strip(a)
                if re.search(b, q):
                    q = q.strip(b)
                if re.search(c, q):
                    q = q.strip(c)
                if re.search(d, q):
                    q = q.strip(d)
                count += 1        
                arr.append(q)
                if count%5 == 0:
                    # print(arr)
                    arr = []
                    outer_arr.append(arr)

    # Estimated number of questions
    # print(str(count/5))

        # Write the questions and options to a CSV file
    with open('output.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Question', 'Option A', 'Option B', 'Option C', 'Option D'])
        for row in outer_arr:
            print(row)
            writer.writerow(row)
        print("Data has been written to 'output.csv' successfully.")

x = write_csv_file()