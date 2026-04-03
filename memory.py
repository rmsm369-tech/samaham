import json
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

short_term = []

# Load from HF Dataset on startup
try:
    from huggingface_hub import hf_hub_download
    path = hf_hub_download(
        repo_id="nyxtesla/samaham-omniagent",
        filename="memory.json",
        repo_type="space",
        token=os.getenv("HF_KEY")
    )
    with open(path) as f:
        long_term = json.load(f)
    print("Memory loaded from HF ✓")
except:
    try:
        with open("memory.json") as f:
            long_term = json.load(f)
    except:
        long_term = []

def observe(thought, importance):
    short_term.append(thought)
    if importance > 0.7:
        long_term.append({
            "thought": thought,
            "time": datetime.now().isoformat()
        })
        save_long_term()

def save_long_term():
    with open("memory.json", "w") as f:
        json.dump(long_term, f)
    try:
        from huggingface_hub import HfApi
        api = HfApi()
        api.upload_file(
            path_or_fileobj="memory.json",
            path_in_repo="memory.json",
            repo_id="nyxtesla/samaham-omniagent",
            repo_type="space",
            token=os.getenv("HF_KEY")
        )
    except:
        pass

def forget_short_term():
    short_term.clear()
    print("Short term cleared. Only what mattered survived.")
   
if __name__ == "__main__":
    observe("test memory", importance=0.8)
    forget_short_term()
    print(long_term)