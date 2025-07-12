import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📈 기온 데이터 시각화")

# CSV 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("ta_20250712105856.csv", encoding="cp949")  # 필요시 cp949로 변경
    df["일시"] = pd.to_datetime(df["일시"])
    return df

df = load_data()

# 날짜 범위 선택
st.sidebar.header("🔍 기간 선택")
min_date = df["일시"].min()
max_date = df["일시"].max()
start_date, end_date = st.sidebar.date_input("날짜 범위", [min_date, max_date])

# 지역 선택
regions = df["지점명"].unique()
selected_region = st.sidebar.selectbox("지역 선택", regions)

# 필터링
filtered = df[
    (df["일시"] >= pd.to_datetime(start_date)) &
    (df["일시"] <= pd.to_datetime(end_date)) &
    (df["지점명"] == selected_region)
]

# 라인 차트 출력
st.subheader(f"🌡️ {selected_region} 기온 변화 추이")
fig = px.line(filtered, x="일시", y="기온(°C)", title="기온 추이", markers=True)
st.plotly_chart(fig, use_container_width=True)
