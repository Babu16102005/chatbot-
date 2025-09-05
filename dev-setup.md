Development & Build Instructions (VS Code)

Prereqs:
- Node.js >=16, npm
- Python 3.10+
- MongoDB (local or Atlas)

1) Backend
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
Create a .env file in backend/ with:
  MONGODB_URI=<your mongodb uri>
  JWT_SECRET=<strong secret>
  SMTP_HOST=<smtp host> (optional)
  SMTP_PORT=<smtp port>
  SMTP_USER=<smtp user>
  SMTP_PASS=<smtp pass>
  YOUTUBE_API_KEY=<youtube data api key>
  OPENAI_API_KEY=<openai key>
  GEMINI_API_KEY=<google gemini key placeholder>
Run:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

2) Frontend
cd frontend
npm install
npm run dev
Open http://localhost:5173 in Brave to test video streaming links.

Notes:
- The backend shows OTP in console if SMTP is not configured.
- The AI integrations are implemented as examples. Monitor your API usage and enable rate limits.
