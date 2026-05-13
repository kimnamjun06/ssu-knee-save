import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 앱 제목 및 설정
st.set_page_config(page_title="숭실대 무릎수호단", page_icon="🦵")
st.title("⛰️ 숭실대 무릎수호단: 경로별 피로도 분석")
st.write("측정한 Phyphox 엑셀 파일을 업로드하면 AI가 무릎 피로도를 계산합니다.")

# 2. 파일 업로드 기능
uploaded_file = st.file_uploader("Phyphox 엑셀 파일을 선택하세요", type=['xlsx'])

if uploaded_file:
    # 데이터 불러오기
    df = pd.read_excel(uploaded_file)
   
    # 가속도 컬럼 찾기 (Phyphox 기본 컬럼명 기준)
    acc_col = 'Absolute acceleration (m/s^2)'
   
    if acc_col in df.columns:
        data = df[acc_col]
       
        # 3. 핵심 로직 계산 (우리가 정한 가중치 모델)
        peak_95 = data.quantile(0.95) # 상위 5% Peak
        rms = np.sqrt(np.mean(data**2)) # 평균 압박감
        impact = data.mean() # 누적 에너지 지표
       
        # 점수 정규화 및 가중치 적용 (계단을 100점으로 만드는 로직)
        # 실제 발표시는 위에서 계산한 수치를 상수로 매칭해도 좋습니다.
        fatigue_score = (peak_95 * 0.6) + (rms * 0.25) + (impact * 0.15)
       
        # 4. 결과 화면 출력
        st.divider()
        col1, col2 = st.columns(2)
       
        with col1:
            st.metric(label="📊 최종 무릎 피로도 점수", value=f"{min(fatigue_score*5, 100):.1f} / 100")
       
        with col2:
            if fatigue_score > 15: # 임계치는 데이터에 따라 조정
                st.error("위험: 무릎에 충격이 큽니다!")
            else:
                st.success("안전: 무릎이 편안한 경로입니다.")

        # 5. 시각화 그래프
        st.subheader("📈 구간별 충격 변화")
        fig, ax = plt.subplots()
        ax.plot(df['Time (s)'], data, alpha=0.7, color='#3498db')
        ax.set_xlabel("시간 (s)")
        ax.set_ylabel("가속도 (m/s²)")
        st.pyplot(fig)
       
    else:
        st.warning("엑셀 파일에서 'Absolute acceleration (m/s^2)' 컬럼을 찾을 수 없습니다.")

# 6. 하단 정보
st.info("💡 Tip: 이 앱은 60%의 Peak 가중치 알고리즘을 사용합니다.")
 
