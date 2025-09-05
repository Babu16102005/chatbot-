from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..core import db, security
from bson.objectid import ObjectId

router = APIRouter()

class ProgressUpdate(BaseModel):
    user_id: str
    delta_score: int = 0
    level: str | None = None
    test_result: dict | None = None

@router.post('/update')
async def update_progress(p: ProgressUpdate, user=Depends(security.get_current_user)):
    # Only allow user to update their own progress
    if str(user['_id']) != p.user_id:
        raise HTTPException(403, 'Forbidden')
    update = {}
    if p.delta_score:
        update['$inc'] = {'progress.score': p.delta_score}
    if p.level:
        update.setdefault('$set', {})['progress.level'] = p.level
    if p.test_result:
        update.setdefault('$push', {})['progress.tests'] = p.test_result
    db.users.update_one({'_id': ObjectId(p.user_id)}, update)
    u = db.users.find_one({'_id': ObjectId(p.user_id)})
    u.pop('password', None)
    return {'user': u}
