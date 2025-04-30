import streamlit as st
from data import *

def judul():
    st.title('😷Dashboard COVID-19')
    st.write('👋Selamat datang di dashboard interaktif untuk menganalisis data COVID-19 di Indonesia')
    st.write('Dini Septiana - 184230017')

st.sidebar.title('📊Navigasi')
menu = st.sidebar.radio('Pilih Halaman', ['Home', 'Halaman Data'])

if menu == 'Home':
    judul()

    df = load_data()
    year = select_year()
    location = select_location(df)  # Mendukung multi-location
    df_filtered = filter_data(df, year, location)
    kolom(df_filtered)
    pie_chart1(df_filtered)
    bar_chart1(df_filtered)
    bar_chart2(df_filtered)
    map_chart(df_filtered)
elif menu == 'Halaman Data':
    judul()
    year = select_year()
    df = load_data()
    location = select_location(df)
    df_filtered = filter_data(df, year, location)
    show_data(df_filtered)




