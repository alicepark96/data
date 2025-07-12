import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

st.set_page_config(layout="wide")
st.title("두 지점 클릭해서 직선거리 측정하기")

# 클릭된 좌표 리스트를 세션에 저장
if "points" not in st.session_state:
    st.session_state.points = []

# Folium 지도 기본 설정
map_center = [37.5665, 126.9780]  # 서울 기준
m = folium.Map(location=map_center, zoom_start=12)

# 이미 클릭한 점이 있다면 지도에 마커로 표시
for point in st.session_state.points:
    folium.Marker(point, tooltip="📍 클릭 위치").add_to(m)

# 두 지점이면 선도 그리기
if len(st.session_state.points) == 2:
    folium.PolyLine(st.session_state.points, color="blue", weight=3).add_to(m)

    # 거리 계산
    dist = geodesic(st.session_state.points[0], st.session_state.points[1]).km
    st.success(f"📏 두 지점 사이 직선 거리: **{dist:.2f} km**")

# 지도 표시 및 클릭 이벤트 수신
map_data = st_folium(m, width=700, height=500)

# 새로운 클릭이 들어오면 포인트 추가
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    if len(st.session_state.points) < 2:
        st.session_state.points.append((lat, lon))
        st.rerun()
    else:
        st.warning("두 지점까지만 선택할 수 있어요. 초기화하려면 아래 버튼을 누르세요.")

# 초기화 버튼
if st.button("🔄 초기화"):
    st.session_state.points = []
    st.rerun()
