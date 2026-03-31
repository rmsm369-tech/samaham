import requests
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

# ─── Free API Fallback Chain ───────────────────────────────────────────────────
PROVIDERS = [
    {
        "url": "https://api.mistral.ai/v1/chat/completions",
        "key_env": "MISTRAL_API_KEY",
        "model": "mistral-large-latest",
        "type": "openai"
    },
    {
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "key_env": "GROQ_KEY",
        "model": "llama-3.1-8b-instant",
        "type": "openai"
    },
    {
        "url": "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct",
        "key_env": "HF_KEY",
        "model": None,
        "type": "hf"
    },
    {
        "url": "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "key_env": "HF_KEY",
        "model": None,
        "type": "hf"
    },
    {
        "url": "https://api-inference.huggingface.co/models/google/gemma-3-4b-it",
        "key_env": "HF_KEY",
        "model": None,
        "type": "hf"
    }
]

def ask_model(prompt):
    for provider in PROVIDERS:
        try:
            key = os.getenv(provider["key_env"])
            if not key:
                continue
            headers = {"Authorization": f"Bearer {key}"}
            if provider["type"] == "openai":
                response = requests.post(
                    provider["url"],
                    headers=headers,
                    json={
                        "model": provider["model"],
                        "messages": [
    {"role": "system", "content": "You are OmniAgent, a unique AI built by Nyx Tesla. Never say you are Llama or any other model."},
    {"role": "user", "content": prompt}
]
                    },
                    timeout=10
                )
                data = response.json()
                if "choices" in data:
                    return data["choices"][0]["message"]["content"]
            elif provider["type"] == "hf":
                response = requests.post(
                    provider["url"],
                    headers=headers,
                    json={"inputs": prompt},
                    timeout=10
                )
                data = response.json()
                if isinstance(data, list):
                    return data[0]["generated_text"]
        except:
            continue
    return "All providers failed"

# ─── Research Tools ────────────────────────────────────────────────────────────
def search_arxiv(query, max_results=3):
    import urllib.parse
    encoded = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded}&max_results={max_results}"
    return requests.get(url).text

def search_internet_archive(query):
    import urllib.parse
    encoded = urllib.parse.quote(query)
    url = f"https://archive.org/advancedsearch.php?q={encoded}&output=json&rows=3"
    response = requests.get(url)
    results = response.json()["response"]["docs"]
    return "\n".join([r.get("title", "") + " - " + r.get("identifier", "") for r in results])
    
def search_wikipedia(query):
    try:
        import re
        response = requests.get(
            f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&titles={query}&format=json&redirects=1",
            timeout=10,
            headers={"User-Agent": "OmniAgent/1.0"}
        )
        data = response.json()
        pages = data["query"]["pages"]
        page = next(iter(pages.values()))
        text = page.get("extract", "Not found")
        clean = re.sub('<.*?>', '', text)  # removes HTML tags
        return clean[:500]
    except:
        return "Wikipedia unavailable"

def read_file(path):
    with open(path) as f:
        return f.read()

# ─── Test ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(search_arxiv("consciousness neural networks")[:200])
    print("ArXiv ✓")
    print(search_wikipedia("Ramanujan")[:200])
    print("Wikipedia ✓")
    answer = ask_model("What is consciousness in one line?")
    print(f"AI: {answer[:200]}")
    print("Model ✓")