# app.py
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI-Consumer-Complaint-Risk-Severity-Intelligence",
    page_icon="⚡",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("processed_complaints_sample_output.csv")

# ✅ CRITICAL FIX
df["Date received"] = pd.to_datetime(df["Date received"], errors="coerce")

# ---------------- FUTURISTIC CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@500&display=swap');

* { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background: radial-gradient(circle at top, #1a0b2e, #0d0221 60%, #000000);
}

[data-testid="stSidebar"] {
    background: rgba(20, 15, 40, 0.85);
    backdrop-filter: blur(18px);
    border-right: 2px solid rgba(138,43,226,0.4);
}

.hero {
    padding: 3rem;
    border-radius: 22px;
    background: rgba(20,15,40,0.6);
    backdrop-filter: blur(25px);
    border: 2px solid rgba(138,43,226,0.35);
    text-align: center;
    margin-bottom: 3rem;
}

.hero h1 {
    font-size: 3.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #c4b5fd;
    font-size: 1.3rem;
}

.section-title {
    font-size: 1.9rem;
    font-weight: 700;
    color: #ffffff;
    margin: 2rem 0 1rem 0;
    border-bottom: 2px solid rgba(138,43,226,0.4);
    padding-bottom: .6rem;
}

[data-testid="metric-container"] {
    background: rgba(138,43,226,0.15);
    border: 2px solid rgba(138,43,226,0.4);
    border-radius: 16px;
    padding: 1.8rem;
    box-shadow: 0 0 30px rgba(138,43,226,0.4);
}

[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.3rem;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>⚡ AI-Consumer-Complaint-Risk-Severity-Intelligence</h1>
    <p>Enterprise-grade complaint analytics & risk intelligence dashboard</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🎛️ Filters")

product_filter = st.sidebar.multiselect(
    "Products",
    sorted(df["Product"].dropna().unique()),
    default=df["Product"].dropna().unique()
)

issue_filter = st.sidebar.multiselect(
    "Issues",
    sorted(df["Issue"].dropna().unique()),
    default=df["Issue"].dropna().unique()
)

filtered_df = df[
    df["Product"].isin(product_filter) &
    df["Issue"].isin(issue_filter)
]

# ✅ SAFETY CHECK
if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# ---------------- KPIs ----------------
st.markdown('<div class="section-title">📊 Executive KPIs</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

high_df = filtered_df[filtered_df["Severity"] == "High"]
neg_df = filtered_df[filtered_df["Sentiment"] == "Negative"]

c1.metric("Total Complaints", f"{len(filtered_df):,}")
c2.metric("High Severity %", f"{(len(high_df)/len(filtered_df))*100:.1f}%")
c3.metric("Negative Sentiment", f"{len(neg_df):,}")
c4.metric("Top Risk Product",
          high_df["Product"].value_counts().idxmax()
          if not high_df.empty else "N/A")

# ---------------- TIME TREND ----------------
st.markdown('<div class="section-title">📈 Complaint Trend Over Time</div>', unsafe_allow_html=True)

time_df = filtered_df.groupby("Date received").size().reset_index(name="Count")

fig_time = go.Figure()
fig_time.add_trace(go.Scatter(
    x=time_df["Date received"],
    y=time_df["Count"],
    mode="lines+markers",
    line=dict(color="#a78bfa", width=4),
    marker=dict(size=7),
    fill="tozeroy",
    fillcolor="rgba(167,139,250,0.25)"
))

fig_time.update_layout(
    height=420,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e0d4ff"),
    xaxis_title="Date",
    yaxis_title="Complaints"
)

st.plotly_chart(fig_time, use_container_width=True)

# ---------------- BAR CHART FUNCTION ----------------
def bar_chart(df, x, y, title, colorscale):
    fig = go.Figure(go.Bar(
        y=df[y],
        x=df[x],
        orientation="h",
        text=df[x],
        textposition="inside",
        insidetextanchor="middle",
        cliponaxis=False,
        marker=dict(color=df[x], colorscale=colorscale),
        textfont=dict(size=14, color="white")
    ))
    fig.update_layout(
        height=480,
        title=title,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e0d4ff"),
        margin=dict(l=180, r=40)
    )
    return fig

# ---------------- ISSUES & PRODUCTS ----------------
st.markdown('<div class="section-title">🔥 Key Risk Drivers</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

top_issues = filtered_df["Issue"].value_counts().head(10).reset_index()
top_issues.columns = ["Issue", "Count"]

top_products = filtered_df["Product"].value_counts().head(10).reset_index()
top_products.columns = ["Product", "Count"]

with col1:
    st.plotly_chart(bar_chart(top_issues, "Count", "Issue", "Top Issues", "Plasma"),
                    use_container_width=True)

with col2:
    st.plotly_chart(bar_chart(top_products, "Count", "Product", "Top Products", "Magma"),
                    use_container_width=True)

# ---------------- COMPANIES & SEVERITY ----------------
st.markdown('<div class="section-title">🏢 Organizational Risk</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)

top_companies = filtered_df["Company"].value_counts().head(10).reset_index()
top_companies.columns = ["Company", "Count"]

sev_counts = filtered_df["Severity"].value_counts().reset_index()
sev_counts.columns = ["Severity", "Count"]

with col3:
    st.plotly_chart(bar_chart(top_companies, "Count", "Company",
                              "Top Companies by Complaints", "Viridis"),
                    use_container_width=True)

with col4:
    fig_sev = go.Figure(go.Pie(
        labels=sev_counts["Severity"],
        values=sev_counts["Count"],
        hole=0.45,
        pull=[0.08 if s == "High" else 0 for s in sev_counts["Severity"]],
        textinfo="label+value+percent"
    ))
    fig_sev.update_layout(
        height=480,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e0d4ff"),
        title="Severity Distribution"
    )
    st.plotly_chart(fig_sev, use_container_width=True)

# ---------------- HIGH-RISK TABLE ----------------
st.markdown('<div class="section-title">🚨 High-Risk Priority Matrix</div>', unsafe_allow_html=True)

high_df = filtered_df[filtered_df["Severity"] == "High"]

if high_df.empty:
    st.warning("⚠️ No High-Severity complaints found for selected filters.")
else:
    risk_table = (
        high_df
        .groupby(["Company", "Product", "Issue"])
        .agg(High_Risk_Count=("Severity", "count"))
        .reset_index()
        .sort_values("High_Risk_Count", ascending=False)
        .head(15)
    )

    st.dataframe(
        risk_table.style
        .background_gradient(subset=["High_Risk_Count"], cmap="Reds")
        .format({"High_Risk_Count": "{:,}"}),
        use_container_width=True,
        height=420
    )

