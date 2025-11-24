# PainScout.ai - B2B Idea Validator

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.8+
- A Reddit Account
- A Google Account (for Gemini API)

### 2. Installation
1. Clone the repository.
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration (API Keys)

**Step A: Get Reddit API Credentials**
1. Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click "Create Another App..." (or "Create App")
3. Select **"script"**
4. Name: `PainScout`
5. Redirect URI: `http://localhost:8501` (doesn't matter much for script apps, but required)
6. Create it. You will see a **Client ID** (under the name) and a **Client Secret**.

**Step B: Get Gemini API Key**
1. Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Create an API key for free.

**Step C: Update .env file**
1. Rename `.env.example` to `.env`
2. Paste your keys into the file.

### 4. Running the App
Run the following command in your terminal:
```bash
streamlit run painscout/app.py
```

---

## 🎨 Branding & Assets

### Color Palette
- **Primary Blue:** `#2962FF` (Trust, Tech, Reliability)
- **Deep Navy:** `#1A237E` (Professionalism, Depth)
- **Alert Red:** `#D50000` (High Urgency Pain Points)
- **Background:** `#F5F7FA` (Clean SaaS aesthetic)

### Logo Concept
**Symbol:** A stylized radar/sonar sweep combining a magnifying glass.
**Font:** Sans-serif, bold, modern (e.g., Montserrat or Inter).
**Vibe:** "We see what others miss."

---

## 📄 Marketing Assets

### Landing Page Copy

**Headline:** Discover the exact pains your customers are begging to be solved.
**Subheadline:** PainScout.ai scans thousands of conversations on Reddit & X in seconds to reveal unmet B2B needs, so you can build features that sell themselves.

**3 Key Benefits:**
1. **Stop Guessing:** Validate your SaaS ideas with real-time frustration data, not gut feelings.
2. **Steal Competitor Traffic:** Find users complaining about "Tool X" and offer them your solution immediately.
3. **Save 100+ Hours:** Automate market research that usually takes weeks of manual scrolling.

---

### 📧 Cold Outreach Templates (LinkedIn)

**Template 1: The "I saw your post" Approach**
> Subject: Your post about [Problem Topic]
> 
> Hi [Name],
> 
> I saw your comment on r/SaaS about how frustrating it is to [Specific Pain Point]. I'm building a tool called PainScout to solve exactly that by [Solution]. 
> 
> Would love your feedback on our prototype if you have 5 mins?
> 
> Best, [Your Name]

**Template 2: The Founder Validation**
> Subject: Quick question about [Industry]
> 
> Hey [Name], I noticed you're active in the [Industry] space. I'm analyzing common integration headaches for B2B founders and noticed [Pain Point] comes up a lot.
> 
> Is this something you struggle with too?
> 
> Cheers, [Your Name]

**Template 3: The Beta Invite**
> Subject: Building a solution for [Pain Point]
> 
> Hi [Name],
> 
> We're quietly building a tool that fixes [Pain Point] without the bloat of [Competitor]. 
> 
> Since you mentioned looking for an alternative recently, I'd love to give you early access. Let me know!
> 
> [Your Name]

