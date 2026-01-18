from app.db.mongodb import mongodb
import asyncio
from app.core.config import settings

async def list_users():
    await mongodb.connect_to_database()
    users = await mongodb.db.users.find().to_list(10)
    print("--- USERS ---")
    for u in users:
        print(f"Email: {u.get('email')}, Role: {u.get('role')}, HashStart: {u.get('hashed_password')[:10] if u.get('hashed_password') else 'None'}")
    print("--- END ---")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(list_users())
