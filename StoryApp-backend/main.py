from fastapi import FastAPI
from app.routes import auth, story
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(story.router)
app.include_router(auth.auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)
