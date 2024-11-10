# Not working
def generate_questions_chat(text):
    messages = [
        {"role": "system", "content": "You are an expert test creator."},
        {"role": "user", "content": f"""
Based on the following content, create multiple-choice test questions.

Content:
{text}

For each question, follow this format exactly:

Question: [Your question here]

A. [Correct answer]

B. [Incorrect answer]

C. [Incorrect answer]

D. [Incorrect answer]

Ensure that option A is always the correct answer. Provide at least 5 questions, ensuring they are high-quality and relevant to the content.
"""}
    ]

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        max_tokens=1500,
        temperature=0.7,
    )

    questions = response['choices'][0]['message']['content'].strip()
    return questions

# Generate the questions using ChatCompletion
questions = generate_questions_chat(text_content)

# Splitting text

def split_text(text, max_length=2000):
    # Split text into chunks of max_length characters
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

chunks = split_text(text_content)

all_questions = ""

for chunk in chunks:
    questions = generate_questions(chunk)
    all_questions += questions + "\n\n"

print(all_questions)

