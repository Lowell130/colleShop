from pydantic import BaseModel, EmailStr
from typing import Optional

class SettingsUpdate(BaseModel):
    address: str = "Contrada Colle Tinto, 12, 86010 Castropignano (CB)"
    email: EmailStr = "info@ilcolletinto.it"
    phone: str = "+39 0874 123456"
    hours_weekdays: str = "09:00 - 18:00"
    hours_saturday: str = "10:00 - 13:00"
    hours_sunday: str = "Su Prenotazione"
    google_maps_url: str = ""
    booking_email: EmailStr = "info@ilcolletinto.it"
    facebook_url: str = "https://facebook.com"
    instagram_url: str = "https://instagram.com"
    privacy_text: str = ""
    terms_text: str = ""
    seo_title: str = "Il Colle Tinto"
    seo_description: str = "Vini d'eccellenza dal Molise."
    seo_keywords: str = "vino, molise, tintilia"
    seo_image_url: str = ""

class SiteSettings(SettingsUpdate):
    id: Optional[str] = None
