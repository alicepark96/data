import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🌡️ 기온 데이터 시각화")

# CSV 파일 경로
csv_file = "temp.csv"

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(csv_file, encoding="cp949")  # 인코딩 중요!
    df.columns = df.columns.str.strip()  # 공백 제거
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df = df.dropna(subset=["날짜"])
    return df

df = load_data()

# 날짜 범위 선택
st.sidebar.header("📅 기간 선택")
min_date = df["날짜"].min().date()
max_date = df["날짜"].max().date()
selected_dates = st.sidebar.date_input("날짜 범위", [min_date, max_date])

# 기온 항목 선택
temperature_col = st.sidebar.selectbox(
    "기온 항목 선택",
    options=["평균기온(°C)", "최저기온(°C)", "최고기온(°C)"]
)

# 필터링
if len(selected_dates) == 2:
    start, end = selected_dates
    filtered_df = df[(df["날짜"].dt.date >= start) & (df["날짜"].dt.date <= end)]
else:
    filtered_df = df

# 유효성 체크
if temperature_col not in filtered_df.columns:
    st.error(f"선택한 항목 '{temperature_col}'이 데이터에 없습니다.")
    st.write("사용 가능한 열 목록:", list(filtered_df.columns))
else:
    # 시각화
    st.subheader(f"📈 {temperature_col} 변화 추이")
    fig = px.line(
        filtered_df,
        x="날짜",
        y=temperature_col,
        title=f"{temperature_col} 추이",
        markers=True,
        labels={"날짜": "날짜", temperature_col: "기온 (°C)"}
    )
    st.plotly_chart(fig, use_container_width=True)

    # 통계 요약
    st.subheader("📊 통계 요약")
    st.write(f"✅ 평균: {filtered_df[temperature_col].mean():.2f} °C")
    st.write(f"📈 최고: {filtered_df[temperature_col].max():.2f} °C")
    st.write(f"📉 최저: {filtered_df[temperature_col].min():.2f} °C")
