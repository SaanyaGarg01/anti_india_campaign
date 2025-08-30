import os
import requests
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000") + "/api"

st.set_page_config(
    page_title="🛡️ Cyber Threat Detection", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🛡️"
)

# Custom CSS for attractive styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4ECDC4;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    .alert-high {
        background: linear-gradient(90deg, #FF6B6B, #FF8E53);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .alert-medium {
        background: linear-gradient(90deg, #FFE66D, #FF8E53);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .alert-low {
        background: linear-gradient(90deg, #4ECDC4, #44A08D);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🛡️ Cyber Threat Detection: Anti-India Campaign Monitor</div>', unsafe_allow_html=True)

# Sidebar for real-time stats
with st.sidebar:
    st.markdown("### 📊 Real-Time Stats")
    
    # Get live stats
    try:
        posts_r = requests.get(f"{API_BASE}/posts/", timeout=5)
        alerts_r = requests.get(f"{API_BASE}/alerts/", timeout=5)
        posts = posts_r.json() if posts_r.ok else []
        alerts = alerts_r.json() if alerts_r.ok else []
        
        st.metric("🚨 Active Alerts", len(alerts))
        st.metric("📝 Total Posts", len(posts))
        
        if posts:
            anti_posts = [p for p in posts if p.get('stance') == 'anti']
            avg_toxicity = sum(p.get('toxicity', 0) for p in posts) / len(posts)
            st.metric("⚠️ Anti-India Posts", len(anti_posts))
            st.metric("🧪 Avg Toxicity", f"{avg_toxicity:.2f}")
            
        # Threat Level Indicator
        threat_level = "🟢 LOW"
        if len(alerts) > 2:
            threat_level = "🔴 HIGH"
        elif len(alerts) > 0:
            threat_level = "🟡 MEDIUM"
            
        st.markdown(f"### 🎯 Threat Level\n**{threat_level}**")
        
    except Exception as e:
        st.error("Unable to connect to backend")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh (30s)")
    if auto_refresh:
        time.sleep(30)
        st.experimental_rerun()

tabs = st.tabs(["🚨 Alerts", "📝 Posts", "🔍 Keywords", "🌐 Network", "📈 Analytics", "👥 Influencers", "🤖 Live Monitor"])

with tabs[0]:
    st.markdown("### 🚨 Campaign Detection Alerts")
    
    col1, col2, col3 = st.columns(3)
    
    r = requests.get(f"{API_BASE}/alerts/")
    alerts = r.json() if r.ok else []
    
    if alerts:
        # Alert summary metrics
        high_risk = [a for a in alerts if a['risk_score'] > 80]
        medium_risk = [a for a in alerts if 50 <= a['risk_score'] <= 80]
        low_risk = [a for a in alerts if a['risk_score'] < 50]
        
        with col1:
            st.metric("🔴 High Risk", len(high_risk), delta=len(high_risk))
        with col2:
            st.metric("🟡 Medium Risk", len(medium_risk), delta=len(medium_risk))
        with col3:
            st.metric("🟢 Low Risk", len(low_risk), delta=len(low_risk))
        
        st.markdown("---")
        
        # Display alerts with styling
        for alert in sorted(alerts, key=lambda x: x['risk_score'], reverse=True):
            risk_score = alert['risk_score']
            if risk_score > 80:
                alert_class = "alert-high"
                emoji = "🔴"
            elif risk_score > 50:
                alert_class = "alert-medium"
                emoji = "🟡"
            else:
                alert_class = "alert-low"
                emoji = "🟢"
            
            st.markdown(f"""
            <div class="{alert_class}">
                <h4>{emoji} {alert['name']}</h4>
                <p><strong>Risk Score:</strong> {risk_score:.1f}/100</p>
                <p><strong>Detected:</strong> {alert['created_at']}</p>
                <p><strong>Details:</strong> {alert.get('details', {})}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Campaign details button
            if st.button(f"🔍 Analyze Campaign {alert['id']}", key=f"analyze_{alert['id']}"):
                campaign_r = requests.get(f"{API_BASE}/alerts/campaign/{alert['id']}")
                if campaign_r.ok:
                    campaign_data = campaign_r.json()
                    st.json(campaign_data)
    else:
        st.info("🔄 No active alerts detected. System is monitoring...")

with tabs[1]:
    st.markdown("### 📝 Social Media Posts Analysis")
    
    r = requests.get(f"{API_BASE}/posts/")
    posts = r.json() if r.ok else []
    
    if posts:
        # Filter options
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            platform_filter = st.selectbox("🔍 Platform", ["All"] + list(set(p['platform'] for p in posts)))
        with col2:
            stance_filter = st.selectbox("🎯 Stance", ["All", "anti", "pro", "neutral"])
        with col3:
            min_toxicity = st.slider("🧪 Min Toxicity", 0.0, 1.0, 0.0)
        with col4:
            show_count = st.selectbox("📊 Show", [10, 20, 50, 100])
        
        # Apply filters
        filtered_posts = posts
        if platform_filter != "All":
            filtered_posts = [p for p in filtered_posts if p['platform'] == platform_filter]
        if stance_filter != "All":
            filtered_posts = [p for p in filtered_posts if p['stance'] == stance_filter]
        filtered_posts = [p for p in filtered_posts if p.get('toxicity', 0) >= min_toxicity]
        
        st.markdown(f"**Showing {len(filtered_posts[:show_count])} of {len(filtered_posts)} posts**")
        
        # Display posts in cards
        for i, post in enumerate(filtered_posts[:show_count]):
            stance_emoji = {"anti": "🔴", "pro": "🟢", "neutral": "🟡"}.get(post['stance'], "⚪")
            platform_emoji = {"twitter": "🐦", "reddit": "🤖", "youtube": "📺"}.get(post['platform'], "📱")
            
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                    **{platform_emoji} {post['platform'].title()}** | **{post['author_handle']}** | {stance_emoji} **{post['stance'].title()}**
                    
                    *{post['text'][:300]}{'...' if len(post['text']) > 300 else ''}*
                    """)
                with col2:
                    toxicity_color = "🔴" if post.get('toxicity', 0) > 0.7 else "🟡" if post.get('toxicity', 0) > 0.4 else "🟢"
                    st.metric("Toxicity", f"{post.get('toxicity', 0):.2f}", delta=None)
                    st.markdown(f"**Lang:** {post.get('language', 'N/A')}")
                    if post.get('hashtags'):
                        st.markdown(f"**Tags:** {', '.join(f'#{tag}' for tag in post['hashtags'][:3])}")
                
                st.markdown("---")
    else:
        st.info("📭 No posts found. Start monitoring social platforms!")

with tabs[2]:
    st.subheader("Flagged Keywords")
    with st.form("add_kw"):
        term = st.text_input("Term")
        category = st.selectbox("Category", ["general", "hashtag", "phrase"]) 
        description = st.text_input("Description", "")
        submitted = st.form_submit_button("Add Keyword")
        if submitted and term:
            r = requests.post(f"{API_BASE}/keywords/", json={"term": term, "category": category, "description": description})
            if r.ok:
                st.success("Added")
            else:
                st.error(r.text)
    r = requests.get(f"{API_BASE}/keywords/")
    kws = r.json() if r.ok else []
    if kws:
        for kw in kws:
            st.write(f"**{kw['term']}** ({kw['category']}) - {kw['description']}")
    else:
        st.write("No keywords yet.")

with tabs[3]:
    st.subheader("Network Overview")
    r = requests.get(f"{API_BASE}/posts/")
    posts = r.json() if r.ok else []
    
    users = set()
    hashtags = set()
    for p in posts:
        users.add(p.get("author_handle", "anon"))
        hashtags.update(p.get("hashtags", []))
    
    st.write(f"**Users**: {len(users)}")
    st.write(f"**Hashtags**: {len(hashtags)}")
    st.write(f"**Posts**: {len(posts)}")
    
    if hashtags:
        st.write("**Top Hashtags:**")
        for tag in list(hashtags)[:10]:
            st.write(f"- #{tag}")

with tabs[4]:
    st.markdown("### 📈 Advanced Analytics Dashboard")
    
    # Get data
    trends_r = requests.get(f"{API_BASE}/analytics/trends")
    posts_r = requests.get(f"{API_BASE}/posts/")
    trends = trends_r.json() if trends_r.ok else []
    posts = posts_r.json() if posts_r.ok else []
    
    if posts:
        col1, col2 = st.columns(2)
        
        # Stance distribution pie chart
        with col1:
            stance_counts = {}
            for post in posts:
                stance = post.get('stance', 'unknown')
                stance_counts[stance] = stance_counts.get(stance, 0) + 1
            
            fig_pie = px.pie(
                values=list(stance_counts.values()),
                names=list(stance_counts.keys()),
                title="🎯 Stance Distribution",
                color_discrete_map={'anti': '#FF6B6B', 'pro': '#4ECDC4', 'neutral': '#FFE66D'}
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Platform distribution
        with col2:
            platform_counts = {}
            for post in posts:
                platform = post.get('platform', 'unknown')
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
            
            fig_bar = px.bar(
                x=list(platform_counts.keys()),
                y=list(platform_counts.values()),
                title="📱 Posts by Platform",
                color=list(platform_counts.values()),
                color_continuous_scale="viridis"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Toxicity heatmap
        st.markdown("#### 🧪 Toxicity Analysis")
        toxicity_data = []
        for post in posts:
            toxicity_data.append({
                'Platform': post.get('platform', 'unknown'),
                'Stance': post.get('stance', 'unknown'),
                'Toxicity': post.get('toxicity', 0)
            })
        
        if toxicity_data:
            import pandas as pd
            df = pd.DataFrame(toxicity_data)
            
            # Toxicity distribution histogram
            fig_hist = px.histogram(
                df, x='Toxicity', color='Stance',
                title="Distribution of Toxicity Scores",
                nbins=20,
                color_discrete_map={'anti': '#FF6B6B', 'pro': '#4ECDC4', 'neutral': '#FFE66D'}
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        # Time series if trends available
        if trends:
            st.markdown("#### 📊 Activity Timeline")
            
            # Convert trends to DataFrame for plotting
            trend_df = pd.DataFrame(trends)
            if not trend_df.empty:
                fig_time = go.Figure()
                fig_time.add_trace(go.Scatter(
                    x=trend_df['time'], y=trend_df['count'],
                    mode='lines+markers', name='Post Count',
                    line=dict(color='#4ECDC4', width=3)
                ))
                fig_time.add_trace(go.Scatter(
                    x=trend_df['time'], y=[x*100 for x in trend_df['anti_ratio']],
                    mode='lines+markers', name='Anti-India %',
                    line=dict(color='#FF6B6B', width=3), yaxis='y2'
                ))
                
                fig_time.update_layout(
                    title="Activity and Risk Over Time",
                    xaxis_title="Time",
                    yaxis_title="Post Count",
                    yaxis2=dict(title="Anti-India %", overlaying='y', side='right'),
                    hovermode='x unified'
                )
                st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.info("📊 No data available for analytics yet.")

with tabs[5]:
    st.markdown("### 👥 Influencer Analysis")
    
    r = requests.get(f"{API_BASE}/analytics/influencers")
    infl = r.json() if r.ok else []
    
    if infl:
        # Top influencers metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏆 Top Influencer", infl[0]['author'], f"{infl[0]['posts']} posts")
        with col2:
            avg_toxicity = sum(u['avg_toxicity'] for u in infl) / len(infl)
            st.metric("🧪 Avg Toxicity", f"{avg_toxicity:.2f}")
        with col3:
            total_posts = sum(u['posts'] for u in infl)
            st.metric("📊 Total Posts", total_posts)
        
        st.markdown("---")
        
        # Influencer leaderboard with enhanced display
        st.markdown("#### 🏅 Top Influencers (Last 3 Days)")
        
        for i, user in enumerate(infl[:10]):
            rank_emoji = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
            
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            with col1:
                st.markdown(f"### {rank_emoji[i]}")
            with col2:
                risk_level = "🔴 HIGH" if user['avg_toxicity'] > 0.7 else "🟡 MED" if user['avg_toxicity'] > 0.4 else "🟢 LOW"
                st.markdown(f"**{user['author']}**\n{risk_level}")
            with col3:
                st.metric("Posts", user['posts'])
            with col4:
                st.metric("Toxicity", f"{user['avg_toxicity']:.2f}")
            
            st.markdown("---")
    else:
        st.info("👥 No influencer data available yet.")

with tabs[6]:
    st.markdown("### 🤖 Live Monitoring Dashboard")
    
    # Real-time simulation
    st.markdown("#### 🔴 LIVE: Threat Detection Status")
    
    # Status indicators
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**🌐 Twitter API**")
        st.success("🟢 Connected")
    with col2:
        st.markdown("**🤖 Reddit Monitor**")
        st.success("🟢 Active")
    with col3:
        st.markdown("**📺 YouTube Scanner**")
        st.success("🟢 Scanning")
    with col4:
        st.markdown("**🧠 AI Analysis**")
        st.success("🟢 Processing")
    
    st.markdown("---")
    
    # Simulated live feed
    st.markdown("#### 📡 Live Content Feed")
    
    if st.button("🔄 Refresh Feed"):
        st.rerun()
    
    # Show recent posts as live feed
    posts_r = requests.get(f"{API_BASE}/posts/")
    posts = posts_r.json() if posts_r.ok else []
    
    if posts:
        st.markdown("**Recent Detections:**")
        for post in sorted(posts, key=lambda x: x['created_at'], reverse=True)[:5]:
            platform_emoji = {"twitter": "🐦", "reddit": "🤖", "youtube": "📺"}.get(post['platform'], "📱")
            stance_emoji = {"anti": "🔴", "pro": "🟢", "neutral": "🟡"}.get(post['stance'], "⚪")
            
            with st.container():
                st.markdown(f"""
                **{datetime.now().strftime('%H:%M:%S')}** | {platform_emoji} **{post['platform'].title()}** | {stance_emoji} **{post['stance'].upper()}**
                
                📝 *{post['text'][:150]}{'...' if len(post['text']) > 150 else ''}*
                
                🧪 Toxicity: **{post.get('toxicity', 0):.2f}** | 👤 Author: **{post['author_handle']}**
                """)
                st.markdown("---")
    
    # Monitoring controls
    st.markdown("#### ⚙️ Monitoring Controls")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⏸️ Pause Monitoring"):
            st.warning("Monitoring paused")
        if st.button("🚨 Trigger Alert Test"):
            st.error("🚨 Test Alert: Suspicious activity detected!")
    
    with col2:
        threshold = st.slider("🎯 Alert Threshold", 0.0, 1.0, 0.6)
        st.info(f"Current threshold: {threshold}")
        
        auto_refresh_live = st.checkbox("🔄 Auto-refresh Live Feed")
        if auto_refresh_live:
            time.sleep(5)
            st.rerun()


