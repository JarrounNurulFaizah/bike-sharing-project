import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Data Cleaning
day_df.dropna(inplace=True)
hour_df.dropna(inplace=True)

# Konversi kolom date
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Mapping season dan weather
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_map = {1: 'Clear', 2: 'Cloudy', 3: 'Light Rain', 4: 'Heavy Rain'}

day_df['season'] = day_df['season'].map(season_map)
day_df['weathersit'] = day_df['weathersit'].map(weather_map)

hour_df['season'] = hour_df['season'].map(season_map)
hour_df['weathersit'] = hour_df['weathersit'].map(weather_map)

# Streamlit UI
st.title("Dashboard Penyewaan Sepeda")

# Sidebar Filters
date_start = st.sidebar.date_input("Pilih Tanggal Mulai", day_df['dteday'].min().date())
date_end = st.sidebar.date_input("Pilih Tanggal Akhir", day_df['dteday'].max().date())
season_filter = st.sidebar.multiselect("Pilih Musim", day_df['season'].unique(), default=day_df['season'].unique())
weather_filter = st.sidebar.multiselect("Pilih Cuaca", day_df['weathersit'].unique(), default=day_df['weathersit'].unique())

# Filter data
day_filtered = day_df[(day_df['dteday'] >= pd.to_datetime(date_start)) & (day_df['dteday'] <= pd.to_datetime(date_end))]
day_filtered = day_filtered[day_filtered['season'].isin(season_filter) & day_filtered['weathersit'].isin(weather_filter)]

# Rata-rata penyewaan
st.subheader("📊 Rata-rata Penyewaan Sepeda")
st.metric(label="Rata-rata Penyewaan", value=round(day_filtered['cnt'].mean(), 2))
st.metric(label="Total Penyewaan", value=int(day_filtered['cnt'].sum()))

# Grafik Penyewaan Sepeda Berdasarkan Musim
st.subheader("🚴 Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots()
sns.barplot(data=day_filtered, x='season', y='cnt', estimator=sum, ci=None, ax=ax)
ax.set_ylabel("Jumlah Penyewaan")
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')
st.pyplot(fig)

# Grafik Penyewaan Berdasarkan Cuaca
st.subheader("🌦 Penyewaan Sepeda Berdasarkan Cuaca")
fig, ax = plt.subplots()
sns.boxplot(data=day_filtered, x='weathersit', y='cnt', ax=ax)
st.pyplot(fig)

# Peminjaman Terbanyak dan Tersedikit 
st.subheader("⏰ Peminjaman Sepeda Terbanyak dan Tersedikit")
hour_filtered = hour_df[(hour_df['dteday'] >= pd.to_datetime(date_start)) & (hour_df['dteday'] <= pd.to_datetime(date_end))]

# Menentukan 5 jam dengan peminjaman terbanyak dan tersedikit
top_hours = hour_filtered.groupby('hr')['cnt'].sum().nlargest(5)
least_hours = hour_filtered.groupby('hr')['cnt'].sum().nsmallest(5)

# Grafik Peminjaman Terbanyak
fig, ax = plt.subplots()
top_hours.plot(kind='bar', color='green', ax=ax)
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Peminjaman Sepeda Terbanyak")
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')
st.pyplot(fig)

# Grafik Peminjaman Tersedikit
fig, ax = plt.subplots()
least_hours.plot(kind='bar', color='red', ax=ax)
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Peminjaman Sepeda Tersedikit")
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')
st.pyplot(fig)

# Grafik Tren Penyewaan Sepeda Harian
st.subheader("📈 Tren Penyewaan Sepeda Per Hari")
fig, ax = plt.subplots()
day_filtered.plot(x='dteday', y='cnt', kind='line', marker='o', ax=ax)
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Tampilkan Data Penyewaan Sepeda
st.subheader("📋 Data Penyewaan Sepeda")
st.dataframe(day_filtered)
