import subprocess

def text_to_speech(text):
    subprocess.run(
        ["festival", "--tts"],
        input=text,
        text=True,
    )

# Example usage
if __name__ == "__main__":
    text_to_speech("Hi, how can I help you?")
