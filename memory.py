import json
from datetime import datetime

short_term = []

# Load existing long term memory on startup
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

def forget_short_term():
    short_term.clear()
    print("Short term cleared. Only what mattered survived.")

if __name__ == "__main__":
    observe("test thought", importance=0.8)
    forget_short_term()