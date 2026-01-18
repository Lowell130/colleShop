from fastapi import APIRouter, Depends, HTTPException, status
from app.db.mongodb import mongodb
from app.models.settings import SiteSettings, SettingsUpdate
from app.core.security import get_current_user
from app.models.user import User
from typing import Any

router = APIRouter()

@router.get("/", response_model=SiteSettings)
async def get_settings() -> Any:
    # Try to find existing settings
    settings = await mongodb.db.settings.find_one({})
    
    if not settings:
        # Return defaults if not found (or create them?)
        # Let's return defaults
        return SiteSettings()
    
    return SiteSettings(**settings, id=str(settings["_id"]))

@router.put("/", response_model=SiteSettings)
async def update_settings(settings_in: SettingsUpdate, current_user: User = Depends(get_current_user)) -> Any:
    # Admin only
    if current_user.get("role") != "admin":
         raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if settings exist
    existing = await mongodb.db.settings.find_one({})
    
    if existing:
        await mongodb.db.settings.update_one({"_id": existing["_id"]}, {"$set": settings_in.dict(exclude_unset=True)})
        updated = await mongodb.db.settings.find_one({"_id": existing["_id"]})
        return SiteSettings(**updated, id=str(updated["_id"]))
    else:
        # Create new
        new_settings = settings_in.dict()
        result = await mongodb.db.settings.insert_one(new_settings)
        return SiteSettings(**new_settings, id=str(result.inserted_id))
