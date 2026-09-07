from datetime import datetime, timezone
import httpx
from .config import settings

class LinkedInAdapter:
    """Authorized acquisition adapter. Demo data is used until an approved API token is configured."""

    async def search_person(self, query: str, limit: int):
        if not settings.linkedin_access_token:
            return [self._demo_profile(query)]
        # Keep live acquisition behind an explicit approved API integration.
        # Do not add browser automation, CAPTCHA solving, proxy rotation, or access-control bypasses.
        raise RuntimeError("Live LinkedIn acquisition is not configured. Add an approved LinkedIn API integration and implement its permitted endpoint here.")

    async def search_posts(self, query: str, limit: int):
        if not settings.linkedin_access_token:
            return [self._demo_post(query, i) for i in range(min(limit, 5))]
        raise RuntimeError("Live LinkedIn post search is not configured. Use an approved API/permission set.")

    def _demo_profile(self, query: str):
        now = datetime.now(timezone.utc).isoformat()
        return {
            "id": "demo-profile",
            "name": query.title(),
            "headline": "Demo profile — connect an approved LinkedIn API for live data",
            "location": "Not available in demo mode",
            "about": "This result demonstrates the complete request → acquisition → TTL cache → API → UI pipeline without storing LinkedIn data permanently.",
            "profile_url": "https://www.linkedin.com/",
            "experience": [{"title": "Example role", "company": "Example company", "start": "2024", "end": "Present"}],
            "education": [{"school": "Example University", "degree": "Data Science"}],
            "skills": ["Python", "Data Science", "Machine Learning", "APIs"],
            "fetched_at": now,
        }

    def _demo_post(self, query: str, index: int):
        now = datetime.now(timezone.utc).isoformat()
        return {
            "id": f"demo-post-{index}",
            "author": "Demo Author",
            "text": f"Demo result for topic: {query}. Connect an approved LinkedIn API to replace this sample with live permitted data.",
            "posted_at": now,
            "url": "https://www.linkedin.com/",
            "engagement": {"reactions": 0, "comments": 0},
            "topic": query,
        }
