import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import UserInDB
import traceback

async def create_user():
    print(f"Connecting to MongoDB at {settings.MONGO_URI}...")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client.get_default_database()
    users_collection = db["users"]

    # Check if user exists
    existing_user = await users_collection.find_one({"email": "user@colleshop.it"})
    if existing_user:
        print("Test user already exists (user@colleshop.it).")
        return

    print("Creating test user...")
    test_user = {
        "email": "user@colleshop.it",
        "full_name": "Mario Rossi",
        "hashed_password": get_password_hash("user123"),
        "is_active": True,
        "is_superuser": False,
        "role": "user"
    }

    result = await users_collection.insert_one(test_user)
    print(f"Test user created successfully with ID: {result.inserted_id}")
    print("Email: user@colleshop.it")
    print("Password: user123")

if __name__ == "__main__":
    try:
        asyncio.run(create_user())
    except Exception as e:
        traceback.print_exc()
