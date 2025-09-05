from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..core import ai, security, youtube
router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    lang: str = 'en'

@router.post('/search')
async def search(req: SearchRequest, user=Depends(security.get_current_user)):
    # 1) Fetch candidates from YouTube Data API
    candidates = youtube.search_youtube(req.query, max_results=8, lang=req.lang)
    # 2) Rank / annotate using LLM (OpenAI GPT-4) for best educational picks
    ranked = ai.rank_videos(req.query, candidates)
    return {'results': ranked}

class SummarizeRequest(BaseModel):
    video_url: str
    topics: list[str] = []

@router.post('/summarize')
async def summarize(req: SummarizeRequest, user=Depends(security.get_current_user)):
    # Summarize: fetch captions (if available) and call LLM
    summary = ai.summarize_video(req.video_url, topics=req.topics)
    return {'summary': summary}
