import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# 제목
st.title("지명을 입력해서 지도에 마커 찍기")

# 사용자로부터 지명 입력
location_input = st.text_input("지명을 입력하세요 (예: 서울시청, 부산 해운대 등)")

# 지도 기본 위치
default_location = [37.5665, 126.9780]  # 서울 중심

# 지도 생성
m = folium.Map(location=default_location, zoom_start=12)

# 지명 입력 후 처리
if location_input:
    geolocator = Nominatim(user_agent="geo_app")
    location = geolocator.geocode(location_input)

    if location:
        # 위치 정보를 지도에 마커로 추가
        folium.Marker(
            location=[location.latitude, location.longitude],
            popup=location_input,
            tooltip="📍 " + location_input
        ).add_to(m)

        # 입력한 위치로 지도 중심 이동
        m.location = [location.latitude, location.longitude]
        m.zoom_start = 14
    else:
        st.error("지명을 찾을 수 없습니다. 정확한 지명을 입력해주세요.")

# 지도 출력
st_folium(m, width=700, height=500)
