from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from googletrans import Translator
import shutil
import speech_recognition as sr

app = FastAPI(title="Multilingual Translator API")
translator = Translator()

@app.get("/")
async def home():
    return {
        "message": "Welcome to Multilingual Translator!",
        "features": [
            "Speech to Text",
            "Text Translation", 
            "Text to Speech",
            "Sign Language Detection"
        ],
        "usage": "Visit /docs for API documentation"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/translate")
async def translate_text(text: str, target_lang: str = "es"):
    """
    Translate text to another language
    
    Parameters:
    - text: The text you want to translate
    - target_lang: Target language code (default: es for Spanish)
    
    Supported languages:
    en (English), es (Spanish), fr (French), de (German), 
    hi (Hindi), ja (Japanese), zh-cn (Chinese), ar (Arabic),
    ru (Russian), pt (Portuguese), it (Italian), ko (Korean)
    """
    try:
        result = translator.translate(text, dest=target_lang)
        return {
            "success": True,
            "original_text": text,
            "translated_text": result.text,
            "source_language": result.src,
            "target_language": target_lang
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Translation failed"
        }

@app.post("/speech-to-text")
async def speech_to_text_api(
    audio_file: UploadFile = File(...),
    source_lang: str = "en-US",
    target_lang: str = "es"
):
    """
    Convert uploaded audio file to text and translate
    
    Parameters:
    - audio_file: Audio file (WAV format recommended)
    - source_lang: Source language (e.g., en-US, es-ES, hi-IN)
    - target_lang: Target language code for translation
    """
    try:
        # Save uploaded file temporarily
        temp_audio = "temp_audio.wav"
        with open(temp_audio, "wb") as f:
            shutil.copyfileobj(audio_file.file, f)
        
        # Recognize speech
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_audio) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language=source_lang)
        
        # Translate
        translated = translator.translate(text, dest=target_lang)
        
        return {
            "success": True,
            "original_text": text,
            "translated_text": translated.text,
            "source_language": source_lang,
            "target_language": target_lang
        }
    except sr.UnknownValueError:
        return {"success": False, "error": "Could not understand audio"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/microphone-to-text")
async def microphone_input():
    """
    Record from microphone (only works when running locally)
    """
    try:
        from app.speech_to_text import SpeechToText
        stt = SpeechToText()
        text = stt.listen_from_microphone()
        
        return {
            "success": True,
            "recognized_text": text
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/text-to-speech")
async def text_to_speech_api(text: str, save_file: bool = False):
    """
    Convert text to speech
    
    Parameters:
    - text: Text to convert to speech
    - save_file: If true, saves audio file instead of speaking
    """
    try:
        from app.text_to_speech import TextToSpeech
        tts = TextToSpeech()
        
        if save_file:
            filename = "output_audio.mp3"
            tts.save_audio(text, filename)
            return {
                "success": True,
                "message": "Audio file created",
                "filename": filename,
                "text": text
            }
        else:
            tts.speak(text)
            return {
                "success": True,
                "message": "Text spoken successfully",
                "text": text
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/full-translation-pipeline")
async def full_pipeline(
    input_type: str = "text",
    text: str = "",
    target_lang: str = "es",
    output_speech: bool = False
):
    """
    Complete translation pipeline:
    1. Input: text or speech (microphone)
    2. Translate to target language
    3. Output: text or speech
    
    Parameters:
    - input_type: "text" or "speech" (microphone)
    - text: Text to translate (if input_type is "text")
    - target_lang: Target language code
    - output_speech: If true, speaks the translation
    """
    try:
        # Step 1: Get input text
        if input_type == "speech":
            from app.speech_to_text import SpeechToText
            stt = SpeechToText()
            text = stt.listen_from_microphone()
            if not text or "Error" in text or "Could not" in text:
                return {"success": False, "error": "Speech recognition failed"}
        
        # Step 2: Translate
        result = translator.translate(text, dest=target_lang)
        translated = result.text
        
        # Step 3: Output
        if output_speech:
            from app.text_to_speech import TextToSpeech
            tts = TextToSpeech()
            tts.speak(translated)
        
        return {
            "success": True,
            "original_text": text,
            "translated_text": translated,
            "source_language": result.src,
            "target_language": target_lang,
            "output_type": "speech" if output_speech else "text"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/languages")
async def get_languages():
    """Get list of all supported languages"""
    return {
        "supported_languages": {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "hi": "Hindi",
            "ja": "Japanese",
            "zh-cn": "Chinese",
            "ar": "Arabic",
            "ru": "Russian",
            "pt": "Portuguese",
            "it": "Italian",
            "ko": "Korean",
            "tr": "Turkish",
            "nl": "Dutch",
            "pl": "Polish",
            "sv": "Swedish"
        }
    }