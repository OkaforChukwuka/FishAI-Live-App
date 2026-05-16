import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="FishAI Live System",
    layout="wide"
)

# -----------------------------
# CUSTOM HEADER
# -----------------------------
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1 {
    color: white;
    font-size: 42px !important;
}

.metric-card {
    background-color: #161B22;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #30363D;
}

.insight-box {
    background-color: #161B22;
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #ff7f50;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
# 🐟 FishAI Live Smart Selling System

### AI-powered fish price prediction and smart selling recommendation platform
""")

# -----------------------------
# CREATE SAMPLE DATASET
# -----------------------------
np.random.seed(42)

locations = ['Lagos', 'Abuja', 'Warri', 'Port Harcourt']
fish_types = ['Catfish', 'Tilapia']
demand_levels = ['Low', 'Medium', 'High']
supply_levels = ['Low', 'Medium', 'High']

rows = []

for i in range(300):

    location = np.random.choice(locations)
    fish = np.random.choice(fish_types)
    demand = np.random.choice(demand_levels)
    supply = np.random.choice(supply_levels)

    quantity = np.random.randint(50, 150)

    competitor_price = np.random.randint(1300, 1700)

    base_price = 1400

    if demand == "High":
        base_price += 120
    elif demand == "Medium":
        base_price += 50

    if supply == "Low":
        base_price += 100

    if fish == "Tilapia":
        base_price += 80

    price = base_price + np.random.randint(-50, 50)

    rows.append([
        location,
        fish,
        demand,
        supply,
        quantity,
        competitor_price,
        price
    ])

df = pd.DataFrame(rows, columns=[
    'Location',
    'Fish_Type',
    'Demand_Level',
    'Supply_Level',
    'Quantity_Sold',
    'Competitor_Price',
    'Price_per_KG'
])

# -----------------------------
# ENCODING
# -----------------------------
mapping = {
    'Location': {'Abuja':0, 'Lagos':1, 'Port Harcourt':2, 'Warri':3},
    'Fish_Type': {'Catfish':0, 'Tilapia':1},
    'Demand_Level': {'Low':0, 'Medium':1, 'High':2},
    'Supply_Level': {'Low':0, 'Medium':1, 'High':2}
}

encoded_df = df.copy()

for col in mapping:
    encoded_df[col] = encoded_df[col].map(mapping[col])

# -----------------------------
# TRAIN MODEL
# -----------------------------
X = encoded_df.drop(columns=['Price_per_KG'])
y = encoded_df['Price_per_KG']

model = RandomForestRegressor()
model.fit(X, y)

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("Enter Market Conditions")

location = st.sidebar.selectbox(
    "Location",
    locations
)

fish_type = st.sidebar.selectbox(
    "Fish Type",
    fish_types
)

demand = st.sidebar.selectbox(
    "Demand Level",
    demand_levels
)

supply = st.sidebar.selectbox(
    "Supply Level",
    supply_levels
)

quantity = st.sidebar.slider(
    "Quantity Sold",
    50,
    150,
    100
)

competitor_price = st.sidebar.slider(
    "Competitor Price",
    1300,
    1700,
    1500
)

# -----------------------------
# PREDICTION
# -----------------------------
input_data = pd.DataFrame([[
    mapping['Location'][location],
    mapping['Fish_Type'][fish_type],
    mapping['Demand_Level'][demand],
    mapping['Supply_Level'][supply],
    quantity,
    competitor_price
]], columns=X.columns)

predicted_price = model.predict(input_data)[0]

# -----------------------------
# RECOMMENDATION
# -----------------------------
if predicted_price > 1550 and demand == "High":
    recommendation = "✅ SELL NOW"

elif predicted_price < 1450:
    recommendation = "⏳ WAIT"

else:
    recommendation = "👀 MONITOR"

# -----------------------------
# KPI CARDS
# -----------------------------

total_revenue = df['Price_per_KG'].sum()
avg_price = df['Price_per_KG'].mean()
filtered_df = df[
    (df['Fish_Type'] == fish_type)
]

best_market = filtered_df.groupby('Location')['Price_per_KG'].mean().idxmax()

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
<div class="metric-card">
<h3>Total Revenue</h3>
<h1>₦{int(total_revenue):,}</h1>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="metric-card">
<h3>Predicted Price</h3>
<h1>₦{int(predicted_price)}</h1>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="metric-card">
<h3>Recommendation</h3>
<h1>{recommendation}</h1>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="metric-card">
<h3>Best Market</h3>
<h1>{best_market}</h1>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# AI INSIGHTS
# -----------------------------

if demand == "High" and supply == "Low":
    insight = "🔥 High demand and low supply are pushing fish prices upward."

elif demand == "Low":
    insight = "📉 Low market demand may reduce selling opportunities."

else:
    insight = "📊 Market conditions are currently stable."

st.markdown(f"""
<div class="insight-box">
<h3>AI Market Insight</h3>
<p>{insight}</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# CHARTS
# -----------------------------
chart1 = px.bar(
    df,
    x='Location',
    y='Price_per_KG',
    color='Fish_Type',
    title='🐟 Fish Prices by Location',
    color_discrete_sequence=['#008080', '#ff7f50']
)

chart1.update_layout(
    template='plotly_dark',
    paper_bgcolor='#0E1117',
    plot_bgcolor='#0E1117'
)

st.plotly_chart(chart1, use_container_width=True)

chart2 = px.scatter(
    df,
    x='Quantity_Sold',
    y='Price_per_KG',
    color='Demand_Level',
    title='📈 Demand vs Price',
    color_discrete_sequence=['#ff7f50', '#008080', '#5DADE2']
)

chart2.update_layout(
    template='plotly_dark',
    paper_bgcolor='#0E1117',
    plot_bgcolor='#0E1117'
)

st.plotly_chart(chart2, use_container_width=True)

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.subheader("Dataset Preview")

st.dataframe(df.head(20))
