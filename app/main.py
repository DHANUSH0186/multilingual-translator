from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import shutil

app = FastAPI(title="Multilingual Translator API")

@app.get("/")
async def home():
    return {
        "message": "Welcome to Multilingual Translator!",
        "features": [
            "Speech to Text",
            "Text Translation", 
            "Text to Speech",
            "Sign Language Detection"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/translate")
async def translate_text(
    text: str = Form(...),
    target_lang: str = Form("es")
):
    """Translate text to another language"""
    from googletrans import Translator
    translator = Translator()
    
    try:
        result = translator.translate(text, dest=target_lang)
        return {
            "original": text,
            "translated": result.text,
            "source_lang": result.src,
            "target_lang": target_lang
        }
    except Exception as e:
        return {"error": str(e)}