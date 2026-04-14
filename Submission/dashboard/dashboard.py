import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")

# Path ke main_data.csv (ada di dalam folder Submission/dashboard/)
file_path = "Submission/dashboard/main_data.csv"

# Cek apakah file ada
if os.path.exists(file_path):
    st.success(f"✅ File ditemukan di: {file_path}")
    df = pd.read_csv(file_path)
    st.write(df.head())
else:
    st.error(f"❌ File tidak ditemukan di: {file_path}")
    st.write("📁 Mencoba mencari di semua folder...")
    
    # Cari file main_data.csv di semua folder
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "main_data.csv":
                st.success(f"✅ Ditemukan di: {os.path.join(root, file)}")
                df = pd.read_csv(os.path.join(root, file))
                st.write(df.head())
                break
