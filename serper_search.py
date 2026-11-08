"""Opt-in Serper-compatible search for the GlobeBotter example."""

# Candidate for etheia-agent-map — no equivalent could be inspected (404).
# See: https://github.com/Etheia-Consulting-LLC/etheia-agent-map

import json
import os
from urllib.request import Request, urlopen


class SerperSearch:
    """Return search snippets and source URLs, not full-page contents."""

    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")
        self.base_url = (
            os.getenv("SERPER_BASE_URL") or "https://google.serper.dev"
        ).rstrip("/")

    def run(self, query: str) -> str:
        if not self.api_key:
            raise RuntimeError("Set SERPER_API_KEY for web search")
        request = Request(
            self.base_url + "/search",
            data=json.dumps({"q": query, "num": 5}).encode("utf-8"),
            headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=30) as response:
            data = json.load(response)
        results = [
            {
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            }
            for item in data.get("organic", [])
            if item.get("link")
        ]
        return json.dumps({"results": results}, ensure_ascii=False)
