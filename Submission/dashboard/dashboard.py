import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")

# Cek file dengan os.listdir()
st.write("📁 File yang ada di folder ini:")
files = os.listdir(".")
st.write(files)

# Coba baca file
try:
    df = pd.read_csv("main_data.csv")
    st.success("✅ main_data.csv berhasil dibaca!")
    st.write(df.head())
except Exception as e:
    st.error(f"❌ Gagal membaca main_data.csv: {e}")
