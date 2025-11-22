# FastAPI-Movie-Recommendation-API

This project provides a simple movie recommendation API built with **FastAPI**.  
It takes a user preference as input and generates movie suggestions using the **Gemini 2.5 Flash** model.  
Movie data is loaded from a CSV dataset.

---

## Features
- Accepts user movie preference text  
- Uses Gemini API to generate recommendations  
- Returns 5–8 movie suggestions  
- Reads movie data from a CSV file  

---

## Tech Stack
- **FastAPI**
- **Python**
- **Gemini 2.5 Flash API**
- **Pandas**

---

## Endpoints

### POST /recommend
Send a movie preference and receive AI-generated recommendations.

### GET /
Basic health endpoint.

---

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
