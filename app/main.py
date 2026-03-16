# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
import pypdf
import io
import time

from app.engine.ai_analyzer import analyze_rfp_text
# Importing our compiled Rust module!
import rust_core

app = FastAPI(
    title="AI RFP Insight Engine",
    description="High-performance backend for analyzing Request for Proposals (RFPs) using Rust and Gemini 1.5 Pro.",
    version="1.0.0"
)

@app.post("/analyze-rfp", summary="Analyze a PDF RFP document")
async def analyze_rfp(file: UploadFile = File(...)):
    """
    Accepts a PDF file, extracts text, optimizes it via Rust, and analyzes it using AI.
    """
    # 1. Validation
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    start_time = time.time()
    
    try:
        # 2. Read PDF into memory and extract raw text
        pdf_bytes = await file.read()
        pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        
        raw_text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                raw_text += extracted + " "
                
        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract any text from the provided PDF.")
            
        # 3. Rust Performance Bridge: Pre-processing & Scoring
        # We clean the text to save LLM tokens and reduce hallucination risks
        cleaned_text = rust_core.clean_text(raw_text)
        
        # We run a quick keyword match score using Rust to demonstrate pre-filtering
        keywords = ["budget", "deadline", "compliance", "mandatory", "security", "penalty", "sla"]
        match_score = rust_core.calculate_match_score(cleaned_text, keywords)
        
        # 4. AI Analysis via Gemini 1.5 Pro
        ai_result = await analyze_rfp_text(cleaned_text)
        
        processing_time = round(time.time() - start_time, 2)
        
        # 5. Return a structured response combining AI insights and system performance metrics
        return {
            "status": "success",
            "metrics": {
                "processing_time_seconds": processing_time,
                "rust_pre_filter_score": match_score,
                "original_char_count": len(raw_text),
                "cleaned_char_count": len(cleaned_text),
                "tokens_saved_approx": (len(raw_text) - len(cleaned_text)) // 4 
            },
            "analysis": ai_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")