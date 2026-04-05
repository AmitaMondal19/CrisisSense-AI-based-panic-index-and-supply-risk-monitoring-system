from ml_model import ml_predict
import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import time
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="CrisisSense", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.stMetric {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='color:#ff4b4b;'>🔴 CrisisSense</h1>
<p style='color:gray;'>AI Monitoring System for Panic vs Reality</p>
""", unsafe_allow_html=True)

st.markdown("""
<marquee style='color:orange; font-size:16px;'>
🚨 Fuel prices rising | ⚠️ Panic buying in Delhi | 🟢 Supply stable in Kolkata | 📈 Demand increasing
</marquee>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA (FIXED) ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

panic_path = os.path.join(BASE_DIR, "data", "panic_data.csv")
price_path = os.path.join(BASE_DIR, "data", "price_data.csv")

panic_df = pd.read_csv(panic_path)
price_df = pd.read_csv(price_path)
price_df["date"] = pd.to_datetime(price_df["date"])

# ---------------- SIDEBAR ----------------
city_list = [
    "Kolkata", "Delhi", "Mumbai", "Chennai", "Bangalore",
    "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow"
]

commodity = st.sidebar.selectbox(
    "Select Commodity",
    ["All", "Rice", "Fuel", "Cooking Oil", "Vegetables"]
)

city = st.sidebar.selectbox("Select City", city_list)

# ---------------- PANIC LOGIC ----------------
keywords_high = ["shortage", "panic", "running out", "queues"]
keywords_medium = ["rising", "increase", "demand"]

# def compute_panic_score(df):
#     score = 0
#     count = len(df)

#     if count == 0:
#         return 0.2

#     for _, row in df.iterrows():
#         base = row["panic_score"]
#         text = row["headline"].lower()

#         if any(word in text for word in keywords_high):
#             base += 0.2
#         elif any(word in text for word in keywords_medium):
#             base += 0.1

#         score += base

#     return min(score / count, 1.0)

def compute_panic_score(df):
    score = 0
    count = len(df)

    if count == 0:
        return 0.2

    for _, row in df.iterrows():
        text = row["headline"].lower()

        # Original dataset score
        base = row["panic_score"]

        # Keyword boost
        keyword_boost = 0
        if any(word in text for word in keywords_high):
            keyword_boost = 0.2
        elif any(word in text for word in keywords_medium):
            keyword_boost = 0.1

        # ML prediction 🔥
        ml_score = ml_predict(text)

        # FINAL COMBINATION 🔥
        combined = (0.5 * base) + (0.3 * keyword_boost) + (0.2 * ml_score)

        score += combined

    return min(score / count, 1.0)

# ---------------- FILTER DATA ----------------
filtered_panic = panic_df[panic_df["location"] == city]
if filtered_panic.empty:
    filtered_panic = panic_df.sample(10).copy()
    filtered_panic["location"] = city

if commodity == "All":
    filtered_price = price_df[price_df["city"] == city]
else:
    filtered_price = price_df[
        (price_df["commodity"] == commodity) &
        (price_df["city"] == city)
    ]

if filtered_price.empty:
    filtered_price = price_df.sample(20).copy()
    filtered_price["city"] = city

# ---------------- CALCULATIONS ----------------
panic_score = compute_panic_score(filtered_panic)

latest = filtered_price["price"].iloc[-1]
avg = filtered_price["price"].mean()
std = filtered_price["price"].std()

price_change = (latest - avg) / avg
volatility = std / avg if avg != 0 else 0

panic_index = int((panic_score * 0.5 + price_change * 0.3 + volatility * 0.2) * 100)
panic_index = max(0, min(panic_index, 100))

confidence = int((1 - volatility) * 100)
confidence = max(50, min(confidence, 95))

# ---------------- REAL vs FAKE ----------------
if panic_score > 0.6 and abs(price_change) < 0.05:
    panic_type = "🚨 Fake Panic (Hype)"
elif panic_score > 0.6 and abs(price_change) >= 0.05:
    panic_type = "⚠️ Real Panic (Actual Shortage)"
else:
    panic_type = "✅ Normal Situation"

# ---------------- DECISION ----------------
if panic_index < 30 and price_change < 0.05:
    decision = "🟢 Do Not Panic"
elif panic_index < 60:
    decision = "🟡 Monitor Situation"
else:
    decision = "🔴 Possible Shortage"

# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Panic Index", panic_index)

with col2:
    st.metric("Confidence", f"{confidence}%")

with col3:
    st.metric("Decision", decision)

st.progress(confidence / 100)

# ---------------- STATUS ----------------
if "Do Not Panic" in decision:
    st.success("System Status: Stable")
elif "Monitor" in decision:
    st.warning("System Status: Watch Closely")
else:
    st.error("System Status: High Risk")

# ---------------- PANIC TYPE ----------------
st.markdown("### 🧠 Panic Analysis")

if "Fake" in panic_type:
    st.error(panic_type)
elif "Real" in panic_type:
    st.warning(panic_type)
else:
    st.success(panic_type)

# ---------------- TOP ALERT ----------------
st.markdown("### 🚨 Top Alert")
top_alert = filtered_panic.sort_values(by="panic_score", ascending=False).iloc[0]["headline"]
st.error(top_alert)

st.markdown("---")

# ---------------- PANIC VS REALITY ----------------
st.markdown("### 📊 Panic vs Reality")

colA, colB = st.columns(2)

with colA:
    st.metric("Panic Score", round(panic_score * 100))

with colB:
    reality = int((1 - abs(price_change)) * 100)
    st.metric("Reality Score", reality)

gap = abs((panic_score * 100) - reality)

if gap > 40 and "Fake" in panic_type:
    st.error("⚠️ High Mismatch: Panic Likely Exaggerated")
elif gap > 20:
    st.warning("⚠️ Moderate Gap")
else:
    st.success("✅ Panic matches Reality")

st.markdown("---")

# ---------------- PRICE TREND ----------------
left, right = st.columns([2, 1])

with left:
    st.subheader("📈 Price Trend")

    if commodity == "All":
        pivot_df = filtered_price.pivot_table(
            index="date",
            columns="commodity",
            values="price"
        )
        st.line_chart(pivot_df)
    else:
        st.line_chart(filtered_price.set_index("date")["price"])

# ---------------- LIVE FEED ----------------
with right:
    st.subheader("🐦 Live Social Feed")

    posts = filtered_panic["headline"].sample(5).tolist()

    for post in posts:
        st.markdown(f"• {post}")
        time.sleep(0.1)

st.markdown("---")

# ---------------- MAP ----------------
st.subheader("🗺️ Crisis Heatmap")

city_coords = {
    "Kolkata": [22.5726, 88.3639],
    "Delhi": [28.7041, 77.1025],
    "Mumbai": [19.0760, 72.8777],
    "Chennai": [13.0827, 80.2707],
    "Bangalore": [12.9716, 77.5946],
    "Hyderabad": [17.3850, 78.4867],
    "Pune": [18.5204, 73.8567],
    "Ahmedabad": [23.0225, 72.5714],
    "Jaipur": [26.9124, 75.7873],
    "Lucknow": [26.8467, 80.9462]
}

m = folium.Map(location=[22.5, 80], zoom_start=5, tiles="CartoDB positron")

for c in city_coords:
    lat, lon = city_coords[c]
    subset = panic_df[panic_df["location"] == c]
    score = compute_panic_score(subset)
    p_index = int(score * 100)

    color = "green" if p_index < 30 else "orange" if p_index < 60 else "red"

    folium.CircleMarker(
        location=[lat, lon],
        radius=6 + p_index * 0.1,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.9,
        popup=f"{c} - Panic Index: {p_index}"
    ).add_to(m)

st_folium(m, width=900, height=500)

st.markdown("---")

# ---------------- CITY COMPARISON ----------------
st.subheader("🌍 City Comparison (Panic vs Reality)")

city_analysis = []

for c in city_coords:
    panic_subset = panic_df[panic_df["location"] == c]
    price_subset = price_df[price_df["city"] == c]

    p_score = compute_panic_score(panic_subset)

    if not price_subset.empty:
        latest = price_subset["price"].iloc[-1]
        avg = price_subset["price"].mean()
        change = (latest - avg) / avg
    else:
        change = 0.1

    panic_index = int(p_score * 100)
    reality_score = int((1 - abs(change)) * 100)
    gap = abs(panic_index - reality_score)

    city_analysis.append({
        "City": c,
        "Panic": panic_index,
        "Reality": reality_score,
        "Gap": gap
    })

city_df = pd.DataFrame(city_analysis).sort_values(by="Panic", ascending=False)

st.dataframe(city_df, use_container_width=True)

st.subheader("📊 Visual Comparison")
st.bar_chart(city_df.set_index("City")[["Panic", "Reality"]])

st.subheader("🚨 Most Critical City")

top_city = city_df.iloc[0]

st.error(
    f"{top_city['City']} has highest panic ({top_city['Panic']}) "
    f"with gap of {top_city['Gap']} → Likely exaggerated situation"
)