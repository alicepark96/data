import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("클릭으로 마커 찍기")

# 세션 상태에 클릭 좌표 저장
if "clicked_location" not in st.session_state:
    st.session_state["clicked_location"] = None

# 지도 기본 설정
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 이전 클릭 위치가 있으면 마커 추가
if st.session_state["clicked_location"]:
    lat, lon = st.session_state["clicked_location"]
    folium.Marker([lat, lon], tooltip="📍 선택한 위치").add_to(m)
    m.location = [lat, lon]
    m.zoom_start = 14

# Folium 지도 보여주기 + 클릭 감지
map_data = st_folium(m, width=700, height=500)

# 클릭 이벤트 발생하면 세션 상태에 저장
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    st.session_state["clicked_location"] = (lat, lon)
    st.rerun()  # 지도를 다시 그리기 위해 rerun 실행

# 좌표 출력
if st.session_state["clicked_location"]:
    st.success(f"📌 선택한 위치: 위도 {lat:.6f}, 경도 {lon:.6f}")
