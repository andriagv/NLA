import speech_recognition as sr

audio_path = 'Are.wav'

# Initialize the recognizer
recognizer = sr.Recognizer()

# Load the audio file
with sr.AudioFile(audio_path) as source:
    # Adjust for ambient noise and recognize the speech
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.record(source)

    # Perform speech recognition
    try:
        transcription = recognizer.recognize_google(audio)
        print("Transcription: {}".format(transcription))

        # Save the transcribed text to a text file
        output_file_path = 'output.txt'
        with open(output_file_path, 'w') as output_file:
            output_file.write(transcription)

        print("Transcribed text saved to {}".format(output_file_path))

    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
