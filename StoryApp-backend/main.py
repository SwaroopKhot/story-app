from fastapi import FastAPI
from app.routes import auth, story


app = FastAPI()
app.include_router(story.router)
app.include_router(auth.auth_router)
