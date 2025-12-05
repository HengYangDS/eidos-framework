import os
import json
import urllib.request
import urllib.error
from typing import Protocol, Any, Dict, List, Optional
from ..zero.symbolism.ast import Graph
from ..system.logging import get_logger

logger = get_logger(__name__)

class CognitiveDriver(Protocol):
    """
    Protocol for AI Agents (LLMs) that interface with Eidos.
    """
    
    async def synthesize_code(self, intent: str, context: Optional[Graph] = None) -> str:
        """
        Generates Eidos DSL code based on user intent and current graph context.
        """
        ...

    async def diagnose_error(self, error_trace: str, data_sample: Any) -> str:
        """
        Analyzes an error and provides a diagnosis or fix suggestion.
        """
        ...

    async def compute_embedding(self, text: List[str]) -> List[List[float]]:
        """
        Computes vector embeddings for semantic routing.
        """
        ...

class OpenAIDriver:
    """
    Implementation using OpenAI API.
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.embedding_url = "https://api.openai.com/v1/embeddings"

    def _post(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            # Fallback to mock if no key is present (for testing/offline)
            if "embeddings" in url:
                return {"data": [{"embedding": [0.1] * 1536} for _ in payload.get("input", [])]}
            return {
                "choices": [{
                    "message": {
                        "content": f"# [MOCK] AI Generated code for: {payload.get('messages', [{}])[-1].get('content')}\nfrom eidos import Source, Sink\nflow = Source('mock') >> Sink('mock')"
                    }
                }]
            }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            logger.error("OpenAI API HTTP error", error=str(e))
            return {
                "choices": [{"message": {"content": f"# Error calling OpenAI: {e}"}}]
            }
        except Exception as e:
            logger.exception("Network error calling OpenAI")
            return {
                "choices": [{"message": {"content": f"# Network Error: {e}"}}]
            }

    async def synthesize_code(self, intent: str, context: Optional[Graph] = None) -> str:
        system_prompt = """You are Eidos Nous, an AI coding assistant for the Eidos Logic Operating System.
Your goal is to translate natural language intent into valid Python code using the Eidos DSL.

Key Concepts:
- Use `Source("uri")`, `Map(fn)`, `Filter(fn)`, `Sink("uri")`.
- Operators: `>>` (Pipe), `|` (Choice), `&` (Parallel).
- Output ONLY Python code. No markdown blocks, no explanations.
"""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\nIntent: {intent}"}
            ],
            "temperature": 0.0
        }
        
        response = self._post(self.api_url, payload)
        content = response["choices"][0]["message"]["content"]
        # Strip potential markdown code blocks
        if content.startswith("```python"):
            content = content.split("\n", 1)[1]
        if content.endswith("```"):
            content = content.rsplit("\n", 1)[0]
        return content.strip()

    async def diagnose_error(self, error_trace: str, data_sample: Any) -> str:
        system_prompt = "You are an expert debugger for Eidos pipelines. Analyze the traceback and data sample to provide a fix suggestion."
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Error:\n{error_trace}\n\nSample Data:\n{data_sample}"}
            ]
        }
        response = self._post(self.api_url, payload)
        return response["choices"][0]["message"]["content"]

    async def compute_embedding(self, text: List[str]) -> List[List[float]]:
        if not self.api_key:
             # Mock for tests without API key
            return [[0.1] * 1536 for _ in text]
            
        payload = {
            "model": "text-embedding-3-small",
            "input": text
        }
        response = self._post(self.embedding_url, payload)
        return [item["embedding"] for item in response["data"]]
