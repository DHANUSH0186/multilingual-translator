import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed
        self.engine.setProperty('volume', 0.9)  # Volume (0-1)
    
    def speak(self, text, language='en'):
        """Speak the text aloud"""
        print(f"🔊 Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def save_audio(self, text, filename='output.mp3'):
        """Save text as audio file"""
        print(f"💾 Saving audio to {filename}")
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()
        print(f"✅ Audio saved!")
    
    def set_voice_properties(self, rate=150, volume=0.9):
        """Customize voice speed and volume"""
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

if __name__ == "__main__":
    tts = TextToSpeech()
    
    print("Text-to-Speech Demo")
    print("=" * 50)
    
    # Test English
    tts.speak("Hello! I am your multilingual translator.")
    
    # Test with user input
    text = input("\nEnter text to speak: ")
    if text:
        tts.speak(text)
        
        # Ask if they want to save
        save = input("Save as audio file? (y/n): ")
        if save.lower() == 'y':
            tts.save_audio(text, "my_audio.mp3")