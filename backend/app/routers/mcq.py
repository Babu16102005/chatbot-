from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..core import ai, security
router = APIRouter()

class MCQInput(BaseModel):
    text: str
    level: str = 'basic'

@router.post('/generate')
async def generate_mcq(req: MCQInput, user=Depends(security.get_current_user)):
    mcqs = ai.generate_mcq(req.text, req.level)
    return {'mcqs': mcqs}
