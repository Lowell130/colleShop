
from pydantic import BaseModel, EmailStr, Field, ConfigDict, BeforeValidator
from typing import Optional, Annotated
from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class Address(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    role: str = "user"
    tax_code: Optional[str] = None
    shipping_address: Optional[Address] = None
    billing_address: Optional[Address] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    tax_code: Optional[str] = None
    shipping_address: Optional[Address] = None
    billing_address: Optional[Address] = None

class UserInDB(UserBase):
    hashed_password: str

class User(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
