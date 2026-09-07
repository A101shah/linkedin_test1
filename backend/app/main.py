import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .cache import TTLCache
from .config import settings
from .linkedin import LinkedInAdapter
from .models import SearchRequest, JobResponse

app = FastAPI(title="LinkedIn Insight API", version="1.0.0")
origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
cache = TTLCache(settings.cache_ttl_seconds, settings.redis_url)
adapter = LinkedInAdapter()

@app.get("/health")
async def health():
    return {"status": "ok", "temporary_cache": True, "ttl_seconds": settings.cache_ttl_seconds, "redis": bool(settings.redis_url)}

@app.post("/api/search", response_model=JobResponse)
async def search(request: SearchRequest):
    job_id = str(uuid.uuid4())
    try:
        data = await (adapter.search_person(request.query, request.limit) if request.type == "person" else adapter.search_posts(request.query, request.limit))
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    await cache.set(job_id, {"type": request.type, "query": request.query, "data": data})
    return {"job_id": job_id, "status": "completed", "expires_in_seconds": settings.cache_ttl_seconds}

@app.get("/api/results/{job_id}")
async def results(job_id: str):
    result = await cache.get(job_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Result expired or does not exist")
    return result

@app.delete("/api/results/{job_id}")
async def delete_result(job_id: str):
    await cache.delete(job_id)
    return {"deleted": True}
