from pydantic import BaseModel, EmailStr
from typing import Optional

class SettingsUpdate(BaseModel):
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    hours_weekdays: Optional[str] = None
    hours_saturday: Optional[str] = None
    hours_sunday: Optional[str] = None
    shipping_cost: Optional[float] = None
    free_shipping_threshold: Optional[float] = None
    google_maps_url: Optional[str] = None
    booking_email: Optional[EmailStr] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    privacy_text: Optional[str] = None
    terms_text: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    seo_image_url: Optional[str] = None

class SiteSettings(SettingsUpdate):
    id: Optional[str] = None
