import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import UserInDB
from datetime import datetime

async def create_admin():
    print(f"Connecting to MongoDB at {settings.MONGO_URI}...")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client.get_default_database()
    users_collection = db["users"]

    # Check if admin exists
    existing_admin = await users_collection.find_one({"email": "admin@colleshop.it"})
    if existing_admin:
        print("Admin user already exists (admin@colleshop.it).")
        return

    print("Creating admin user...")
    admin_user = {
        "email": "admin@colleshop.it",
        "full_name": "Amministratore",
        "hashed_password": get_password_hash("admin123"),
        "is_active": True,
        "is_superuser": True,
        "role": "admin"
    }

    result = await users_collection.insert_one(admin_user)
    print(f"Admin user created successfully with ID: {result.inserted_id}")
    print("Email: admin@colleshop.it")
    print("Password: admin123")

if __name__ == "__main__":
    try:
        asyncio.run(create_admin())
    except Exception as e:
        import traceback
        traceback.print_exc()
