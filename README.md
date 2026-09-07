# LinkedIn Insight Pipeline

A full-stack, ephemeral LinkedIn data acquisition and analysis prototype. The application is designed around permitted/authorized LinkedIn API access and keeps requested data only briefly in a TTL cache rather than building a permanent archive.

## Architecture

Next.js frontend → FastAPI backend → acquisition adapter → ephemeral TTL storage → JSON API.

The LinkedIn adapter intentionally does not bypass LinkedIn controls, CAPTCHA, rate limits, authentication, or access restrictions. Configure an approved LinkedIn API integration before using live acquisition.

## Local development

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000` for the frontend.

## Live LinkedIn access

The project includes a `LinkedInAdapter` with environment-based credentials and a safe demo provider. Live endpoints should only be enabled for APIs and scopes that your LinkedIn application is approved to use. LinkedIn's current documentation restricts several profile/post APIs and permissions.

## Temporary storage

The default backend cache is an in-process TTL cache. `CACHE_TTL_SECONDS` controls retention. For horizontally scaled deployment, replace it with a short-TTL Redis/Upstash adapter without changing the API layer.
