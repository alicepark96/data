import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📈 기온 데이터 시각화")

# CSV 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("ta_20250712105856.csv", encoding="cp949")
    df.columns = df.columns.str.strip()  # 공백 제거
    df["날짜"] = pd.to_datetime(df["날짜"])  # ✔ 수정된 열 이름
    return df

df = load_data()

# 날짜 범위 선택
st.sidebar.header("🔍 기간 선택")
min_date = df["날짜"].min()
max_date = df["날짜"].max()
start_date, end_date = st.sidebar.date_input("날짜 범위", [min_date, max_date])

# 필터링
filtered = df[
    (df["날짜"] >= pd.to_datetime(start_date)) &
    (df["날짜"] <= pd.to_datetime(end_date))
]

# 선택할 기온 유형
temperature_type = st.sidebar.selectbox("기온_
