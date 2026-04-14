# DASHBOARD BIKE SHARING
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Setting style
sns.set(style='dark')

# LOAD DATA
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# Pisahkan data hourly dan daily
hour_df = df[df['data_type'] == 'hourly'].copy()
day_df = df[df['data_type'] == 'daily'].copy()

# SIDEBAR FILTER
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.title("Bike Sharing")
    st.markdown("---")
    
    # Date filter
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    st.markdown("---")
    st.caption("Data: Capital Bikeshare (2011-2012)")

# Filter data
filtered_day = day_df[
    (day_df["dteday"] >= pd.Timestamp(start_date)) &
    (day_df["dteday"] <= pd.Timestamp(end_date))
]

filtered_hour = hour_df[
    (hour_df["dteday"] >= pd.Timestamp(start_date)) &
    (hour_df["dteday"] <= pd.Timestamp(end_date))
]

# HEADER
st.title("Bike Sharing Dashboard")
st.markdown(f"**Data periode:** {start_date} sampai {end_date}")
st.markdown("---")

# METRICS (4 kotak)
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_rental = filtered_day['cnt'].sum()
    st.metric("Total Penyewaan", value=f"{total_rental:,}")

with col2:
    avg_daily = filtered_day['cnt'].mean()
    st.metric("Rata-rata per Hari", value=f"{avg_daily:,.0f}")

with col3:
    total_casual = filtered_hour['casual'].sum()
    st.metric("Pengguna Casual", value=f"{total_casual:,}")

with col4:
    total_registered = filtered_hour['registered'].sum()
    st.metric("Pengguna Registered", value=f"{total_registered:,}")

st.markdown("---")

# CHART 1: TREN HARIAN
st.subheader("Tren Penyewaan Harian")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(filtered_day["dteday"], filtered_day["cnt"], 
        marker='o', linewidth=2, color="#2E86AB", markersize=3)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.tick_params(axis='x', rotation=45)
ax.grid(True, linestyle='--', alpha=0.3)
st.pyplot(fig)

st.markdown("---")

# CHART 2: POLA PER JAM (Casual vs Registered)
st.subheader("Pola Penyewaan per Jam")

hourly_pattern = filtered_hour.groupby(by="hr", observed=True).agg({
    "cnt": "mean",
    "casual": "mean",
    "registered": "mean"
}).reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(hourly_pattern["hr"], hourly_pattern["registered"], 
        marker='o', linewidth=2, label="Registered", color="#2E86AB")
ax.plot(hourly_pattern["hr"], hourly_pattern["casual"], 
        marker='s', linewidth=2, label="Casual", color="#A63D40")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Jumlah Penyewa")
ax.legend()
ax.grid(True, linestyle='--', alpha=0.3)
st.pyplot(fig)

st.markdown("---")

# CHART 3: PENGARUH CUACA
st.subheader("Pengaruh Cuaca terhadap Penyewaan")

weather_map = {1: 'Cerah', 2: 'Kabut', 3: 'Hujan Ringan', 4: 'Hujan Deras'}
filtered_hour['weather_label'] = filtered_hour['weathersit'].map(weather_map)

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=filtered_hour, x='weather_label', y='cnt', ax=ax, palette='Set2')
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Penyewaan")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

st.markdown("---")

# CHART 4: 5 JAM TERSIBUK
st.subheader("5 Jam dengan Penyewaan Tertinggi")

top_hours = filtered_hour.groupby(by="hr", observed=True).agg({
    "cnt": "mean"
}).round(2).sort_values(by="cnt", ascending=False).head(5).reset_index()
top_hours.columns = ['Jam', 'Rata-rata Penyewaan']

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(top_hours['Jam'].astype(str), top_hours['Rata-rata Penyewaan'], 
               color="#2E86AB")
ax.set_xlabel("Rata-rata Jumlah Penyewa")
ax.invert_yaxis()

for bar in bars:
    width = bar.get_width()
    ax.annotate(f'{width:.0f}', xy=(width, bar.get_y() + bar.get_height()/2),
                xytext=(5, 0), textcoords="offset points", ha='left', va='center')
st.pyplot(fig)

st.markdown("---")

# CHART 5: WEEKDAY vs WEEKEND
st.subheader("Weekday vs Weekend")

filtered_hour['day_type'] = filtered_hour['weekday'].apply(
    lambda x: 'Weekend' if x in [0,6] else 'Weekday'
)
day_type_pattern = filtered_hour.groupby(by="day_type", observed=True).agg({
    "cnt": "mean"
}).round(2).reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#2E86AB", "#F18F01"]
bars = ax.bar(day_type_pattern["day_type"], day_type_pattern["cnt"], color=colors)
ax.set_xlabel("Tipe Hari")
ax.set_ylabel("Rata-rata Jumlah Penyewa")

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.0f}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
st.pyplot(fig)

st.markdown("---")

# CHART 6: PERBANDINGAN 2011 vs 2012
st.subheader("Perbandingan 2011 vs 2012")

filtered_hour['year'] = filtered_hour['yr'].map({0: '2011', 1: '2012'})
year_comparison = filtered_hour.groupby(by="year", observed=True).agg({
    "cnt": "mean"
}).round(2).reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#A63D40", "#2E86AB"]
bars = ax.bar(year_comparison["year"], year_comparison["cnt"], color=colors)
ax.set_xlabel("Tahun")
ax.set_ylabel("Rata-rata Penyewaan per Jam")

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.0f}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
st.pyplot(fig)

st.markdown("---")

# FOOTER
st.caption(f"Copyright © 2024 | Bike Sharing Dashboard | Data {start_date} - {end_date}")