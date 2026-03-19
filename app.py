import streamlit as st
import pandas as pd

st.set_page_config(page_title="수질-건강 영향 분석", layout="wide")

st.title("💧 수질오염과 건강 영향 분석 대시보드")

st.markdown("""
이 앱은 수질오염 지표(BOD, 중금속 등)와 건강 영향(소화기, 내분비 질환)의 관계를
간단한 모델로 시뮬레이션합니다.
""")

# --------------------------
# 사이드바
# --------------------------
st.sidebar.header("📊 설정")

region = st.sidebar.selectbox(
    "유역 선택",
    ["낙동강", "북한강"]
)

bod = st.sidebar.slider("BOD (mg/L)", 0.0, 10.0, 4.0)
tn = st.sidebar.slider("총 질소 (T-N)", 0.0, 5.0, 3.0)
tp = st.sidebar.slider("총 인 (T-P)", 0.0, 0.5, 0.1)

heavy_metal = st.sidebar.slider("중금속 지수 (Pb/Cd/As 종합)", 0.0, 5.0, 2.0)
chlorophyll = st.sidebar.slider("클로로필-a", 0.0, 100.0, 50.0)

# --------------------------
# 간단 예측 모델 (가짜 but 구조용)
# --------------------------
def predict_gastro(bod):
    return bod * 15  # BOD → 소화기

def predict_endocrine(metal):
    return metal * 10  # 중금속 → 내분비

def predict_skin(chl):
    return chl * 1.5  # 조류 → 피부

gastro = predict_gastro(bod)
endocrine = predict_endocrine(heavy_metal)
skin = predict_skin(chlorophyll)

# --------------------------
# 결과 출력
# --------------------------
st.subheader("📈 예측 결과")

col1, col2, col3 = st.columns(3)

col1.metric("소화기 질환 위험", f"{gastro:.1f}")
col2.metric("내분비 질환 위험", f"{endocrine:.1f}")
col3.metric("피부 질환 위험", f"{skin:.1f}")

# --------------------------
# 시각화
# --------------------------
st.subheader("📊 질환 위험 비교")

df = pd.DataFrame({
    "질환": ["소화기", "내분비", "피부"],
    "위험도": [gastro, endocrine, skin]
})

st.bar_chart(df.set_index("질환"))

# --------------------------
# 정책 시나리오
# --------------------------
st.subheader("🏛️ 정책 시나리오 효과")

scenario = st.selectbox(
    "시나리오 선택",
    ["기본", "BOD 20% 감소", "중금속 30% 감소", "통합 개선"]
)

if scenario == "BOD 20% 감소":
    gastro *= 0.85
elif scenario == "중금속 30% 감소":
    endocrine *= 0.85
elif scenario == "통합 개선":
    gastro *= 0.85
    endocrine *= 0.88
    skin *= 0.9

st.write("### 적용 후 질환 위험")

col1, col2, col3 = st.columns(3)
col1.metric("소화기", f"{gastro:.1f}")
col2.metric("내분비", f"{endocrine:.1f}")
col3.metric("피부", f"{skin:.1f}")

# --------------------------
# 인사이트
# --------------------------
st.subheader("💡 인사이트")

st.markdown("""
- BOD 증가 → 소화기 질환 급증
- 중금속 → 내분비 질환과 강한 상관
- 복합 정책 적용 시 전체 질환 감소 효과 발생
""")
