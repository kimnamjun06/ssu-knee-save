import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="숭실대 무릎 피로도 가이드", layout="wide", page_icon="🦵")

sections = {
    "입구 → 학생회관": {
        "경로": ["엘리베이터", "언덕", "계단"],
        "최대Peak": [45.25, 56.92, 59.78],
        "95%Peak": [18.93, 18.86, 21.48],
        "평균Peak": [9.89, 9.45, 10.40],
        "RMS": [5.551, 5.357, 6.151],
        "초당충격량": [22.64, 24.39, 27.82],
        "피로도점수": [88.8, 88.2, 100.0],
    },
    "학생회관 → 도서관": {
        "경로": ["엘리베이터", "언덕", "계단"],
        "최대Peak": [32.98, 42.55, 64.58],
        "95%Peak": [18.45, 21.45, 21.90],
        "평균Peak": [9.83, 10.73, 11.18],
        "RMS": [4.308, 6.244, 6.560],
        "초당충격량": [13.10, 26.96, 28.37],
        "피로도점수": [71.8, 96.1, 100.0],
    },
}

def get_grade(score):
    if score >= 90:
        return "상 🔴", "#FF4444", "무릎에 높은 부담. 무릎 질환자는 반드시 피하세요."
    elif score >= 75:
        return "중 🟡", "#FFB300", "보통 수준의 부담. 장시간 반복 시 주의하세요."
    else:
        return "하 🟢", "#4CAF50", "무릎 부담이 적습니다. 안심하고 이용하세요."

st.markdown("""
<div style="background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem;">
    <h1 style="color: white; margin:0; font-size: 2.2rem;">🦵 숭실대 캠퍼스 무릎 피로도 가이드</h1>
    <p style="color: #bbdefb; margin: 0.5rem 0 0 0; font-size: 1.1rem;">Phyphox 보행 가속도 데이터 기반 | 입구 → 학생회관 → 도서관</p>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["📍 입구 → 학생회관", "📍 학생회관 → 도서관", "📊 전체 비교"])

for tab_idx, (section_name, sdata) in enumerate(sections.items()):
    df = pd.DataFrame(sdata)
    df["피로등급"], df["색상"], df["가이드"] = zip(*df["피로도점수"].map(get_grade))

    with tabs[tab_idx]:
        st.markdown(f"## {section_name}")
        cols = st.columns(3)
        icons = ["🛗", "🏔️", "🪜"]
        for i, row in df.iterrows():
            with cols[i]:
                grade, color, guide = row["피로등급"], row["색상"], row["가이드"]
                st.markdown(f"""
                <div style="background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 2px 12px rgba(0,0,0,0.08); border-top: 5px solid {color}; min-height: 300px;">
                    <h2 style="margin:0; font-size:1.4rem;">{icons[i]} {row["경로"]}</h2>
                    <div style="font-size: 3rem; font-weight: bold; color: {color}; margin: 0.5rem 0;">{row["피로도점수"]}<span style="font-size:1.2rem;">/100</span></div>
                    <div style="display:inline-block; background:{color}22; color:{color}; padding: 4px 16px; border-radius: 20px; font-weight: bold; font-size: 1.1rem;">피로도 {grade}</div>
                    <p style="margin-top: 1rem; color: #555; font-size: 0.95rem;">{guide}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📊 Peak 가속도 비교")
            fig_peak = go.Figure()
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

        st.markdown("### 🎯 무릎 피로도 게이지")
        gauge_cols = st.columns(3)
        for i, row in df.iterrows():
            with gauge_cols[i]:
                fig_g = go.Figure(go.Indicator(
                    mode="gauge+number", value=row["피로도점수"],
                    title={"text": row["경로"]},
                    gauge={"axis": {"range": [0, 100]}, "bar": {"color": row["색상"]},
                           "steps": [{"range": [0, 50], "color": "#E8F5E9"}, {"range": [50, 75], "color": "#FFF9C4"},
                                     {"range": [75, 90], "color": "#FFE0B2"}, {"range": [90, 100], "color": "#FFCDD2"}],
                           "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 90}}))
                fig_g.update_layout(height=250, margin=dict(t=40, b=0, l=30, r=30))
                st.plotly_chart(fig_g, use_container_width=True)

        st.markdown("### 📋 측정 데이터")
        display_df = df[["경로", "최대Peak", "95%Peak", "평균Peak", "RMS", "초당충격량", "피로도점수", "피로등급"]].copy()
        display_df.columns = ["경로", "최대 Peak (m/s²)", "95% Peak (m/s²)", "평균 Peak (m/s²)", "RMS (m/s²)", "초당 충격량", "피로도 점수", "피로 등급"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

with tabs[2]:
    st.markdown("## 📊 전체 구간 비교")
    all_rows = []
    for section_name, sdata in sections.items():
        for i in range(3):
            all_rows.append({
                "구간": section_name, "경로": sdata["경로"][i],
                "최대Peak": sdata["최대Peak"][i], "95%Peak": sdata["95%Peak"][i],
                "평균Peak": sdata["평균Peak"][i], "RMS": sdata["RMS"][i],
                "초당충격량": sdata["초당충격량"][i], "피로도점수": sdata["피로도점수"][i],
            })
    all_df = pd.DataFrame(all_rows)
    all_df["피로등급"] = all_df["피로도점수"].map(lambda s: get_grade(s)[0])
    colors_map = {"엘리베이터": "#2196F3", "언덕": "#4CAF50", "계단": "#F44336"}

    fig_all = go.Figure()
    for route in ["엘리베이터", "언덕", "계단"]:
        sub = all_df[all_df["경로"] == route]
        fig_all.add_trace(go.Bar(name=route, x=sub["구간"], y=sub["피로도점수"], text=sub["피로도점수"], textposition="outside", marker_color=colors_map[route]))
    fig_all.update_layout(barmode="group", height=450, yaxis_title="피로도 점수 (/100)", template="plotly_white", title="구간 × 경로별 무릎 피로도 점수",
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_all, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_r = go.Figure()
        for route in ["엘리베이터", "언덕", "계단"]:
            sub = all_df[all_df["경로"] == route]
            fig_r.add_trace(go.Bar(name=route, x=sub["구간"], y=sub["RMS"], text=sub["RMS"].round(2), textposition="outside", marker_color=colors_map[route]))
        fig_r.update_layout(barmode="group", height=400, yaxis_title="RMS (m/s²)", template="plotly_white", title="구간별 RMS 비교")
        st.plotly_chart(fig_r, use_container_width=True)

    with col2:
        fig_p = go.Figure()
        for route in ["엘리베이터", "언덕", "계단"]:
            sub = all_df[all_df["경로"] == route]
            fig_p.add_trace(go.Bar(name=route, x=sub["구간"], y=sub["95%Peak"], text=sub["95%Peak"].round(1), textposition="outside", marker_color=colors_map[route]))
        fig_p.update_layout(barmode="group", height=400, yaxis_title="95% Peak (m/s²)", template="plotly_white", title="구간별 95% Peak 비교")
        st.plotly_chart(fig_p, use_container_width=True)

    st.markdown("### 📋 전체 데이터")
    show_df = all_df[["구간", "경로", "최대Peak", "95%Peak", "평균Peak", "RMS", "초당충격량", "피로도점수", "피로등급"]].copy()
    show_df.columns = ["구간", "경로", "최대 Peak", "95% Peak", "평균 Peak", "RMS", "초당 충격량", "피로도 점수", "피로 등급"]
    st.dataframe(show_df, use_container_width=True, hide_index=True)

    st.markdown("""
    ---
    ### 💡 핵심 인사이트
    - **계단은 두 구간 모두 피로도 1위** — 특히 학생회관→도서관 계단은 최대 Peak 64.58 m/s²로 전 구간 최고
    - **입구→학생회관**: 세 경로 피로도 차이가 크지 않음 (88~100) → 어떤 경로든 부담은 비슷
    - **학생회관→도서관**: 엘리베이터(71.8)만 확실히 낮음 → **이 구간에서 엘리베이터가 가장 효과적**
    - **언덕**은 구간에 따라 편차가 큼 — 입구 구간은 양호하나, 도서관 구간은 계단에 근접
    """)

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
