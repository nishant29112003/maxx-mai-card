from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import recommend, auth

app = FastAPI()

# ✅ CORS: Allow frontend (localhost:3000) to access backend (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routers
app.include_router(recommend.router)
app.include_router(auth.router)
