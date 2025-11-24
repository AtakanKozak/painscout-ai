import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "PainScout.ai/1.0")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Mock Mode: Enable if keys are missing
    MOCK_MODE = os.getenv("MOCK_MODE", "False").lower() == "true" or not (REDDIT_CLIENT_ID and GEMINI_API_KEY)

    # Search Configuration
    DEFAULT_SUBREDDITS = ["SaaS", "Entrepreneur", "startups", "sales", "marketing", "smallbusiness"]
    DEFAULT_KEYWORDS = [
        "need a tool that", 
        "wish there was", 
        "hate when", 
        "integration sucks", 
        "biggest problem", 
        "manual work", 
        "too expensive",
        "alternative to",
        "pain point"
    ]
