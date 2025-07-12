import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(layout="wide")
st.title("📈 기온 데이터 시각화")

# ✅ 데이터 불러오기 함수
@st.cache_data
def load_data():
    df = pd.read_csv("ta_20250712105856.csv", encoding="cp949")
    df.columns = df.columns.str.strip().str.replace("\u200b", "", regex=False)  # 제로폭공백 제거
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df = df.dropna(subset=["날짜"])
    return df

df = load_data()

# ✅ 사용자-friendly 이름 ↔ 실제 컬럼 이름 매핑
column_map = {
    "평균기온": "평균기온 (°C)",
    "최저기온": "최저기온 (°C)",
    "최고기온": "최고기온 (°C)"
}

# ✅ 사이드바 UI
st.sidebar.header("📅 기간 선택")
min_date = df["날짜"].min()
max_date = df["날짜"].max()
start_date, end_date = st.sidebar.date_input("날짜 범위", [min_date, max_date])

st.sidebar.header("🌡️ 기온 항목 선택")
selected_label = st.sidebar.selectbox("기온 항목 선택", list(column_map.keys()))
temperature_type = column_map[selected_label]

# ✅ 날짜로 필터링
filtered = df[
    (df["날짜"] >= pd.to_datetime(start_date)) &
    (df["날짜"] <= pd.to_datetime(end_date))
]

# ✅ 유효성 검사 + 시각화
if filtered.empty:
    st.warning("⚠️ 선택한 날짜 범위에 해당하는 데이터가 없습니다.")
elif temperature_type not in filtered.columns:
    st.error(f"❌ 선택한 항목 '{temperature_type}'이 데이터에 없습니다.")
    st.write("사용 가능한 열 목록:", filtered.columns.tolist())
else:
    st.subheader(f"📊 {selected_label} 변화 추이")
    fig = px.line(filtered, x="날짜", y=temperature_type, title=f"{selected_label} 추이", markers=True)
    st.plotly_chart(fig, use_container_width=True)
