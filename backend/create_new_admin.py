from app.db.mongodb import mongodb
import asyncio
from app.core.security import get_password_hash
from app.models.user import UserCreate

async def create_admin():
    print("Connecting to DB...")
    await mongodb.connect_to_database()
    print("Connected.")
    
    email = "newadmin@colleshop.it"
    password = "admin123"
    full_name = "Nuovo Admin"
    
    # Check if exists
    existing = await mongodb.db.users.find_one({"email": email})
    if existing:
        print(f"User {email} already exists. Deleting...")
        await mongodb.db.users.delete_one({"email": email})
    
    hashed_password = get_password_hash(password)
    print(f"Generated Hash: {hashed_password}")
    
    user_data = {
        "email": email,
        "hashed_password": hashed_password,
        "full_name": full_name,
        "role": "admin",
        "is_active": True,
        "shipping_address": {},
        "billing_address": {}
    }
    
    print(f"Creating user {email}...")
    result = await mongodb.db.users.insert_one(user_data)
    print(f"User created with ID: {result.inserted_id}")
    print("Done.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(create_admin())
    except Exception as e:
        print(f"Error: {e}")
