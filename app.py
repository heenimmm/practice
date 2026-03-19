import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="수질-건강 영향 분석",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if st.session_state.dark_mode:
    BG          = "#0B0F1A"
    CARD_BG     = "#111827"
    SIDEBAR_BG  = "#0D1321"
    BORDER      = "#1E2D40"
    TEXT        = "#E8EDF5"
    SUBTEXT     = "#8A97AA"
    ACCENT      = "#38BDF8"
    ACCENT2     = "#818CF8"
    DANGER      = "#F87171"
    SUCCESS     = "#34D399"
    CHART_BEFORE = "#38BDF8"
    CHART_AFTER  = "#34D399"
    TOGGLE_ICON  = "☀️"
    TOGGLE_LABEL = "라이트 모드로 전환"
else:
    BG          = "#F0F4FA"
    CARD_BG     = "#FFFFFF"
    SIDEBAR_BG  = "#E8EEF7"
    BORDER      = "#CBD5E1"
    TEXT        = "#0F172A"
    SUBTEXT     = "#64748B"
    ACCENT      = "#0369A1"
    ACCENT2     = "#6366F1"
    DANGER      = "#DC2626"
    SUCCESS     = "#059669"
    CHART_BEFORE = "#0369A1"
    CHART_AFTER  = "#059669"
    TOGGLE_ICON  = "🌙"
    TOGGLE_LABEL = "다크 모드로 전환"

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap');

  html, body, [data-testid="stAppViewContainer"] {{
      background-color: {BG} !important;
      color: {TEXT} !important;
      font-family: 'Noto Sans KR', sans-serif;
  }}
  [data-testid="stSidebar"] {{
      background-color: {SIDEBAR_BG} !important;
      border-right: 1px solid {BORDER};
  }}
  [data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
  h1, h2, h3 {{
      color: {TEXT} !important;
      font-family: 'Noto Sans KR', sans-serif !important;
      font-weight: 700 !important;
      letter-spacing: -0.02em;
  }}
  [data-testid="block-container"] {{
      background-color: {BG} !important;
      padding-top: 1.5rem !important;
  }}
  .wq-card {{
      background: {CARD_BG};
      border: 1px solid {BORDER};
      border-radius: 14px;
      padding: 1.4rem 1.6rem;
      margin-bottom: 1.2rem;
  }}
  .wq-divider {{
      border: none;
      border-top: 1px solid {BORDER};
      margin: 1.6rem 0;
  }}
  [data-testid="stMetric"] {{
      background: {CARD_BG} !important;
      border: 1px solid {BORDER};
      border-radius: 14px;
      padding: 1.2rem 1.4rem !important;
  }}
  [data-testid="stMetricLabel"] {{
      color: {SUBTEXT} !important;
      font-size: 0.8rem !important;
      font-weight: 500 !important;
  }}
  [data-testid="stMetricValue"] {{
      color: {TEXT} !important;
      font-family: 'Space Mono', monospace !important;
      font-size: 1.9rem !important;
  }}
  [data-testid="stSelectbox"] div[data-baseweb="select"] {{
      background-color: {CARD_BG} !important;
      border-color: {BORDER} !important;
      border-radius: 10px;
  }}
  [data-testid="stDataFrame"] {{
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid {BORDER} !important;
  }}
  .stButton > button {{
      background: {CARD_BG} !important;
      color: {TEXT} !important;
      border: 1px solid {BORDER} !important;
      border-radius: 8px !important;
      font-family: 'Noto Sans KR', sans-serif !important;
      font-weight: 500 !important;
      transition: all 0.2s;
  }}
  .stButton > button:hover {{
      border-color: {ACCENT} !important;
      color: {ACCENT} !important;
  }}
  [data-testid="stProgress"] > div > div > div > div {{
      background: linear-gradient(90deg, {ACCENT}, {ACCENT2}) !important;
  }}
  .stSlider label {{
      color: {SUBTEXT} !important;
      font-size: 0.82rem !important;
      font-weight: 500 !important;
  }}
  footer, #MainMenu {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

BASELINE = {
    "bod": 4.0, "metal": 2.2, "chl": 50.0,
    "gastro": 66.5, "endocrine": 35.6, "skin": 110.5,
}

# ── 사이드바 ──
with st.sidebar:
    try:
        from PIL import Image
        logo = Image.open("image.png")
        st.image(logo, use_container_width=True)
    except Exception:
        pass

    st.markdown(f"<div style='height:0.8rem;'></div>", unsafe_allow_html=True)

    col_t1, col_t2 = st.columns([3, 2])
    with col_t1:
        mode_text = "🌙 다크 모드" if st.session_state.dark_mode else "☀️ 라이트 모드"
        st.markdown(
            f"<p style='color:{SUBTEXT};font-size:0.8rem;margin:0;padding-top:8px;'>{mode_text}</p>",
            unsafe_allow_html=True
        )
    with col_t2:
        if st.button(TOGGLE_ICON, key="theme_toggle", help=TOGGLE_LABEL):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.markdown(f"<hr style='border-color:{BORDER};margin:1rem 0 1.2rem;'>", unsafe_allow_html=True)

    st.markdown(
        f"<p style='color:{ACCENT};font-size:0.72rem;font-weight:700;letter-spacing:0.1em;"
        f"text-transform:uppercase;margin-bottom:0.8rem;'>수질 지표 입력</p>",
        unsafe_allow_html=True
    )
    bod   = st.slider("💧 BOD (mg/L)",        0.0, 10.0,  BASELINE["bod"],   0.1)
    metal = st.slider("⚗️ 중금속 Pb (μg/L)",  0.0,  5.0,  BASELINE["metal"], 0.1)
    chl   = st.slider("🌿 클로로필-a (μg/L)", 0.0, 100.0, BASELINE["chl"],   1.0)

    st.markdown(f"<hr style='border-color:{BORDER};margin:1.2rem 0;'>", unsafe_allow_html=True)

    st.markdown(
        f"<p style='color:{ACCENT};font-size:0.72rem;font-weight:700;letter-spacing:0.1em;"
        f"text-transform:uppercase;margin-bottom:0.8rem;'>정책 시나리오</p>",
        unsafe_allow_html=True
    )
    scenario = st.selectbox(
        "시나리오 선택",
        ["없음", "BOD 20% 감소", "중금속 30% 감소", "통합 개선 (A+B+C)"],
        label_visibility="collapsed"
    )

    st.markdown(f"<hr style='border-color:{BORDER};margin:1.2rem 0;'>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:{SUBTEXT};font-size:0.75rem;line-height:1.7;'>"
        f"<b style='color:{TEXT};'>낙동강</b> 평균 BOD <b style='color:{DANGER};'>4.00</b> mg/L<br>"
        f"<b style='color:{TEXT};'>북한강</b> 평균 BOD <b style='color:{SUCCESS};'>1.67</b> mg/L"
        f"</p>",
        unsafe_allow_html=True
    )

# ── 예측 모델 ──
def predict(b, m, c):
    return (
        BASELINE["gastro"]    * (b / BASELINE["bod"]),
        BASELINE["endocrine"] * (m / BASELINE["metal"]),
        BASELINE["skin"]      * (c / BASELINE["chl"]),
    )

gastro, endocrine, skin = predict(bod, metal, chl)
gastro_a, endocrine_a, skin_a = gastro, endocrine, skin

if scenario == "BOD 20% 감소":
    gastro_a *= 0.85
elif scenario == "중금속 30% 감소":
    endocrine_a *= 0.85
elif scenario == "통합 개선 (A+B+C)":
    gastro_a *= 0.85; endocrine_a *= 0.88; skin_a *= 0.92

# ── 헤더 ──
st.markdown(
    f"""
    <div style="margin-bottom:0.3rem;">
      <span style="color:{ACCENT};font-size:0.72rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;">
        보건환경정책연구원 · 2025
      </span>
    </div>
    <h1 style="font-size:2rem;line-height:1.2;margin-bottom:0.3rem;">
      💧 수질오염 → 건강 영향 시뮬레이터
    </h1>
    <p style="color:{SUBTEXT};font-size:0.95rem;margin-bottom:0;">
      낙동강·북한강 유역 수질 지표를 조정하여 질환 방문 위험도 변화를 실시간으로 확인합니다.
    </p>
    """,
    unsafe_allow_html=True
)

status_color = DANGER if bod > 5 else (ACCENT if bod > 3 else SUCCESS)
status_label = "위험" if bod > 5 else ("주의" if bod > 3 else "양호")
st.markdown(
    f"""
    <div style="margin:1rem 0 1.6rem;">
      <span style="background:{status_color}22;color:{status_color};border:1px solid {status_color}55;
                   border-radius:99px;font-size:0.73rem;font-weight:700;padding:3px 12px;">
        ● 현재 수질 상태: {status_label}
      </span>
      <span style="color:{SUBTEXT};font-size:0.8rem;margin-left:10px;font-family:'Space Mono',monospace;">
        BOD {bod:.1f} · 중금속 {metal:.1f} · Chl-a {chl:.0f}
      </span>
    </div>
    """,
    unsafe_allow_html=True
)

# ── KPI ──
st.markdown(
    f"<p style='color:{ACCENT};font-size:0.72rem;font-weight:700;letter-spacing:0.1em;"
    f"text-transform:uppercase;margin-bottom:0.8rem;'>📌 월간 의료기관 방문 예측</p>",
    unsafe_allow_html=True
)
c1, c2, c3 = st.columns(3)

def delta_fmt(after, before):
    d = after - before
    if abs(d) < 0.05: return "변화 없음"
    return f"{'+'if d>0 else''}{d:.1f} 회"

c1.metric("🥗 소화기 질환",  f"{gastro_a:.1f} 회",    delta_fmt(gastro_a, gastro),    delta_color="inverse")
c2.metric("🧬 내분비 질환",  f"{endocrine_a:.1f} 회",  delta_fmt(endocrine_a, endocrine), delta_color="inverse")
c3.metric("🌸 피부 질환",    f"{skin_a:.1f} 회",       delta_fmt(skin_a, skin),         delta_color="inverse")

st.markdown(f"<hr class='wq-divider'>", unsafe_allow_html=True)

# ── 차트 + 위험도 ──
left_col, right_col = st.columns([3, 2], gap="large")

with left_col:
    st.markdown(
        f"<p style='color:{ACCENT};font-size:0.72rem;font-weight:700;letter-spacing:0.1em;"
        f"text-transform:uppercase;margin-bottom:0.6rem;'>📊 정책 적용 전 / 후 비교</p>",
        unsafe_allow_html=True
    )
    df_chart = pd.DataFrame({
        "질환": ["소화기", "내분비", "피부"],
        "정책 적용 전": [gastro, endocrine, skin],
        "정책 적용 후": [gastro_a, endocrine_a, skin_a]
    }).set_index("질환")
    st.bar_chart(df_chart, color=[CHART_BEFORE, CHART_AFTER])

    st.markdown(
        f"<p style='color:{ACCENT};font-size:0.72rem;font-weight:700;letter-spacing:0.1em;"
        f"text-transform:uppercase;margin:1.2rem 0 0.5rem;'>📉 변화율 요약</p>",
        unsafe_allow_html=True
    )
    df_pct = pd.DataFrame({
        "질환":         ["소화기", "내분비", "피부"],
        "정책 전 (회)": [round(gastro,1), round(endocrine,1), round(skin,1)],
        "정책 후 (회)": [round(gastro_a,1), round(endocrine_a,1), round(skin_a,1)],
        "변화율 (%)":   [
            round((gastro_a-gastro)/gastro*100,1),
            round((endocrine_a-endocrine)/endocrine*100,1),
            round((skin_a-skin)/skin*100,1)
        ]
    })
    st.dataframe(df_pct, use_container_width=True, hide_index=True)

with right_col:
    st.markdown(
        f"<p style='color:{ACCENT};font-size:0.72rem;font-weight:700;letter-spacing:0.1em;"
        f"text-transform:uppercase;margin-bottom:0.8rem;'>📈 위험도 수준</p>",
        unsafe_allow_html=True
    )
    for lbl, val, base in [
        ("🥗 소화기 질환", gastro_a,    BASELINE["gastro"]),
        ("🧬 내분비 질환", endocrine_a, BASELINE["endocrine"]),
        ("🌸 피부 질환",  skin_a,      BASELINE["skin"]),
    ]:
        r = min(val / (base * 1.5), 1.0)
        if r > 0.75:   color, status = DANGER, "위험"
        elif r > 0.5:  color, status = "#FBBF24", "주의"
        else:          color, status = SUCCESS, "양호"
        st.markdown(
            f"""
            <div style="background:{CARD_BG};border:1px solid {BORDER};border-radius:12px;
                        padding:1rem 1.2rem;margin-bottom:0.8rem;">
              <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                <span style="font-size:0.88rem;font-weight:600;color:{TEXT};">{lbl}</span>
                <span style="background:{color}22;color:{color};border:1px solid {color}44;
                             border-radius:99px;font-size:0.7rem;font-weight:700;padding:2px 8px;">
                  {status}
                </span>
              </div>
              <div style="background:{BORDER};border-radius:99px;height:8px;overflow:hidden;">
                <div style="background:linear-gradient(90deg,{ACCENT},{color});
                            width:{r*100:.1f}%;height:100%;border-radius:99px;"></div>
              </div>
              <div style="display:flex;justify-content:space-between;margin-top:0.3rem;">
                <span style="font-size:0.7rem;color:{SUBTEXT};">0</span>
                <span style="font-size:0.7rem;color:{SUBTEXT};font-family:'Space Mono',monospace;">
                  {val:.1f} / {base*1.5:.0f} 회
                </span>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(f"<hr style='border-color:{BORDER};margin:0.4rem 0 0.6rem;'>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:{ACCENT};font-size:0.72rem;font-weight:700;letter-spacing:0.1em;"
        f"text-transform:uppercase;margin-bottom:0.5rem;'>🌊 유역별 비교</p>",
        unsafe_allow_html=True
    )
    df_compare = pd.DataFrame({
        "유역":    ["낙동강", "북한강"],
        "BOD":     [4.00, 1.67],
        "중금속":  [2.21, 0.61],
        "Chl-a":  [51.83, 16.16],
    })
    st.dataframe(df_compare, use_container_width=True, hide_index=True)

st.markdown(f"<hr class='wq-divider'>", unsafe_allow_html=True)

# ── 해석 카드 ──
st.markdown(
    f"<p style='color:{ACCENT};font-size:0.72rem;font-weight:700;letter-spacing:0.1em;"
    f"text-transform:uppercase;margin-bottom:0.8rem;'>💡 분석 해석</p>",
    unsafe_allow_html=True
)
i1, i2, i3 = st.columns(3)
for col, icon, title, desc, corr_val in [
    (i1,"🔵","BOD → 소화기",
     "유기물 오염(BOD↑)은 수인성 병원균 증식을 촉진해 소화기 질환 방문을 직접 증가시킵니다.","r = 0.985"),
    (i2,"🟣","중금속 → 내분비",
     "납·카드뮴·비소는 에스트로겐 수용체 교란, 갑상선 호르몬 억제 등 내분비계 독성 경로에 작용합니다.","r ≈ 0.98"),
    (i3,"🟢","녹조 → 피부",
     "클로로필-a 증가는 시아노톡신·부유 미립자를 통해 피부 자극·염증 반응을 유발합니다.","r = 0.859"),
]:
    with col:
        st.markdown(
            f"""<div class="wq-card">
              <div style="font-size:1.5rem;margin-bottom:0.5rem;">{icon}</div>
              <div style="font-size:0.9rem;font-weight:700;color:{TEXT};margin-bottom:0.4rem;">{title}</div>
              <div style="font-size:0.8rem;color:{SUBTEXT};line-height:1.6;margin-bottom:0.6rem;">{desc}</div>
              <span style="background:{ACCENT}22;color:{ACCENT};border:1px solid {ACCENT}44;
                           border-radius:6px;font-size:0.7rem;font-weight:700;padding:2px 8px;
                           font-family:'Space Mono',monospace;">{corr_val}</span>
            </div>""",
            unsafe_allow_html=True
        )

# ── 정책 요약 ──
if scenario != "없음":
    st.markdown(f"<hr class='wq-divider'>", unsafe_allow_html=True)
    total = abs(gastro_a-gastro) + abs(endocrine_a-endocrine) + abs(skin_a-skin)
    st.markdown(
        f"""<div style="background:{ACCENT}11;border:1px solid {ACCENT}44;border-radius:14px;
                        padding:1.2rem 1.6rem;">
          <p style="color:{ACCENT};font-size:0.72rem;font-weight:700;letter-spacing:0.08em;
                    text-transform:uppercase;margin:0 0 0.4rem;">선택 정책: {scenario}</p>
          <p style="color:{TEXT};font-size:1rem;margin:0;">
            정책 적용 시 3개 질환 방문 총
            <b style="color:{SUCCESS};font-family:'Space Mono',monospace;"> {total:.1f}회/월</b> 감소 예상
          </p>
          <p style="color:{SUBTEXT};font-size:0.8rem;margin:0.4rem 0 0;">
            낙동강 유역 인구 규모를 고려할 때 연간 수십억 원 규모의 의료비 절감 효과가 기대됩니다.
          </p>
        </div>""",
        unsafe_allow_html=True
    )

# ── 푸터 ──
st.markdown(
    f"""<div style="margin-top:3rem;padding:1.2rem 0;border-top:1px solid {BORDER};
                    display:flex;justify-content:space-between;flex-wrap:wrap;gap:0.4rem;">
      <span style="color:{SUBTEXT};font-size:0.73rem;">
        © 2025 보건환경정책연구원 · 낙동강·북한강 유역 수질-건강 영향 분석
      </span>
      <span style="color:{SUBTEXT};font-size:0.73rem;font-family:'Space Mono',monospace;">
        n = 50 · Pearson r · 2023–2025
      </span>
    </div>""",
    unsafe_allow_html=True
)
