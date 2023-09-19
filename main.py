import openai
import pyttsx3
import speech_recognition as sr

# Set your OpenAI API key
openai.api_key = "INSERT-API-KEY-HERE"

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to transcribe audio from a file
def transcribe(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print('Could not understand audio')
        except sr.RequestError as e:
            print(f'Recognition request failed: {e}')

# Function to generate a response using OpenAI's GPT-3
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

# Function to speak text using text-to-speech engine
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    is_question_asked = False

    while not is_question_asked:
        print("Say 'Hey GPT' to begin")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source, timeout=5)  # Adjust the timeout as needed
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "hey gpt":
                    is_question_asked = True
                    print("Recording your question...")

                else:
                    print("Say 'Hey GPT' to start recording a question")
                    
            except sr.WaitTimeoutError:
                print("Listening timeout. Say 'Hey GPT' to start again.")
            except Exception as e:
                print(f"An error occurred: {e}")

    # Once 'is_question_asked' is True, proceed with recording and processing the question.
    filename = "input.wav"
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source, phrase_time_limit=None, timeout=10)  # Adjust the timeout as needed
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())

    text = transcribe(filename)
    if text:
        print(f"You said: {text}")

        response = generate_response(text)
        print(f"GPT says: {response}")
        speak_text(response)

if __name__ == "__main__":
    main()
