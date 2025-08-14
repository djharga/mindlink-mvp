# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import requests

OPENAI_KEY = os.getenv('OPENAI_API_KEY')

app = FastAPI(title='MindLink API')

class TextRequest(BaseModel):
    text: str
    lang: str = 'ar'

@app.post('/v1/generate')
async def generate(payload: TextRequest):
    prompt = f"حول النص التالي لإخراج مناسب للاستخدام في MindLink: {payload.text}"
    headers = {
        'Authorization': f'Bearer {OPENAI_KEY}',
        'Content-Type': 'application/json'
    }
    body = {
        'model':'gpt-4o-mini',
        'messages': [
            {'role':'system', 'content':'أنت مساعد توليد محتوى مبتكر.'},
            {'role':'user', 'content': prompt}
        ]
    }
    r = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=body)
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail='OpenAI API error')
    data = r.json()
    return {'result': data['choices'][0]['message']['content']}

@app.post('/v1/transcribe')
async def transcribe(file: UploadFile = File(...)):
    # Forward audio to Whisper (OpenAI) — بسيطة للعرض
    files = {'file': (file.filename, await file.read())}
    headers = {'Authorization': f'Bearer {OPENAI_KEY}'}
    r = requests.post('https://api.openai.com/v1/audio/transcriptions', headers=headers, files=files, data={'model':'whisper-1'})
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail='Transcription failed')
    return r.json()
