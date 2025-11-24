import google.generativeai as genai
import pandas as pd
import json
from painscout.config import Config
import time
import random

class PainAnalyzer:
    def __init__(self):
        self.mock_mode = Config.MOCK_MODE
        if not self.mock_mode:
            if not Config.GEMINI_API_KEY:
                 self.mock_mode = True
            else:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-pro')

    def analyze_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        df['pain_point'] = None
        df['sentiment_score'] = 0
        df['category'] = None
        df['target_audience'] = None
        df['urgency'] = 'Low'
        
        print("Starting AI analysis..." if not self.mock_mode else "Starting Mock AI Analysis...")
        
        for index, row in df.iterrows():
            content = f"Title: {row['title']}\nBody: {row['text'][:500]}"
            if len(content) < 20:
                continue
                
            try:
                if self.mock_mode:
                    analysis = self._mock_analyze(content)
                else:
                    analysis = self._analyze_single_post(content)
                    # Rate limit safety
                    time.sleep(1) 

                if analysis:
                    df.at[index, 'pain_point'] = analysis.get('pain_point')
                    df.at[index, 'sentiment_score'] = analysis.get('frustration_score', 0)
                    df.at[index, 'category'] = analysis.get('category')
                    df.at[index, 'target_audience'] = analysis.get('target_audience')
                    df.at[index, 'urgency'] = analysis.get('urgency')
                
            except Exception as e:
                print(f"Error analyzing post {index}: {e}")
                continue
                
        return df

    def _analyze_single_post(self, text: str) -> dict:
        prompt = f"""
        Analyze the following social media post for B2B software pain points.
        Return ONLY a raw JSON object (no markdown formatting) with the following keys:
        - "pain_point": Brief summary of the problem/need (max 10 words).
        - "frustration_score": Integer 1-10 (10 being extremely frustrated/urgent).
        - "category": One of [Integration, Pricing, UI/UX, Missing Feature, Customer Support, Performance].
        - "target_audience": Guessed role or industry (e.g., "Marketing Agency", "Developer").
        - "urgency": "High", "Medium", or "Low".
        
        If no clear pain point exists, return null.

        Post content:
        {text}
        """
        
        try:
            response = self.model.generate_content(prompt)
            cleaned_text = response.text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
                
            data = json.loads(cleaned_text)
            return data
        except Exception:
            return None

    def _mock_analyze(self, text: str) -> dict:
        """Simulates AI analysis for demo purposes."""
        categories = ["Integration", "Pricing", "UI/UX", "Missing Feature", "Performance"]
        urgencies = ["High", "Medium", "Low"]
        
        # Simple keyword matching to make mock data feel slightly real
        lower_text = text.lower()
        category = "Missing Feature"
        if "price" in lower_text or "expensive" in lower_text: category = "Pricing"
        elif "integrate" in lower_text or "connect" in lower_text: category = "Integration"
        elif "slow" in lower_text or "buggy" in lower_text: category = "Performance"
        
        return {
            "pain_point": f"User struggle with {category.lower()} issues",
            "frustration_score": random.randint(5, 10),
            "category": category,
            "target_audience": "SaaS Founder",
            "urgency": random.choice(urgencies)
        }
