from app.core.config import settings
import json

print("--- CORS CONFIG CHECK ---")
print(f"Raw CORS_ORIGINS type: {type(settings.CORS_ORIGINS)}")
print(f"Raw CORS_ORIGINS value: {settings.CORS_ORIGINS}")
print(f"Computed cors_origins_list: {settings.cors_origins_list}")
print("--- END CHECK ---")
