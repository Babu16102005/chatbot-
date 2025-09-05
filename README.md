Career ChatBot — Full Implementation Scaffold (Plain CSS)

What's included:
- Frontend: React + Vite (JS) with plain CSS (no Tailwind/Bootstrap)
- Backend: FastAPI (Python) with:
  * JWT authentication + OTP email verification
  * YouTube Data API integration for searching videos (server-side)
  * OpenAI GPT-4 example usage for ranking/recommendation & summarization (requires API key)
  * Google Gemini placeholder for MCQ generation (configure GEMINI_API_KEY)
  * User progress tracking & level gating (MongoDB)
  * Rate limiting via slowapi
- Dev instructions in dev-setup.md

Important:
- You must provide API keys (YouTube, OpenAI, Google Gemini) and SMTP credentials in backend/.env
- Replace placeholder API calls with your production-safe implementations if needed.
