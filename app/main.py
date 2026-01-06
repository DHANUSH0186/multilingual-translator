from fastapi import FastAPI
from googletrans import Translator

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
            "nl": "Dutch"
        }
    }