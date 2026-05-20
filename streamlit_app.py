import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="🦵 숭실대 무릎 피로도 가이드", layout="wide", page_icon="🦵")

# --- 데이터 정의 ---
data = {
    "구간": ["학생회관→도서관"] * 3,
    "경로": ["엘리베이터", "언덕", "계단"],
    "최대Peak": [32.98, 42.55, 64.58],
    "95%Peak": [18.45, 21.45, 21.90],
    "평균Peak": [9.83, 10.73, 11.18],
    "RMS": [4.308, 6.244, 6.560],
    "초당충격량": [13.10, 26.96, 28.37],
    "피로도점수": [71.8, 96.1, 100.0],
}
df = pd.DataFrame(data)

def get_grade(score):
    if score >= 90:
        return "상 🔴", "#FF4444", "무릎에 높은 부담이 가해집니다. 무릎 질환자는 반드시 피하세요."
    elif score >= 75:
        return "중 🟡", "#FFB300", "보통 수준의 부담입니다. 장시간 반복 시 주의하세요."
    else:
        return "하 🟢", "#4CAF50", "무릎 부담이 적습니다. 안심하고 이용하세요."

df["피로등급"], df["색상"], df["가이드"] = zip(*df["피로도점수"].map(get_grade))

# --- 헤더 ---
st.markdown("""
<div style="background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem;">
    <h1 style="color: white; margin:0; font-size: 2.2rem;">🦵 숭실대 캠퍼스 무릎 피로도 가이드</h1>
    <p style="color: #bbdefb; margin: 0.5rem 0 0 0; font-size: 1.1rem;">Phyphox 보행 가속도 데이터 기반 | 학생회관 → 도서관 구간</p>
</div>
""", unsafe_allow_html=True)

# --- 사이드바: 사용자 조건 ---
st.sidebar.markdown("## 🧑‍🦽 나의 조건 설정")
knee_condition = st.sidebar.selectbox("무릎 상태", ["건강함", "약간 불편", "관절 질환 있음"])
carrying = st.sidebar.selectbox("짐 무게", ["가벼움 (노트북 이하)", "보통 (가방)", "무거움 (캐리어 등)"])
weather = st.sidebar.selectbox("날씨", ["맑음", "비/눈", "결빙"])

st.sidebar.markdown("---")

# 가이드라인 로직
def get_recommendation(knee, carry, wthr):
    if knee == "관절 질환 있음" or wthr == "결빙":
        return "🛗 **엘리베이터**를 강력 권장합니다.", "엘리베이터"
    if wthr == "비/눈" and carry == "무거움 (캐리어 등)":
        return "🛗 미끄럼 + 무거운 짐 → **엘리베이터**가 안전합니다.", "엘리베이터"
    if knee == "약간 불편":
        if carry == "무거움 (캐리어 등)":
            return "🛗 무릎 부담 최소화를 위해 **엘리베이터**를 추천합니다.", "엘리베이터"
        return "🏔️ **언덕**도 괜찮지만, 불편하면 **엘리베이터**를 이용하세요.", "언덕"
    if carry == "무거움 (캐리어 등)":
        return "🛗 짐이 무거우면 **엘리베이터**가 현명한 선택입니다.", "엘리베이터"
    return "🏔️ 건강하다면 **언덕**으로! 운동 효과도 있고 계단보다 무릎에 덜합니다.", "언덕"

rec_text, rec_route = get_recommendation(knee_condition, carrying, weather)

st.sidebar.markdown("### 🧭 맞춤 추천 경로")
rec_color = "#4CAF50" if rec_route == "엘리베이터" else "#FFB300"
st.sidebar.markdown(f"""
<div style="background: {rec_color}22; border-left: 4px solid {rec_color}; padding: 1rem; border-radius: 8px;">
{rec_text}
</div>
""", unsafe_allow_html=True)

# --- 메인: 피로도 카드 3개 ---
cols = st.columns(3)
for i, row in df.iterrows():
    with cols[i]:
        grade, color, guide = row["피로등급"], row["색상"], row["가이드"]
        st.markdown(f"""
        <div style="background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 2px 12px rgba(0,0,0,0.08); border-top: 5px solid {color}; height: 320px;">
            <h2 style="margin:0; font-size:1.4rem;">{["🛗","🏔️","🪜"][i]} {row["경로"]}</h2>
            <div style="font-size: 3rem; font-weight: bold; color: {color}; margin: 0.5rem 0;">{row["피로도점수"]}<span style="font-size:1.2rem;">/100</span></div>
            <div style="display:inline-block; background:{color}22; color:{color}; padding: 4px 16px; border-radius: 20px; font-weight: bold; font-size: 1.1rem;">피로도 {grade}</div>
            <p style="margin-top: 1rem; color: #555; font-size: 0.95rem;">{guide}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 비교 차트 ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Peak 가속도 비교")
    fig_peak = go.Figure()
    colors = ["#2196F3", "#4CAF50", "#F44336"]
    for metric, name in [("최대Peak", "최대 Peak"), ("95%Peak", "95% Peak"), ("평균Peak", "평균 Peak")]:
        fig_peak.add_trace(go.Bar(name=name, x=df["경로"], y=df[metric], text=df[metric].round(1), textposition="outside"))
    fig_peak.update_layout(barmode="group", height=400, yaxis_title="m/s²", template="plotly_white",
                           legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_peak, use_container_width=True)

with col2:
    st.markdown("### 📊 RMS & 초당 충격량 비교")
    fig_rms = go.Figure()
    fig_rms.add_trace(go.Bar(name="RMS (m/s²)", x=df["경로"], y=df["RMS"], text=df["RMS"].round(2), textposition="outside", marker_color="#7E57C2"))
    fig_rms.add_trace(go.Bar(name="초당 충격량", x=df["경로"], y=df["초당충격량"], text=df["초당충격량"].round(1), textposition="outside", marker_color="#FF7043"))
    fig_rms.update_layout(barmode="group", height=400, yaxis_title="수치", template="plotly_white",
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_rms, use_container_width=True)

# --- 게이지 차트 ---
st.markdown("### 🎯 경로별 무릎 피로도 게이지")
gauge_cols = st.columns(3)
for i, row in df.iterrows():
    with gauge_cols[i]:
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=row["피로도점수"],
            title={"text": f"{row['경로']}"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": row["색상"]},
                "steps": [
                    {"range": [0, 50], "color": "#E8F5E9"},
                    {"range": [50, 75], "color": "#FFF9C4"},
                    {"range": [75, 90], "color": "#FFE0B2"},
                    {"range": [90, 100], "color": "#FFCDD2"},
                ],
                "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 90},
            },
        ))
        fig_g.update_layout(height=250, margin=dict(t=40, b=0, l=30, r=30))
        st.plotly_chart(fig_g, use_container_width=True)

# --- 상세 데이터 테이블 ---
st.markdown("### 📋 전체 측정 데이터")
display_df = df[["경로", "최대Peak", "95%Peak", "평균Peak", "RMS", "초당충격량", "피로도점수", "피로등급"]].copy()
display_df.columns = ["경로", "최대 Peak (m/s²)", "95% Peak (m/s²)", "평균 Peak (m/s²)", "RMS (m/s²)", "초당 충격량", "피로도 점수", "피로 등급"]
st.dataframe(display_df, use_container_width=True, hide_index=True)

# --- 가이드라인 ---
st.markdown("""
---
### 📌 무릎 보호 가이드라인

| 피로 등급 | 점수 범위 | 대상 | 권장 사항 |
|:--:|:--:|:--|:--|
| **하 🟢** | 0 ~ 74 | 모든 학우 | 안심하고 이용 가능. 무릎 부담 최소 |
| **중 🟡** | 75 ~ 89 | 일반 학우 | 반복 이용 시 스트레칭 권장. 무거운 짐은 피할 것 |
| **상 🔴** | 90 ~ 100 | 주의 필요 | 무릎 질환자·고령자는 회피 권장. 불가피 시 보조기 착용 |

> 💡 **Tip**: 비 오는 날이나 짐이 무거울 때는 한 단계 높여서 판단하세요!
""")

st.markdown("""
<div style="text-align:center; color:#999; padding: 2rem; font-size: 0.85rem;">
    Phyphox 앱 측정 데이터 기반 | 숭실대학교 캠퍼스 접근성 연구
</div>
""", unsafe_allow_html=True)

 
