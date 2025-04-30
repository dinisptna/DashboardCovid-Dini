import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    df = pd.read_csv('covid_19_indonesia_time_series_all.csv')
    df = df[df["Location"] != "Indonesia"] # Filter out Indonesia
    return df

def filter_data(df, year=None, location=None):
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    if location and "Semua Provinsi" not in location:
        df = df[df['Location'].isin(location)]  # Mendukung multi-location
    return df

def select_year():
    return st.sidebar.selectbox(
        "📆Pilih Tahun",
        options=[None, 2020, 2021, 2022, 2023],
        format_func=lambda x: "Semua Tahun" if x is None else x
    )

def select_location(df):
    locations = sorted(df['Location'].unique())
    return st.sidebar.multiselect(
        "📍Pilih Provinsi",
        options=["Semua Provinsi"] + locations,  # Tambahkan opsi "Semua Provinsi"
        default=["Semua Provinsi"],  # Default ke "Semua Provinsi"
        format_func=lambda x: x
    )

def show_data(df):
    selected_columns = ['Location'] + list (df.loc[:, 'New Cases':'New Recovered'].columns)
    df_selected = df[selected_columns]
    st.subheader('Data COVID-19🔴⚪')
    st.dataframe(df_selected.head(10))

    st.subheader('📈Statistik Deskriptif')
    st.write(df_selected.describe())
    st.write('Dini Septiana - 184230017')

def total_cases(df):
    total_cases= df.sort_values("Date").groupby("Location", as_index=False).last()
    return total_cases["Total Cases"].sum()

def total_deaths(df):
    total_deaths= df.sort_values("Date").groupby("Location", as_index=False).last()
    return total_deaths["Total Deaths"].sum()

def total_recovered(df):
    total_recovered= df.sort_values("Date").groupby("Location", as_index=False).last()
    return total_recovered["Total Recovered"].sum()

def kolom(df):
    kasus=total_cases(df)
    kematian=total_deaths(df)
    sembuh=total_recovered(df)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="🦠Total Kasus", value=f"{kasus:,.0f}".replace(",", "."))
    col2.metric(label="💀Total Kematian", value=f"{kematian:,.0f}".replace(",", "."))
    col3.metric(label="💚Total Sembuh", value=f"{sembuh:,.0f}".replace(",", "."))

def pie_chart1(df):
    total_mati = total_deaths(df)
    total_sembuh = total_recovered(df)

    data = {
        'Status' : ['Meninggal', 'Sembuh'],
        'Jumlah' : [total_mati, total_sembuh]
    }

    fig = px.pie(
        data,
        names='Status',
        values='Jumlah',
        title='📊Perbandingan Total Kematian vs Total Kesembuhan COVID-19',
        hole = 0.5,
        color_discrete_sequence= [ '#42f560', '#f54245']
    )

    st.plotly_chart(fig, use_container_width=True)    

def bar_chart1(df):
    df_last = df.sort_values("Date").groupby("Location", as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Deaths')

    fig = px.bar(
        top5,
        x='Location',
        y='Total Deaths',
        title='5 Provinsi dengan Total Kematian COVID-19 Tertinggi',
        color='Total Recovered',
        color_continuous_scale='reds',
        labels={'Total Cases': 'Total Kasus', 'Location': 'Provinsi', 'Total Deaths': 'Total Kematian'}
    )
    fig.update_layout(title_x=0.5)
    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kasus')
    st.plotly_chart(fig, use_container_width=True)

def bar_chart2(df):
    df_last = df.sort_values("Date").groupby("Location", as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Recovered')
    fig = px.bar(
        top5,
        x='Location',
        y='Total Recovered',
        title='📊5 Provinsi dengan Total Kesembuhan COVID-19 Tertinggi',
        color='Total Deaths',
        color_continuous_scale='greens',
        labels={'Total Recovered': 'Total Kesembuhan', 'Location': 'Provinsi'}
    )
    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kesembuhan', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def map_chart(df, year=None):
    df["Date"] = pd.to_datetime(df["Date"])
    if year:
        df = df[df["Date"].dt.year == year]
    
    df_agg = df.groupby(['Location', 'Latitude', 'Longitude'], as_index=False)['New Cases'].sum()
    df_map = df_agg.dropna(subset=['Latitude', 'Longitude','New Cases'])

    if df_map.empty:
        st.warning("Tidak ada data untuk tahun yang dipilih.")
        return
    fig = px.scatter_mapbox(
        df_map,
        lat='Latitude',
        lon='Longitude',
        hover_name='Location',
        size='New Cases',
        color='New Cases',
        zoom =3,
        size_max=20,
        center={"lat": -2.5, "lon": 118},
        opacity=0.7,
        title=f'📍Peta Sebaran Kasus COVID-19 di Indonesia Tahun ({year if year else 'Semua Tahun'})',
        color_continuous_scale= "OrRd",
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        height=600,
        margin={"r":0,"t":50,"l":0,"b":0},)
    st.plotly_chart(fig, use_container_width=True)