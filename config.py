from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()

# Access any environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM_MODE = "gemini"  # or "local"
LLM_MODE = "groq"  # or "local"
# LLM_MODE = "openai"  # or "local"
