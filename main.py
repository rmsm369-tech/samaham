from tools import ask_model, search_arxiv
from memory import observe, forget_short_term
from subconscious import start
from brain import AwarenessDecayNetwork
import torch
import os
import json
import winsound

# Load brain
brain = AwarenessDecayNetwork()
if os.path.exists("brain_weights.pth"):
    brain.load_state_dict(torch.load("brain_weights.pth"))
    print("Brain loaded ✓")

def get_memory_context():
    try:
        with open("memory.json") as f:
            past = json.load(f)
        return " ".join([m["thought"] for m in past[-3:]])
    except:
        return ""

def beep(times):
    for _ in range(times):
        winsound.Beep(1000, 150)
        winsound.Beep(500, 50)  # small gap

def run():
    print("OmniAgent starting...")
    start()
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        
        observe(user_input, importance=0.8)
        
        x = torch.randn(2)
        _, confidence, vetoed = brain(x)
        print(f"[Veto: {'SILENT' if vetoed else 'SPEAK'} | Confidence: {confidence:.2f}]")
        
        if vetoed:
            print("Agent: [Silence]")
        elif any(word in user_input.lower() for word in ["research", "paper", "find"]):
            results = search_arxiv(user_input)
            print("Agent: Found papers on ArXiv.")
        else:
            context = get_memory_context()
            prompt = f"Context: {context}\nUser: {user_input}" if context else user_input
            response = ask_model(prompt)
            print(f"Agent: {response}")
            
        # FIX: Indented the action properly and aligned it with the main loop
        if any(word in user_input.lower() for word in ["research", "paper", "find", "calculate", "solve", "search"]):
            beep(0)  # specific task
        else:
            beep(0)   # general chat
        
        forget_short_term()

if __name__ == "__main__":
    run()