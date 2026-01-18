from app.db.mongodb import mongodb
import asyncio
from app.core.security import get_password_hash

async def reset_admin():
    print("Connecting to DB...")
    await mongodb.connect_to_database()
    print("Connected.")
    
    # New password
    new_password = "admin123"
    hashed_password = get_password_hash(new_password)
    print(f"Generated Hash: {hashed_password}")
    
    # Update Admin
    email = "admin@colleshop.it"
    print(f"Updating {email}...")
    result = await mongodb.db.users.update_one(
        {"email": email},
        {"$set": {"hashed_password": hashed_password}}
    )
    print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

    # Update User
    email_user = "user@colleshop.it"
    print(f"Updating {email_user}...")
    result_user = await mongodb.db.users.update_one(
        {"email": email_user},
        {"$set": {"hashed_password": hashed_password}}
    )
    print(f"Matched: {result_user.matched_count}, Modified: {result_user.modified_count}")
    
    print("Done.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(reset_admin())
    except Exception as e:
        print(f"Error: {e}")
