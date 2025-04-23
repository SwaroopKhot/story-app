from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.models.user import UserCreate, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.db.mongodb import users_collection
from datetime import timedelta

auth_router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@auth_router.post("/register")
async def register(user: UserCreate):
    existing = await users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(user.password)
    await users_collection.insert_one({"username": user.username, "hashed_password": hashed_password})
    return {"msg": "User created successfully"}

@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["username"]}, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer", "user": user["username"]}

# Token Validation 
from jose import JWTError
from app.core.security import decode_access_token

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await users_collection.find_one({"username": username})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token error")
