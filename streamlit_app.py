import streamlit as st
import joblib
import numpy as np

# 모델 로드
try:
    model = joblib.load('brix_model.joblib')
except Exception as e:
    st.error(f"모델 로드 실패: {e}")
    st.stop()

# 앱 제목
st.title("🍊 제주도 성산지역 감귤 당도 예측 모델")
st.markdown("---")

# 설명
st.write("아래의 기후 데이터를 입력하면 감귤의 당도(Brix)를 예측합니다.")

# 입력 폼
st.subheader("📊 기후 데이터 입력")

col1, col2 = st.columns(2)

with col1:
    avg_temp = st.number_input(
        "평균기온 (℃)",
        min_value=-10.0,
        max_value=50.0,
        value=15.0,
        step=0.1,
        help="연중 또는 특정 기간의 평균 기온"
    )

with col2:
    min_temp = st.number_input(
        "최저기온 (℃)",
        min_value=-30.0,
        max_value=30.0,
        value=5.0,
        step=0.1,
        help="연중 또는 특정 기간의 최저 기온"
    )

col3, col4 = st.columns(2)

with col3:
    sun_hours = st.number_input(
        "가조시간 (시간)",
        min_value=0.0,
        max_value=5000.0,
        value=2000.0,
        step=10.0,
        help="햇빛을 받은 누적 시간"
    )

with col4:
    min_frost_temp = st.number_input(
        "최저 초상온도 (℃)",
        min_value=-20.0,
        max_value=20.0,
        value=-5.0,
        step=0.1,
        help="가장 낮은 초상(서리) 온도"
    )

# 예측 버튼
if st.button("🔮 당도 예측하기", use_container_width=True):
    # 입력값을 배열로 변환
    input_data = np.array([[avg_temp, min_temp, sun_hours, min_frost_temp]])
    
    # 모델로 예측
    prediction = model.predict(input_data)[0]
    
    # 결과 표시
    st.markdown("---")
    st.subheader("✅ 예측 결과")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("예측 당도 (Brix)", f"{prediction:.2f}°Bx")
    
    with col2:
        if prediction >= 12:
            quality = "🌟 매우 우수"
        elif prediction >= 10:
            quality = "⭐ 우수"
        elif prediction >= 8:
            quality = "👍 좋음"
        else:
            quality = "⚠️ 보통"
        st.metric("품질 평가", quality)
    
    # 입력값 요약
    st.markdown("**입력된 기후 데이터:**")
    st.write(f"- 평균기온: {avg_temp}℃")
    st.write(f"- 최저기온: {min_temp}℃")
    st.write(f"- 가조시간: {sun_hours}시간")
    st.write(f"- 최저 초상온도: {min_frost_temp}℃")
