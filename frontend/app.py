import os
import requests
import pandas as pd
import streamlit as st
from pyvis.network import Network

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000") + "/api"

st.set_page_config(page_title="Anti-India Campaign Monitor", layout="wide")

st.title("Cyber Threat Detection: Anti-India Campaigns")

tabs = st.tabs(["Alerts", "Posts", "Keywords", "Graph", "Trends", "Influencers"])

with tabs[0]:
    st.subheader("Live Alerts")
    r = requests.get(f"{API_BASE}/alerts/")
    alerts = r.json() if r.ok else []
    if alerts:
        df = pd.DataFrame(alerts)
        st.dataframe(df)
    else:
        st.info("No alerts yet. Ingest posts to trigger alerts.")

with tabs[1]:
    st.subheader("Recent Posts")
    r = requests.get(f"{API_BASE}/posts/")
    posts = r.json() if r.ok else []
    if posts:
        df = pd.DataFrame(posts)
        st.dataframe(df[["id", "platform", "author_handle", "stance", "toxicity", "created_at", "text"]])
    else:
        st.info("No posts yet.")

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
    st.dataframe(pd.DataFrame(kws))

with tabs[3]:
    st.subheader("Graph Preview (sample)")
    # Simple local visualization: users and hashtags from posts list
    r = requests.get(f"{API_BASE}/posts/")
    posts = r.json() if r.ok else []
    net = Network(height="600px", width="100%", directed=True, notebook=False)
    users = {}
    tags = {}
    for p in posts[:200]:
        u = p.get("author_handle") or p.get("author_id") or "anon"
        if u not in users:
            net.add_node(f"u:{u}", label=u, color="#1976d2")
            users[u] = True
        for h in p.get("hashtags", [])[:5]:
            if h not in tags:
                net.add_node(f"h:{h}", label=f"#{h}", color="#43a047")
                tags[h] = True
            net.add_edge(f"u:{u}", f"h:{h}")
    html_path = "/tmp/graph.html"
    net.show(html_path)
    with open(html_path, "r", encoding="utf-8") as f:
        st.components.v1.html(f.read(), height=620, scrolling=True)

with tabs[4]:
    st.subheader("Engagement & Risk Trends")
    r = requests.get(f"{API_BASE}/analytics/trends")
    series = r.json() if r.ok else []
    if series:
        df = pd.DataFrame(series)
        st.line_chart(df.set_index("time")["count"], height=250)
        st.line_chart(df.set_index("time")["anti_ratio"], height=250)
        st.line_chart(df.set_index("time")["avg_toxicity"], height=250)
    else:
        st.info("No trend data yet.")

with tabs[5]:
    st.subheader("Influencer Leaderboard")
    r = requests.get(f"{API_BASE}/analytics/influencers")
    infl = r.json() if r.ok else []
    if infl:
        df = pd.DataFrame(infl)
        st.dataframe(df)
    else:
        st.info("No influencer data yet.")


