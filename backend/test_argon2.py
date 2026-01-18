from passlib.context import CryptContext
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
    hash = pwd_context.hash("test_password")
    print(f"SUCCESS: Hash created: {hash}")
    verify = pwd_context.verify("test_password", hash)
    print(f"SUCCESS: Verification result: {verify}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
