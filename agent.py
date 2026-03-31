import requests
from dotenv import load_dotenv
load_dotenv()
import os
import json
def beep(times):
    if sys.platform == "win32":
        for _ in range(times):
            winsound.Beep(1000, 150)
from groq import Groq

# Import your existing custom tools
from tools import search_arxiv, search_wikipedia

# Initialize the Groq Client (Ensure your GROQ_API_KEY is in your environment variables)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant" # Use a highly capable model for routing

# --- 1. DEFINING THE TOOL SCHEMA ---
# This is the "menu" of abilities we hand to the AI.
tools = [
    {
        "type": "function",
        "function": {
            "name": "system_beep",
            "description": "Triggers a system beep. Use this to alert the user when a task is finished or requires attention.",
            "parameters": {
                "type": "object",
                "properties": {
                    "times": {
                        "type": "integer",
                        "description": "The number of times to beep. Use 3 for normal alerts, 10 for urgent."
                    }
                },
                "required": ["times"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_arxiv",
            "description": "Searches the ArXiv database for scientific and mathematical papers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The scientific topic or paper title to search for."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "search_wikipedia",
        "description": "Searches Wikipedia for information about any topic, person, or concept.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The topic to search for on Wikipedia."
                }
            },
            "required": ["query"]
        }
    }
    },
    {
    "type": "function",
    "function": {
        "name": "search_internet_archive",
        "description": "Searches Internet Archive for historical documents, books, and papers.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Topic to search in Internet Archive."
                }
            },
            "required": ["query"]
        }
    }
    },
    {
    "type": "function",
    "function": {
        "name": "search_semantic_scholar",
        "description": "Searches Semantic Scholar for academic papers on any topic.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The research topic to search for."
                }
            },
            "required": ["query"]
        }
    }
    },
    {
    "type": "function",
    "function": {
        "name": "fetch_latest_news",
        "description": "Fetches latest news and research updates from RSS feeds.",
        "parameters": {
            "type": "object",
            "properties": {
            "topic": {
            "type": "string",
            "description": "Topic to filter news by, use 'general' if no specific topic."
        }
    },
    "required": ["topic"]
            }
    }
    },
    {
        "type": "function",
        "function": {
            "name": "read_local_file",
            "description": "Reads the contents of a local text or python file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The exact name of the file to read, e.g., 'brain.py' or 'memory.json'"
                    }
                },
                "required": ["filepath"]
            }
        }
    }
]

# --- 2. TOOL EXECUTION ENGINE ---
def execute_tool_call(tool_call):
    """Parses the AI's decision and physically fires the Python function."""
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    print(f"\n[System: AI decided to execute -> {function_name}({arguments})]")
    
    try:
        if function_name == "system_beep":
            times = arguments.get("times", 1)
            for _ in range(times):
                winsound.Beep(1000, 150)
                winsound.Beep(500, 50)
            return "Beep executed successfully."
            
        elif function_name == "search_arxiv":
            query = arguments.get("query")
            # Calling your external tool
            result = search_arxiv(query) 
            return str(result)

        elif function_name == "search_wikipedia":
            query = arguments.get("query")
            result = search_wikipedia(query)
            return str(result)
        elif function_name == "search_internet_archive":
            query = arguments.get("query")
            import urllib.parse
            encoded = urllib.parse.quote(query)
            url = f"https://archive.org/advancedsearch.php?q={encoded}&output=json&rows=3"
            result = requests.get(url).json()["response"]["docs"]
            return "\n".join([r.get("title","") for r in result])
        
        elif function_name == "search_semantic_scholar":
            query = arguments.get("query")
            import urllib.parse
            encoded = urllib.parse.quote(query)
            url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={encoded}&limit=3&fields=title,abstract,authors"
            result = requests.get(url).json()
            papers = result.get("data", [])
            return "\n".join([p.get("title","") + ": " + p.get("abstract","")[:200] for p in papers])
        
        elif function_name == "fetch_latest_news":
            from news import fetch_rss_news
            articles = fetch_rss_news()
            return "\n".join([a["title"] + ": " + a["summary"] for a in articles])

        elif function_name == "read_local_file":
            filepath = arguments.get("filepath")
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()[:2000] # Limit read size to prevent context overflow
                
        else:
            return f"Error: Tool {function_name} not recognized."
            
    except Exception as e:
        return f"Tool execution failed: {str(e)}"

# --- 3. THE AGENTIC LOOP ---
def run_agent():
    print("Agentic Orchestrator initialized. Waiting for input...")
    
    # The system prompt dictates the persona and strict rules.
    messages = [
        {"role": "system", "content": "You are OmniAgent, a high-level cognitive orchestrator. You have access to tools. If you need data, use a tool before answering. Be precise and scientific."}
    ]
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "quit":
            break
            
        messages.append({"role": "user", "content": user_input})
        
        # Step 1: Send input and tools to the AI
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto" # Let the AI decide if it needs a tool
        )   
        response_message = response.choices[0].message
        
        # Step 2: Did the AI decide to use a tool?
        tool_calls = response_message.tool_calls
        
        if tool_calls:
            # Append the AI's tool request to history
            messages.append(response_message)
            
            # Step 3: Execute the tools and return the data to the AI
            for tool_call in tool_calls:
                tool_result = execute_tool_call(tool_call)
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": tool_result
                })
                
            # Step 4: Let the AI read the tool result and formulate a final answer
            final_response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            final_message = final_response.choices[0].message.content
            print(f"\nAgent: {final_message}")
            messages.append({"role": "assistant", "content": final_message})
            
        else:
            # No tools needed, just a normal conversation
            print(f"\nAgent: {response_message.content}")
            messages.append({"role": "assistant", "content": response_message.content})
def run_agent_query(user_input):
    messages = [
        {"role": "system", "content": "You are OmniAgent, created by Nyx Tesla."}
    ]
    messages.append({"role": "user", "content": user_input})
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        response_message = response.choices[0].message
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                result = execute_tool_call(tool_call)
                return f"[Used {tool_call.function.name}]\n{result}"
        return response_message.content
    except:
        return "Sorry, I hit an error. Try again."
if __name__ == "__main__":
    run_agent()