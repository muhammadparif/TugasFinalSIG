import streamlit as st
import pandas as pd
import pydeck as pdk

# Fungsi untuk memuat data

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Membaca data dari file CSV
data = load_data('data.csv')

# Sidebar untuk kontrol tampilan peta
st.sidebar.header("Pengaturan Peta")
map_style = st.sidebar.selectbox(
    "Pilih Gaya Peta", 
    ["mapbox://styles/mapbox/light-v9", "mapbox://styles/mapbox/dark-v9", "mapbox://styles/mapbox/streets-v11", "mapbox://styles/mapbox/satellite-v9"]
)

# Judul aplikasi
st.title('Peta Geografis Kecamatan Banggae Timur')


# Menampilkan data dalam tabel
st.write("Data yang digunakan:")
st.dataframe(data)

# Menentukan tampilan peta
view_state = pdk.ViewState(
    latitude=data['latitude'].mean(),
    longitude=data['longitude'].mean(),
    zoom=10,
    pitch=50,
)

# Membuat lapisan HexagonLayer
hex_layer = pdk.Layer(
    'HexagonLayer',
    data=data,
    get_position='[longitude, latitude]',
    radius=200,
    elevation_scale=4,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
    get_fill_color='[255, 165, 0, 160]'
)

# Membuat lapisan ScatterplotLayer
scatter_layer = pdk.Layer(
    'ScatterplotLayer',
    data=data,
    get_position='[longitude, latitude]',
    get_color='[30, 144, 255, 160]',
    get_radius=200,
    pickable=True  # Pastikan lapisan ini bisa dipilih untuk tooltip
)

# Membuat tampilan peta
r = pdk.Deck(
    layers=[hex_layer, scatter_layer],
    initial_view_state=view_state,
    map_style=map_style,
    tooltip={"text": "Kelurahan: {kelurahan}\nLatitude: {latitude}\nLongitude: {longitude}"}
)

# Menampilkan peta
st.pydeck_chart(r)

# CSS kustom untuk mempercantik tampilan
st.markdown(
    """
    <style>
    .stTitle { color: darkblue; }
    .stHeader { color: darkblue; }
    .stMarkdown { color: #4CAF50; }
    </style>
    """,
    unsafe_allow_html=True
)