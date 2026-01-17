
from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from app.core.email_utils import send_email_background
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, User, UserInDB, UserUpdate
from pydantic import EmailStr
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_active_user
from app.db.mongodb import mongodb
from bson import ObjectId
from typing import Any

router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

from app.models.user import UserUpdate
@router.put("/me", response_model=User)
async def update_user_me(user_in: UserUpdate, current_user: User = Depends(get_current_active_user)):
    update_data = user_in.dict(exclude_unset=True)
    
    if update_data:
        # current_user is a dict from mongodb, not a pydantic model yet
        await mongodb.db.users.update_one(
            {"_id": current_user["_id"]},
            {"$set": update_data}
        )
        # Fetch updated user
        current_user = await mongodb.db.users.find_one({"_id": current_user["_id"]})
        
    return current_user

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, background_tasks: BackgroundTasks) -> Any:
    # Check if user exists
    existing_user = await mongodb.db.users.find_one({"email": user_in.email})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    # Create new user
    user_data = user_in.dict()
    hashed_password = get_password_hash(user_in.password)
    del user_data["password"]
    user_data["hashed_password"] = hashed_password
    
    result = await mongodb.db.users.insert_one(user_data)
    created_user = await mongodb.db.users.find_one({"_id": result.inserted_id})

    # Send Welcome Email
    email_html = f"""
    <h1>Benvenuto {user_in.full_name}!</h1>
    <p>Grazie per esserti registrato su Il Colle Tinto.</p>
    <p>Ora puoi accedere alla tua area riservata e gestire i tuoi ordini.</p>
    <br>
    <p>A presto,<br>Il Team di Il Colle Tinto</p>
    """
    background_tasks.add_task(
        send_email_background,
        user_in.email,
        "Benvenuto nel mondo de Il Colle Tinto",
        email_html
    )

    return created_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await mongodb.db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    

    access_token = create_access_token(subject=str(user["_id"]))
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "full_name": user.get("full_name"),
            "email": user.get("email"),
            "role": user.get("role", "user")
        }
    }

from pydantic import BaseModel
import secrets
from datetime import datetime, timedelta

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks):
    user = await mongodb.db.users.find_one({"email": request.email})
    if not user:
        # Don't reveal if user exists
        return {"msg": "If the email exists, a reset link has been sent."}
    
    # Generate token
    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=1)
    
    await mongodb.db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"reset_token": token, "reset_token_expires": expires}}
    )
    
    # Send Email
    reset_link = f"http://localhost:3000/reset-password?token={token}"
    email_html = f"""
    <h1>Recupero Password</h1>
    <p>Hai richiesto di reimpostare la tua password.</p>
    <p>Clicca sul link sottostante per procedere (scade in 1 ora):</p>
    <a href="{reset_link}" style="background-color: #7f1d1d; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; display: inline-block; margin: 20px 0;">Reimposta Password</a>
    <p>Se non sei stato tu, ignora questa email.</p>
    """
    
    background_tasks.add_task(
        send_email_background,
        request.email,
        "Recupero Password - Il Colle Tinto",
        email_html
    )
    
    return {"msg": "If the email exists, a reset link has been sent."}

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    user = await mongodb.db.users.find_one({"reset_token": request.token})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    if user.get("reset_token_expires") < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")
    
    hashed_password = get_password_hash(request.new_password)
    
    await mongodb.db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "hashed_password": hashed_password,
            "reset_token": None,
            "reset_token_expires": None
        }}
    )
    
    return {"msg": "Password updated successfully"}
