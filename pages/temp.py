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
    df.columns = df.columns.str.strip().str.replace("\u200b", "")  # 공백 및 제로폭공백 제거
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")       # 날짜 변환 (실패 시 NaT 처리)
    df = df.dropna(subset=["날짜"])                                 # 날짜 없는 행 제거
    return df

df = load_data()

# ✅ 사이드바: 날짜 범위 선택
st.sidebar.header("📅 기간 선택")
min_date = df["날짜"].min()
max_date = df["날짜"].max()
start_date, end_date = st.sidebar.date_input("날짜 범위", [min_date, max_date])

# ✅ 사이드바: 기온 항목 선택
temperature_options = ["평균기온(°C)", "최저기온(°C)", "최고기온(°C)"]
temperature_type = st.sidebar.selectbox("🌡️ 기온 항목 선택", temperature_options)

# ✅ 날짜 필터링
filtered = df[
    (df["날짜"] >= pd.to_datetime(start_date)) &
    (df["날짜"] <= pd.to_datetime(end_date))
]

# ✅ 디버깅 출력 (원할 경우 주석 해제)
# st.write("✅ 선택된 날짜:", start_date, "~", end_date)
# st.write("✅ 필터링된 데이터 수:", len(filtered))
# st.write("✅ 사용 가능한 컬럼:", filtered.columns.tolist())
# st.write("✅ 선택한 항목:", temperature_type)

# ✅ 조건 확인 후 시각화
if filtered.empty:
    st.warning("⚠️ 선택한 날짜 범위에 해당하는 데이터가 없습니다.")
elif temperature_type not in filtered.columns:
    st.error(f"❌ 선택한 항목 '{temperature_type}'이 데이터에 없습니다.")
    st.write("사용 가능한 열 목록:", filtered.columns.tolist())
else:
    st.subheader(f"🔧 {temperature_type} 변화 추이")
    fig = px.line(filtered, x="날짜", y=temperature_type, title="기온 추이", markers=True)
    st.plotly_chart(fig, use_container_width=True)
