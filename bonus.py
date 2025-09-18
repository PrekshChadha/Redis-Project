#!/usr/bin/env python3
"""
  pip install redisvl sentence-transformers
"""

import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

try:
    from redisvl.extensions.router import Route, SemanticRouter
    from redisvl.utils.vectorize import HFTextVectorizer
except Exception as e:
    raise SystemExit(
        "Missing dependencies. Install with: pip install redisvl sentence-transformers\nError: " + str(e)
    )

genai = Route(
    name="GenAI",
    references=[
        "what is generative ai",
        "chatgpt and language models",
        "llm architectures and fine-tuning",
        "prompt engineering"
    ],
    metadata={"category": "GenAI"},
    distance_threshold=0.72
)

scifi = Route(
    name="science_fiction_entertainment",
    references=[
        "best sci-fi movies and books",
        "space opera recommendations",
        "dune and science fiction films"
    ],
    metadata={"category": "entertainment"},
    distance_threshold=0.72
)

classical = Route(
    name="classical_music",
    references=[
        "recommend classical pieces",
        "beethoven mozart chopin",
        "structure of a symphony"
    ],
    metadata={"category": "music"},
    distance_threshold=0.70
)

# --- Build router ---
# Change redis_url if your Redis is at another host/port


redis_url = os.environ.get("REDIS_URL", "redis://172.16.22.22:16041")

router = SemanticRouter(
    name="topic-router",
    vectorizer=HFTextVectorizer(),        
    routes=[genai, scifi, classical],
    redis_url=redis_url,
    overwrite=True                        
)

queries = [
    "I love Chopin",
    "How do I fine-tune an LLM for code generation?",
    "Recommend a space opera novel",
    "How many moons do we have?",
    "what is 10 + 20?",
]

for q in queries:
    match = router(q)             
    print(match.name if match.name else "No route matched")
