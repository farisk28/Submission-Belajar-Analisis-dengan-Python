# Menyiapkan dataframe
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


#1. create_byyear_df untuk menentukan hasil dari byyear_df
def create_byyear_df(df):
    byyear_df = df.groupby(by="yr").instant.nunique().reset_index()
    byyear_df["yr"] = byyear_df["yr"].replace({
    0: 2011,
    1: 2012,
})
    return byyear_df

# 2. Create_byseason_df untuk menentukan hasil dari byseason_df
def create_byseason_df(df):
    byseason_df = df.groupby(by="season").instant.nunique().reset_index()
    byseason_df["season"] = byseason_df["season"].replace({
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
})
    return byseason_df

# 3. Create_byweather_df untuk menentukan hasil dari byweather_df
def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit").instant.nunique().reset_index()
    byweather_df["weathersit"] = byweather_df["weathersit"].replace({
    1: "Clear",
    2: "Mist",
    3: "Light Snow",
    4: "Heavy Rain"
})
    return byweather_df

# 4. Buat Daily Orders
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "instant":"nunique",
        "cnt": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    return daily_orders_df

# Selanjutnya adalah kita perlu membuat load berkas csv
hour_day_df = pd.read_csv("TugasAkhir/Bike-sharing-dataset/hour_day_df.csv")

# Selanjutnya adah memastikan dteday merupakan type data datetime
datetime_columns = ["dteday"]
hour_day_df.sort_values(by="dteday", inplace=True)
hour_day_df.reset_index(inplace=True)

for column in datetime_columns:
    hour_day_df[column] = pd.to_datetime(hour_day_df[column])

# Membuat Komponen Filter
min_date = hour_day_df["dteday"].min()
max_date = hour_day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("TugasAkhir/Dashboard/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Data yang telah difilter akan disimpan dalam main_df.
main_df = hour_day_df[(hour_day_df["dteday"] >= str(start_date)) & 
                (hour_day_df["dteday"] <= str(end_date))]

# Selanjutnya kita akan memanggil helper function yang telah kita buat sebelumnya
byyear_df = create_byyear_df(main_df)
byweather_df = create_byweather_df(main_df)
byseason_df = create_byseason_df(main_df)
daily_orders_df = create_daily_orders_df (main_df)

# Selanjutnya, melengkapinya dengan visualisasi data

# Menambahkan Header
st.header("Dashboard Perentalan Sepeda")

# Menambah Informasi Terkait Daily Order
st.subheader('Catatan Pesanan')
col1 = st.columns(1)[0]
with col1:
    jumlah_pesanan = daily_orders_df.instant.sum()
    st.metric("Jumlah Pesanan", value=jumlah_pesanan)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["instant"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# Informasi berikutnya adalah informasi rental tahunan
st.subheader("Detail Transaksi")
 
col1, col2 = st.columns(2)
with col1:
    # Membuat pie chart
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Warna untuk pie chart
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    # Plot pie chart
    ax.pie(
        byyear_df['instant'], 
        labels=byyear_df['yr'], 
        colors=colors, 
        autopct='%1.1f%%', 
        startangle=140,
        textprops={'fontsize': 18}
    )

    # Mengatur judul
    ax.set_title("Jumlah Pesanan berdasarkan Tahun", loc="center", fontsize=20)

    # Menampilkan pie chart di Streamlit
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="instant", 
        x="season",
        data=byseason_df.sort_values(by="season", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Jumlah Pesanan berdasarkan Musim", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="instant", 
    y="weathersit",
    data=byweather_df.sort_values(by="instant", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Jumlah Pesanan berdasarkan Cuaca", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.caption("Muhammad Faris Kurniawan")