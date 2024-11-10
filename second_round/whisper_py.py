import whisper
import os

# Load the Whisper model
model = whisper.load_model('medium')
# You can choose 'tiny', 'small', 'medium', 'large'
# Transcribe the audio file

input_path = '../second_round/audio'
output_path = '../second_round/text'

count = 0
for filename in os.listdir(input_path):
    input_file_path = os.path.join(input_path, filename)
    print(str(input_file_path))
    if not os.path.isfile(input_file_path):
        continue
    try:
        result = model.transcribe(input_file_path)
    except Exception as e:
        print("Error transcribing", str(e))
    transcribed_text = result['text']
    output_file_path = os.path.join(output_path, f"{os.path.splitext(filename)[0]}.txt")
    with open(output_file_path, 'w') as output_file:
        output_file.write(transcribed_text)
        print("Successfully wrote file: ", str(output_file_path))
