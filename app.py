import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="수질-건강 영향 분석", layout="wide")

st.title("💧 수질오염 → 건강 영향 시뮬레이터")
st.markdown("수질 지표 변화에 따른 질환 발생 위험을 정량적으로 시각화합니다.")

# --------------------------
# 기준값 (보고서 기반 평균값)
# --------------------------
BASELINE = {
    "bod": 4.0,            # mg/L
    "metal": 2.2,          # μg/L (Pb 기준 대표값)
    "chl": 50.0,           # μg/L
    "gastro": 66.5,        # 회/월
    "endocrine": 35.6,     # 회/월
    "skin": 110.5          # 회/월
}

# --------------------------
# 사이드바
# --------------------------
st.sidebar.header("📊 수질 지표 입력")

bod = st.sidebar.slider("BOD (mg/L)", 0.0, 10.0, BASELINE["bod"])
metal = st.sidebar.slider("중금속 (μg/L)", 0.0, 5.0, BASELINE["metal"])
chl = st.sidebar.slider("클로로필-a (μg/L)", 0.0, 100.0, BASELINE["chl"])

st.sidebar.markdown("---")

scenario = st.sidebar.selectbox(
    "🏛️ 정책 시나리오",
    ["없음", "BOD 20% 감소", "중금속 30% 감소", "통합 개선"]
)

# --------------------------
# 예측 모델 (보고서 기반 비례식)
# --------------------------
def predict():
    gastro = BASELINE["gastro"] * (bod / BASELINE["bod"])
    endocrine = BASELINE["endocrine"] * (metal / BASELINE["metal"])
    skin = BASELINE["skin"] * (chl / BASELINE["chl"])
    return gastro, endocrine, skin

gastro, endocrine, skin = predict()

# --------------------------
# 정책 적용
# --------------------------
gastro_after, endocrine_after, skin_after = gastro, endocrine, skin

if scenario == "BOD 20% 감소":
    gastro_after *= 0.85
elif scenario == "중금속 30% 감소":
    endocrine_after *= 0.85
elif scenario == "통합 개선":
    gastro_after *= 0.85
    endocrine_after *= 0.88
    skin_after *= 0.9

# --------------------------
# KPI 출력
# --------------------------
st.subheader("📌 질환 발생 (월간 의료기관 방문 횟수)")

col1, col2, col3 = st.columns(3)

col1.metric(
    "소화기 질환 (회/월)",
    f"{gastro_after:.1f}",
    f"{gastro_after - gastro:.1f}"
)

col2.metric(
    "내분비 질환 (회/월)",
    f"{endocrine_after:.1f}",
    f"{endocrine_after - endocrine:.1f}"
)

col3.metric(
    "피부 질환 (회/월)",
    f"{skin_after:.1f}",
    f"{skin_after - skin:.1f}"
)

# --------------------------
# 비교 데이터프레임
# --------------------------
df = pd.DataFrame({
    "질환": ["소화기", "내분비", "피부"],
    "기존": [gastro, endocrine, skin],
    "정책 적용 후": [gastro_after, endocrine_after, skin_after]
})

# --------------------------
# 시각화 1: 비교 바차트
# --------------------------
st.subheader("📊 정책 적용 전 vs 후 비교")

st.bar_chart(df.set_index("질환"))

# --------------------------
# 시각화 2: 변화율 (%)
# --------------------------
df["변화율(%)"] = (df["정책 적용 후"] - df["기존"]) / df["기존"] * 100

st.subheader("📉 변화율 (%)")

st.dataframe(df.style.format({
    "기존": "{:.1f}",
    "정책 적용 후": "{:.1f}",
    "변화율(%)": "{:.1f}%"
}))

# --------------------------
# 시각화 3: 게이지 느낌 (progress bar)
# --------------------------
st.subheader("📈 위험도 수준")

def risk_bar(value, base):
    ratio = min(value / (base * 2), 1.0)
    st.progress(ratio)

st.write("소화기 질환")
risk_bar(gastro_after, BASELINE["gastro"])

st.write("내분비 질환")
risk_bar(endocrine_after, BASELINE["endocrine"])

st.write("피부 질환")
risk_bar(skin_after, BASELINE["skin"])

# --------------------------
# 인사이트
# --------------------------
st.subheader("💡 해석")

st.markdown(f"""
- 현재 BOD: **{bod} mg/L**
- 중금속: **{metal} μg/L**
- 클로로필-a: **{chl} μg/L**

👉 수질 변화가 질환 발생에 **비례적으로 영향**을 주는 구조

**핵심 해석**
- BOD ↑ → 소화기 질환 증가
- 중금속 ↑ → 내분비 질환 증가
- 녹조 ↑ → 피부 질환 증가

👉 선택한 정책: **{scenario}**
""")
