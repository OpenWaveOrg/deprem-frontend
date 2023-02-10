import os
import requests
import streamlit as st

import folium
import streamlit_folium as st_folium

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

api_endpoint = os.getenv("API_ENDPOINT")


def sidebar():
    # Displaying sidebar
    st.sidebar.title("Deprem Project")
    st.sidebar.markdown(
        """
    Deprem bölgesinin verilerini görselleştirmeyi amaçlayan bir projedir.
    """
    )

    sidebar_options = requests.get(f"{api_endpoint}/select_options").json()
    with st.sidebar.form("user-form"):
        current_user_input = {}
        final_user_input = {}
        coordinates_data = {}

        for i in sidebar_options:
            current_sidebar_values = sidebar_options[i]
            if "" not in current_sidebar_values:
                current_sidebar_values.insert(0, "")

            if "_" in i:
                j = i.replace("_", " ").replace("konum","").capitalize()
            else:
                j = i.capitalize()

            current_user_input[i] = st.selectbox(
                j, current_sidebar_values, index=current_sidebar_values.index("")
            )

        submitted = st.form_submit_button("Ara")
        if submitted:
            # Remove the "" values from the user input
            for z in current_user_input:
                if current_user_input[z] != "":
                    final_user_input[z] = current_user_input[z]

            st.success("Your options are displayed on the map 📍")

            coordinates_data = requests.get(
                f"{api_endpoint}/get_user_parameters", json=final_user_input
            ).json()

    draw_map(coordinates_data)


def draw_map(coordinates_data: dict):
    if coordinates_data:
        m = folium.Map(location=[37.7981263, 36.1829598], zoom_start=6)
        with st.expander("Show Data"):
            for x in coordinates_data:
                try:
                    if (
                            x["lat"]
                            and x["lon"]
                            and x["lat"] != ""
                            and x["lon"] != ""
                    ):
                        if x['lat'] and x['lon'] and x['lat'] != '' and x['lon'] != '':
                            location = f"http://maps.google.com/?ll={x['lat']},{x['lon']}"
                        else:
                            location = "Konum Bilgisi Yok"
                        folium.Marker(
                            location=[x["lat"], x["lon"]],
                            popup=f"""
                        <table>
                        <tr>
                        <td>İl</td>
                        <td>{x['konum_il']}</td>
                        </tr>
                        <tr>
                        <td>İlçe</td>
                        <td>{x['konum_ilce']}</td>
                        </tr>
                        <tr>
                        <td>Mahalle</td>
                        <td>{x['konum_mahalle']}</td>
                        </tr>
                        <tr>
                        <td>İsim Soyisim</td>
                        <td>{x['isimsoyisim']}</td>
                        </tr>
                        <tr>
                        <td>Kişi Sayısı</td>
                        <td>{x['kisi_sayisi']}</td>
                        </tr>
                        <tr>
                        <td>Telefon Numrası</td>
                        <td>{x['telefon']}</td>
                        </tr>
                        <tr>
                        <td>Adres</td>
                        <td>{x['adres']}</td>
                        </tr>
                        <tr>
                        <td>Apartman</td>
                        <td>{x['apartman']}</td>
                        </tr>
                        <tr>
                        <td>Sokak</td>
                        <td>{x['sokak']}</td>
                        </tr>
                        <tr>
                        <td>Blok</td>
                        <td>{x['blok_no']}</td>
                        </tr>
                        <tr>
                        <td>Kat</td>
                        <td>{x['kat']}</td>
                        </tr>
                        <tr>
                        <td>Google Maps Linki</td>
                        <td>{location}</td>
                        </tr>
                        </table>
                        """,
                            tooltip=f"{x['konum_ilce']}",
                        ).add_to(m)

                        
                except KeyError:
                    pass
        

        st_folium.folium_static(m, width=1400, height=600)



st.set_page_config(layout="wide")
sidebar()
