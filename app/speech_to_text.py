import speech_recognition as sr
from googletrans import Translator

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
    
    def listen_from_microphone(self, language='en-US'):
        """Listen to microphone and convert to text"""
        with sr.Microphone() as source:
            print("🎤 Listening... Speak now!")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                print("🔄 Processing...")
                text = self.recognizer.recognize_google(audio, language=language)
                print(f"✅ You said: {text}")
                return text
            except sr.WaitTimeoutError:
                return "No speech detected"
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError as e:
                return f"Error: {e}"
    
    def translate_speech(self, text, target_lang='es'):
        """Translate the recognized speech"""
        try:
            result = self.translator.translate(text, dest=target_lang)
            return result.text
        except Exception as e:
            return f"Translation error: {e}"

if __name__ == "__main__":
    stt = SpeechToText()
    print("Speech-to-Text Demo")
    print("Speak something in English...")
    
    text = stt.listen_from_microphone('en-US')
    print(f"\nOriginal: {text}")
    
    if text and "Error" not in text and "Could not" not in text:
        translated = stt.translate_speech(text, 'es')
        print(f"Spanish: {translated}")