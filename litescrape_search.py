"""Opt-in native Google search for the GlobeBotter example."""

# Candidate for etheia-agent-map — no equivalent could be inspected (404).
# See: https://github.com/Etheia-Consulting-LLC/etheia-agent-map

import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class LitescrapeSearch:
    """Return search snippets and source URLs, not full-page contents."""

    def __init__(self):
        self.api_key = os.getenv("LITESCRAPE_API_KEY")
        self.base_url = (
            os.getenv("LITESCRAPE_BASE_URL") or "https://api.litescrape.com"
        ).rstrip("/")

    def run(self, query: str) -> str:
        if not self.api_key:
            raise RuntimeError("Set LITESCRAPE_API_KEY for web search")
        url = self.base_url + "/api/google/search?" + urlencode({"q": query, "num": 5})
        request = Request(url, headers={"Authorization": f"Bearer {self.api_key}"})
        with urlopen(request, timeout=30) as response:
            data = json.load(response)
        results = [
            {
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            }
            for item in data.get("organic_results", [])
            if item.get("link")
        ]
        return json.dumps({"results": results}, ensure_ascii=False)
