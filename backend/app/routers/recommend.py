from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..utils.predictor import recommend_card
from ..utils.gmail_parser import parse_and_store  
from pymongo import MongoClient
from app.config.config import MONGO_URI  

router = APIRouter()

class SpendRequest(BaseModel):
    spends: dict

@router.post("/recommend")
def recommend(spend_request: SpendRequest):
    try:
        card = recommend_card(spend_request.spends)
        return {"best_card": card}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/parse_gmail")
def trigger_gmail_parsing():  # NEW
    try:
        parse_and_store()
        return {"message": "Parsing complete and stored in MongoDB"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/last_parsed")
def get_last_parsed():
    try:
        client = MongoClient(MONGO_URI)
        db = client["maxxcard"]
        doc = db.estatements.find_one(sort=[("timestamp", -1)])
        if not doc:
            return {"message": "No parsed statements found"}
        return {
            "email_id": doc["email_id"],
            "parsed_text": doc["parsed_text"],
            "timestamp": str(doc["timestamp"])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
