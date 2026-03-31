import os
from dotenv import load_dotenv
from huggingface_hub import HfApi

load_dotenv()
api = HfApi()

files = ["agent.py", "tools.py", "telegram_bot.py", "memory.py", "news.py", "requirements.txt", "brain.py", "subconscious.py", "train.py"]

for file in files:
    api.upload_file(
        path_or_fileobj=file,
        path_in_repo=file,
        repo_id="nyxtesla/samaham-omniagent",
        repo_type="space",
        token=os.getenv("HF_KEY")
    )
    print(f"Uploaded {file} ✓")