from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, EmailStr
from ..core import db, security, email_utils
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

router = APIRouter()

class RegisterInput(BaseModel):
    email: EmailStr
    password: str

class LoginInput(BaseModel):
    email: EmailStr
    password: str

@router.post('/register')
async def register(data: RegisterInput, background: BackgroundTasks):
    existing = db.users.find_one({'email': data.email})
    if existing:
        raise HTTPException(400, 'Email already registered')
    user = {
        'email': data.email,
        'password': security.hash_password(data.password),
        'is_verified': False,
        'created_at': datetime.utcnow(),
        'progress': {'level':'basic', 'score':0, 'tests':[]}
    }
    res = db.users.insert_one(user)
    otp = security.generate_otp()
    db.otps.insert_one({'email': data.email, 'otp': security.hash_otp(otp), 'expires_at': datetime.utcnow() + timedelta(minutes=10)})
    background.add_task(email_utils.send_otp_email, data.email, otp)
    return {'message':'registered, otp sent'}

@router.post('/verify-otp')
async def verify_otp(email: EmailStr, otp: str):
    rec = db.otps.find_one({'email': email})
    if not rec:
        raise HTTPException(404, 'OTP not found')
    if rec['expires_at'] < datetime.utcnow():
        raise HTTPException(400, 'OTP expired')
    if not security.verify_otp(rec['otp'], otp):
        raise HTTPException(400, 'Invalid OTP')
    db.users.update_one({'email': email}, {'$set':{'is_verified':True}})
    db.otps.delete_many({'email': email})
    return {'message':'verified'}

@router.post('/login')
async def login(data: LoginInput):
    user = db.users.find_one({'email': data.email})
    if not user or not security.verify_password(data.password, user['password']):
        raise HTTPException(400, 'Invalid credentials')
    if not user.get('is_verified', False):
        raise HTTPException(403, 'Email not verified')
    token = security.create_access_token({'sub': str(user['_id']), 'email': user['email']})
    return {'access_token': token, 'token_type':'bearer'}

@router.get('/me')
async def me(user=Depends(security.get_current_user)):
    user_data = dict(user)
    user_data['_id'] = str(user_data['_id'])  # convert ObjectId to string
    return jsonable_encoder(user_data)
