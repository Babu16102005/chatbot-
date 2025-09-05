import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
client = MongoClient(MONGODB_URI)
db = client['career_chatbot']
users = db['users']
otps = db['otps']
progress = db['progress']
# helper
class _DB: pass
_db = _DB()
_db.client = client
_db.db = db
_db.users = users
_db.otps = otps
_db.progress = progress
