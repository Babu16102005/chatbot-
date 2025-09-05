import os, jwt, hmac, hashlib
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from bson.objectid import ObjectId
from . import db
from dotenv import load_dotenv
load_dotenv()

pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
JWT_SECRET = os.getenv('JWT_SECRET', 'devsecret')
ALGORITHM = 'HS256'
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)

def verify_password(plain, hashed):
    return pwd_ctx.verify(plain, hashed)

def create_access_token(data: dict, expires_minutes: int = 60*24):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({'exp': expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return token

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get('sub')
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            raise HTTPException(401, 'Invalid token')
        user.pop('password', None)
        return user
    except Exception:
        raise HTTPException(401, 'Invalid token')

import secrets, string
def generate_otp(length:int=6):
    alphabet = string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def hash_otp(otp:str):
    return hashlib.sha256(otp.encode()).hexdigest()

def verify_otp(hashed_otp, otp_plain):
    return hmac.compare_digest(hashed_otp, hashlib.sha256(otp_plain.encode()).hexdigest())
