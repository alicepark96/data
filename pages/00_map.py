import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("지도 클릭으로 위치 마커 찍기")

# 지도 초기 위치 설정 (서울 중심)
map_center = [37.5665, 126.9780]
m = folium.Map(location=map_center, zoom_start=12)

# 클릭 이벤트 반영 (streamlit-folium이 자동 제공)
map_data = st_folium(m, width=700, height=500)

# 클릭한 위치 정보를 받아 마커 추가
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    
    # 마커 다시 찍기 위한 새 지도
    m = folium.Map(location=[lat, lon], zoom_start=14)
    folium.Marker([lat, lon], tooltip="📍 선택한 위치").add_to(m)
    
    # 다시 그린 지도 출력
    st_folium(m, width=700, height=500)
    
    # 클릭한 좌표 출력
    st.success(f"선택한 위치: 위도 {lat:.6f}, 경도 {lon:.6f}")
else:
    st.info("지도를 클릭하여 위치를 선택하세요.")
