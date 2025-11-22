from fastapi import FastAPI, HTTPException
#from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import requests
import json
from typing import List, Dict

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# ) # Frontende qoşacaqsızsa açın bunu

GEMINI_API_KEY = "API_KEY"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

df=None

class PreferenceRequest(BaseModel):
    preference: str

class MovieRecommendation(BaseModel):
    recommendations: List[Dict]

@app.on_event("startup")
async def startup_event():
    global df
    df=pd.read_csv("Latest 2025 movies Datasets.csv")
    df.columns=df.columns.str.strip()

@app.post("/recommend", response_model=MovieRecommendation)
async def recommend_movies(request : PreferenceRequest):
    try:
        arr=[]
        for _,j in df.head(300).iterrows():
            arr.append({
                "title": str(j.get('title', '')),
                "release_date": str(j.get('release_date', '')),
                "original_language": str(j.get('original_language', '')),
                "popularity": str(j.get('popularity', '')),
                "vote_count": str(j.get('vote_count', '')),
                "vote_average": str(j.get('vote_average', '')),
                "overview": str(j.get('overview', ''))[:200]
            })
        
        movies_json=json.dumps(arr,ensure_ascii=False)
        
        prompt = f"""
Kullanıcı tercihi: {request.preference}

Aşağıdaki film veritabanından kullanıcının tercihine en uygun 5-8 film öner.
original_language kodları: en=İngilizce, es=İspanyolca, hi=Hintçe, ko=Korece vb.

{movies_json}

SADECE bu JSON formatında cevap ver:
{{
    "recommendations": [
        {{
            "title": "Film adı",
            "release_date": "Tarih",
            "language": "Dil",
            "rating": "Puan",
            "popularity": "Popülerlik",
            "reason": "Neden önerildi"
        }}
    ]
}}
"""
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(GEMINI_URL,json=payload)
        response.raise_for_status()
        
        ans=response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        if(ans.startswith("```json")):
            ans=ans[7:]
        if(ans.endswith("```")):
            ans=ans[:-3]
        ans=ans.strip()
        result=json.loads(ans)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@app.get("/")
async def root():
    return {"salam":"sagol"}

