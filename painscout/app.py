import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import time
import base64
from datetime import datetime

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from painscout.config import Config
from painscout.scraper import RedditScraper
from painscout.analyzer import PainAnalyzer
from painscout.reporter import Reporter

# --- Page Config ---
st.set_page_config(
    page_title="PainScout.ai | B2B Idea Validator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS & Animations ---
st.markdown("""
<style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    /* 
    --------------------------------------------------
     GLOBAL THEME VARIABLES
    --------------------------------------------------
    */
    :root {
        --bg-primary: #0A0E27;
        --bg-secondary: #111633;
        --text-primary: #FFFFFF;
        --text-secondary: #94A3B8;
        --accent-primary: #00D4FF;
        --accent-secondary: #2962FF;
        --accent-warning: #FF6B6B;
        --glass-bg: rgba(17, 22, 51, 0.7);
        --glass-border: rgba(255, 255, 255, 0.08);
        --shadow-card: 0px 8px 32px rgba(0, 0, 0, 0.12);
    }

    /* Global Reset & Background */
    .stApp {
        background-color: var(--bg-primary);
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(41, 98, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(0, 212, 255, 0.05) 0%, transparent 30%);
        background-attachment: fixed;
        color: var(--text-primary);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Add noise texture */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: url("https://grainy-gradients.vercel.app/noise.svg");
        opacity: 0.02;
        pointer-events: none;
        z-index: 0;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--glass-border);
    }
    
    /* Typography Override */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: var(--text-primary);
    }
    
    h1 {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    p, div, span {
        font-family: 'Plus Jakarta Sans', sans-serif;
        line-height: 1.6;
    }

    /* Hero Tagline */
    .hero-tagline {
        font-size: 1.25rem;
        color: var(--text-secondary);
        font-weight: 400;
        max-width: 600px;
    }

    /* 
    --------------------------------------------------
     COMPONENTS: CARDS & GLASSMORPHISM
    --------------------------------------------------
    */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 32px;
        margin-bottom: 24px;
        box-shadow: var(--shadow-card);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    }
    
    .glass-card:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0px 12px 40px rgba(0, 212, 255, 0.15);
        border-color: rgba(0, 212, 255, 0.3);
    }

    /* Metrics */
    .metric-value {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: -1px;
        background: linear-gradient(180deg, #fff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-top: 8px;
    }

    /* 
    --------------------------------------------------
     INTERACTIVE ELEMENTS
    --------------------------------------------------
    */
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-secondary) 0%, #1E40AF 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.3px;
        box-shadow: 0 4px 20px rgba(41, 98, 255, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(rgba(255,255,255,0.1), transparent);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(41, 98, 255, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(1px);
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        border-radius: 10px;
    }

    /* 
    --------------------------------------------------
     TAGS & BADGES
    --------------------------------------------------
    */
    .category-tag {
        display: inline-flex;
        align-items: center;
        padding: 6px 16px;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(41, 98, 255, 0.1);
        color: #82B1FF;
        border: 1px solid rgba(41, 98, 255, 0.2);
        backdrop-filter: blur(4px);
    }
    
    .urgency-pill {
        padding: 6px 16px;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .urgency-high { 
        background: rgba(255, 107, 107, 0.15); 
        color: #FF6B6B; 
        border: 1px solid rgba(255, 107, 107, 0.3);
        box-shadow: 0 0 15px rgba(255, 107, 107, 0.1);
    }
    
    .urgency-med { 
        background: rgba(255, 171, 64, 0.15); 
        color: #FFAB40; 
        border: 1px solid rgba(255, 171, 64, 0.3);
    }
    
    .urgency-low { 
        background: rgba(0, 212, 255, 0.15); 
        color: #00D4FF; 
        border: 1px solid rgba(0, 212, 255, 0.3);
    }

    .revenue-badge {
        background: linear-gradient(90deg, #059669 0%, #34D399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border: 1px solid rgba(52, 211, 153, 0.3);
        padding: 4px 12px;
        border-radius: 100px;
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-left: 12px;
        display: inline-block;
    }

    /* Sidebar Stats */
    .sidebar-stat {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.85rem;
        color: var(--text-secondary);
        padding: 12px 0;
        border-bottom: 1px solid var(--glass-border);
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: var(--accent-primary);
        box-shadow: 0 0 10px var(--accent-primary);
        animation: pulse 2s infinite;
        display: inline-block;
        margin-right: 8px;
    }

    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Trending Flame Animation */
    @keyframes flame {
        0% { text-shadow: 0 0 10px #FF6B6B; }
        50% { text-shadow: 0 0 20px #FFAB40; }
        100% { text-shadow: 0 0 10px #FF6B6B; }
    }
    
    .trending-icon {
        animation: flame 2s infinite ease-in-out;
    }

</style>
""", unsafe_allow_html=True)

# --- Helpers ---
def show_toast(message, icon="✅"):
    st.toast(f"{icon} {message}")

# --- Session State for Past Scans ---
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []

def save_scan(df):
    scan_id = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.scan_history.append({"id": scan_id, "data": df, "count": len(df)})
    show_toast(f"Scan saved as {scan_id}", "💾")

# --- Sidebar UI ---
with st.sidebar:
    st.markdown("## 🧭 PainScout.ai")
    st.markdown("""
        <div style='font-size: 0.75rem; color: #64748b; margin-bottom: 2.5rem; letter-spacing: 1px; text-transform: uppercase;'>
            v2.1.0 Enterprise Edition
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔧 Discovery Configuration", expanded=True):
        source_type = st.radio("Intelligence Source", ["X (Twitter)", "Reddit"], index=0)
        
        if source_type == "Reddit":
            st.warning("⚠️ Reddit API Access Restricted")
            input_label = "Target Communities"
            default_val = ",".join(Config.DEFAULT_SUBREDDITS)
            help_text = "Comma-separated subreddits"
        else:
            input_label = "Target Keywords"
            default_val = "saas, startup, sales, marketing, agency"
            help_text = "High-intent topics (e.g. #saas, marketing)"

        topics_input = st.text_area(
            input_label, 
            value=default_val,
            help=help_text,
            height=100
        )
        
        if source_type == "Reddit":
            keywords = st.text_area(
                "Pain Triggers",
                value=",".join(Config.DEFAULT_KEYWORDS),
                height=100
            )
        
        days_back = st.slider("Analysis Window (Days)", 7, 90, 30)
    
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 System Status")
    st.markdown("""
        <div class='sidebar-stat'>
            <span>Status</span> 
            <span><span class='status-dot'></span>Online</span>
        </div>
        <div class='sidebar-stat'>
            <span>Last Scan</span> 
            <span style='color: #94A3B8'>Just now</span>
        </div>
        <div class='sidebar-stat'>
            <span>API Usage</span> 
            <span style='color: #00D4FF'>84%</span>
        </div>
        <div class='sidebar-stat'>
            <span>Next Auto-scan</span> 
            <span>6h 24m</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.scan_history:
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        st.markdown("### 📂 History")
        selected_scan = st.selectbox("Load Previous Scan", [s['id'] for s in st.session_state.scan_history])
        if st.button("Load Scan Data", type="secondary"):
            hist_data = next((s['data'] for s in st.session_state.scan_history if s['id'] == selected_scan), None)
            if hist_data is not None:
                st.session_state.results = hist_data
                st.rerun()
    
    st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
    run_btn = st.button("⚡ Initialize Deep Scan", type="primary")

# --- Main Content ---

# 1. Header / Hero
st.markdown("""
<div style='margin-bottom: 60px; padding-top: 20px;'>
    <h1>Discover Unmet Needs. <br>Build What Sells.</h1>
    <p class='hero-tagline'>
        The AI-powered intelligence engine that transforms scattered customer complaints into 
        <span style='color: #00D4FF; font-weight: 600;'>high-value feature requests</span> and revenue opportunities.
    </p>
</div>
""", unsafe_allow_html=True)

# 2. Live Counter (Glass Panel)
st.markdown("""
<div class="glass-card" style="padding: 24px; display: flex; justify-content: space-around; align-items: center;">
    <div style="text-align: center;">
        <div style="color: #94A3B8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Sources Monitored</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #fff;">12,492</div>
    </div>
    <div style="width: 1px; height: 40px; background: rgba(255,255,255,0.1);"></div>
    <div style="text-align: center;">
        <div style="color: #94A3B8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Data Points Processed</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #fff;">1.4M</div>
    </div>
    <div style="width: 1px; height: 40px; background: rgba(255,255,255,0.1);"></div>
    <div style="text-align: center;">
        <div style="color: #00D4FF; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">High Intent Signals</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #00D4FF; text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);">847</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Logic State ---
if 'results' not in st.session_state:
    st.session_state.results = pd.DataFrame()

# --- Execution Logic ---
if run_btn:
    progress_text = "Initializing scout bots..."
    my_bar = st.progress(0, text=progress_text)
    
    scraper = RedditScraper()
    
    # Parse inputs
    topic_list = [s.strip() for s in topics_input.split(',')]
    
    # For Reddit we need the second box, for X we imply intent keywords
    trigger_list = []
    if source_type == "Reddit":
        trigger_list = [k.strip() for k in keywords.split(',')]
    
    try:
        for percent_complete in range(0, 30):
            time.sleep(0.02)
            my_bar.progress(percent_complete, text=f"🛰️ Intercepting {source_type} signals...")
            
        # RUN SCAN
        raw_data = scraper.run_scan(topic_list, trigger_list, days=days_back, source=source_type)
        
        my_bar.progress(50, text=f"Found {len(raw_data)} raw signals. Engaging Neural Engine...")
        
        if raw_data.empty:
            st.warning("No signals detected. Try broadening your search vectors.")
            my_bar.empty()
        else:
            analyzer = PainAnalyzer()
            my_bar.progress(70, text="🧠 Synthesizing pain points & sentiment analysis...")
            
            analyzed_data = analyzer.analyze_batch(raw_data)
            analyzed_data = analyzed_data.dropna(subset=['pain_point'])
            st.session_state.results = analyzed_data
            
            my_bar.progress(100, text="✅ Intelligence Report Generated")
            time.sleep(0.5)
            my_bar.empty()
            st.balloons()
            show_toast("Deep scan completed successfully!")
            
            # Auto-save scan
            save_scan(analyzed_data)
            
    except Exception as e:
        st.error(f"System Error: {str(e)}")

# --- Results Dashboard ---
if not st.session_state.results.empty:
    df = st.session_state.results
    
    st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)
    
    # Trending Section
    st.markdown("### 🔥 Trending This Week")
    t_col1, t_col2, t_col3 = st.columns(3)
    trending_df = df.sort_values('score', ascending=False).head(3)
    
    for i, (idx, row) in enumerate(trending_df.iterrows()):
        with [t_col1, t_col2, t_col3][i]:
            st.markdown(f"""
            <div class="glass-card" style="border-top: 4px solid #FF6B6B;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;">
                    <div class="urgency-pill urgency-high" style="font-size: 0.6rem;">Trending #{i+1}</div>
                    <div class="trending-icon">🔥</div>
                </div>
                <p style="font-size: 1rem; font-weight: 600; line-height: 1.4; margin-bottom: 16px; height: 65px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">
                    "{row['pain_point']}"
                </p>
                <div style="display:flex; gap: 12px; font-size: 0.75rem; color: #94A3B8; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 12px;">
                    <span>💬 {row['comments']} comments</span>
                    <span>⚡ {row['score']} impact</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Key Metrics
    st.markdown("### 🎯 Executive Overview")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    top_cat = df['category'].mode()[0] if not df['category'].empty else "N/A"
    high_urgency = len(df[df['urgency'] == 'High'])
    avg_frust = df['sentiment_score'].mean()
    
    source_label = "X Signals" if source_type == "X (Twitter)" else "Reddit Posts"
    
    with m_col1:
        st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding: 24px;">
                <div class="metric-value">{len(df)}</div>
                <div class="metric-label">{source_label}</div>
            </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding: 24px;">
                <div class="metric-value" style="background: linear-gradient(180deg, #FF6B6B 0%, #C0392B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{high_urgency}</div>
                <div class="metric-label">Critical Pains</div>
            </div>
        """, unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding: 24px;">
                <div class="metric-value" style="background: linear-gradient(180deg, #00D4FF 0%, #0083B0 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{avg_frust:.1f}</div>
                <div class="metric-label">Avg Frustration</div>
            </div>
        """, unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding: 24px;">
                <div class="metric-value" style="font-size: 1.5rem; line-height: 3.5rem; overflow:hidden; white-space:nowrap;">{top_cat}</div>
                <div class="metric-label">Top Category</div>
            </div>
        """, unsafe_allow_html=True)

    # Charts
    col_chart1, col_chart2 = st.columns([1, 1])
    
    with col_chart1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-bottom: 24px'>Market Gaps by Category</h4>", unsafe_allow_html=True)
        
        # Advanced 3D-style Donut Chart
        fig_cat = go.Figure(data=[go.Pie(
            labels=df['category'], 
            hole=.6,
            marker=dict(colors=px.colors.sequential.Plasma),
            textinfo='label+percent',
            textposition='outside',
            pull=[0.1 if i == 0 else 0 for i in range(len(df['category'].unique()))]
        )])
        fig_cat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="white"),
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            height=300
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_chart2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-bottom: 24px'>Urgency Matrix</h4>", unsafe_allow_html=True)
        
        # Advanced Scatter Plot with Gradient Quadrants
        fig_scat = px.scatter(
            df, 
            x='sentiment_score', 
            y='comments', 
            color='urgency', 
            size='sentiment_score', 
            hover_data=['pain_point'], 
            color_discrete_map={'High': '#FF6B6B', 'Medium': '#FFAB40', 'Low': '#00D4FF'}
        )
        fig_scat.update_traces(marker=dict(line=dict(width=1, color='white'), opacity=0.8))
        fig_scat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="white"),
            xaxis=dict(showgrid=False, title="Frustration Score"),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Engagement Volume"),
            margin=dict(t=0, b=0, l=0, r=0),
            height=300,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_scat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Detailed List
    st.markdown("### 📢 High-Value Opportunity Feed")
    
    top_pains = df.sort_values(['sentiment_score', 'comments'], ascending=False).head(10)
    
    for idx, row in top_pains.iterrows():
        u_class = "urgency-low"
        if row['urgency'] == 'Medium': u_class = "urgency-med"
        if row['urgency'] == 'High': u_class = "urgency-high"
        
        score = int(row['sentiment_score'])
        
        # Dynamic Gauge
        gauge_html = ""
        for i in range(10):
            opacity = "1" if i < score else "0.2"
            color = "#FF6B6B" if score > 7 else "#00D4FF"
            gauge_html += f"<span style='display:inline-block; width:6px; height:18px; background:{color}; margin-right:2px; border-radius:2px; opacity:{opacity};'></span>"
        
        revenue_badge = ""
        if row['comments'] > 20 or row['score'] > 100:
            revenue_badge = "<div class='revenue-badge'>High Revenue Potential</div>"
        
        st.markdown(f"""
        <div class="glass-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom: 16px;">
                <div style="display:flex; align-items:center; gap: 12px;">
                    <span class="category-tag">{row['category']}</span>
                    <span class="urgency-pill {u_class}">{row['urgency']}</span>
                    {revenue_badge}
                </div>
                <div style="text-align:right; color: #94A3B8; font-size:0.8rem;">
                    {row['sub_source']} · <span style="color: #fff">{str(row.get('created_at', 'Just now'))[:10]}</span>
                </div>
            </div>
            
            <div style="display:grid; grid-template-columns: 1fr 180px; gap: 32px;">
                <div>
                    <h4 style="font-size:1.25rem; margin-bottom:12px; line-height: 1.4;">
                        "{row['pain_point']}"
                    </h4>
                    <p style="color: #94A3B8; font-size: 0.95rem; margin-bottom: 0; padding-left: 16px; border-left: 2px solid rgba(255,255,255,0.1);">
                        {row['text'][:200]}...
                    </p>
                </div>
                
                <div style="display:flex; flex-direction:column; justify-content:center; align-items: flex-end; border-left: 1px solid rgba(255,255,255,0.05); padding-left: 24px;">
                    <div style="font-size:0.75rem; color:#94A3B8; text-transform:uppercase; letter-spacing:1px; margin-bottom: 8px;">Frustration Score</div>
                    <div style="margin-bottom: 16px;">{gauge_html}</div>
                    
                    <a href="{row['url']}" target="_blank" style="
                        display:inline-block; 
                        background: rgba(255,255,255,0.05); 
                        color: #fff; 
                        text-decoration: none; 
                        padding: 8px 16px; 
                        border-radius: 8px; 
                        font-size: 0.85rem; 
                        font-weight: 600;
                        transition: all 0.2s;
                        border: 1px solid rgba(255,255,255,0.1);
                    ">
                        View Source ↗
                    </a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Exports
    st.markdown("### 📤 Export Intelligence")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        csv = Reporter.get_csv_download_link(df)
        st.download_button("📥 Download CSV Dataset", data=csv, file_name="painscout_data.csv", mime="text/csv", use_container_width=True)
    with col_e2:
        summary_stats = {'total_posts': len(df), 'top_category': top_cat, 'high_urgency_count': high_urgency}
        pdf_bytes = Reporter.generate_pdf(df, summary_stats)
        st.download_button("📄 Download Executive PDF", data=pdf_bytes, file_name="painscout_report.pdf", mime="application/pdf", use_container_width=True)
    
    if st.button("💾 Save Scan to History", key="manual_save"):
        save_scan(df)

else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 60px; opacity: 0.5;">
        <div style="font-size: 5rem; margin-bottom: 1.5rem; filter: drop-shadow(0 0 30px rgba(0, 212, 255, 0.3));">📡</div>
        <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">Ready to intercept signals?</h3>
        <p style="max-width: 400px; margin: 0 auto;">Configure your search vectors in the sidebar and initialize the deep scan engine.</p>
    </div>
    """, unsafe_allow_html=True)
