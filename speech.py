from gtts import gTTS
import os

def text_to_speech(text):
    # Create a gTTS object
    tts = gTTS(text=text, lang='en')

    # Save the speech to a file
    tts.save("output.mp3")

    # Play the audio file using the default media player
    os.system("xdg-open output.mp3")

# Example usage
if __name__ == "__main__":
    text_to_speech("Hi, how can I help you?")

