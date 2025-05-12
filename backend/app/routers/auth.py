from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.jwt_utils import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(req: LoginRequest):
    
    if req.username == "testuser" and req.password == "testpass":
        token = create_access_token({"sub": req.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")