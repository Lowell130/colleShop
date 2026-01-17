
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, User, UserInDB, UserUpdate
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
async def register(user_in: UserCreate) -> Any:
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
