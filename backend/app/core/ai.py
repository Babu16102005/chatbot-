import os, openai, requests
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY

def rank_videos(query, candidates: list):
    # Use a light prompt to rank by educational usefulness, clarity, and recency.
    # If OPENAI_KEY not provided, return candidates unchanged.
    if not OPENAI_KEY:
        return candidates
    prompt = f"""You are an expert educational curator.
Rank the following candidate YouTube videos for a learner searching for: {query}
Return a JSON array of objects with fields: title, url, views, score (0-100), reason.
Candidates:
{candidates}
"""
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{'role':'system','content':'You rank educational videos.'},
                      {'role':'user','content':prompt}],
            max_tokens=500,
            temperature=0.2
        )
        txt = resp['choices'][0]['message']['content']
        # Attempt to parse JSON from model — this is best-effort
        import json
        parsed = json.loads(txt)
        return parsed
    except Exception as e:
        print('OpenAI rank error', e)
        return candidates

def summarize_video(video_url: str, topics: list[str]=[]):
    # Ideally: fetch captions via youtube-transcript-api, chunk and call LLM for summarization.
    # Here we call OpenAI with a short stub if available.
    if not OPENAI_KEY:
        return {'title':'Sample Video','summary':'Summary placeholder','topics':topics}
    prompt = f"""Summarize the educational content of the video: {video_url}
Provide a short paragraph summary and bullet points for key topics.
Topics to emphasize: {topics}
Keep answer under 300 words.
"""
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{'role':'user','content':prompt}],
            max_tokens=500,
            temperature=0.2
        )
        return {'title': video_url, 'summary': resp['choices'][0]['message']['content'], 'topics': topics}
    except Exception as e:
        print('OpenAI summarize error', e)
        return {'title': video_url, 'summary':'Error generating summary', 'topics':topics}

def generate_mcq(text: str, level: str='basic'):
    # Placeholder: call Google Gemini or use OpenAI if GEMINI_KEY not present
    if GEMINI_KEY:
        # Insert code to call Gemini API here
        # For now, stub:
        return [{'q':'What is X?','options':['A','B','C','D'],'answer':0,'explanation':'Because...'}]
    if OPENAI_KEY:
        prompt = f"""Generate 3 multiple choice questions (4 options each) from the following material for level {level}. Return JSON array with fields q, options, answer (index), explanation.
Material:
{text}
"""
        try:
            resp = openai.ChatCompletion.create(
                model='gpt-4',
                messages=[{'role':'user','content':prompt}],
                max_tokens=700,
                temperature=0.3
            )
            import json
            txt = resp['choices'][0]['message']['content']
            parsed = json.loads(txt)
            return parsed
        except Exception as e:
            print('OpenAI MCQ error', e)
            return [{'q':'Sample?','options':['A','B','C','D'],'answer':0,'explanation':'stub'}]
    return [{'q':'Sample?','options':['A','B','C','D'],'answer':0,'explanation':'stub'}]
