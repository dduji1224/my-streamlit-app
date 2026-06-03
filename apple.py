import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="대학생 장학금 통합 대시보드", layout="wide")

# 전체 제목
st.title("🎓 대학생 학자금 대출 및 등록금 현황 통합 분석")
st.markdown("---")

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    df1 = pd.read_csv("Q1_사각지대_생활비대출_분석용.csv")
    df2 = pd.read_csv("Q2_설립유형별_부담격차_대출_분석용.csv")
    return df1, df2

try:
    df1, df2 = load_data()

    # 레이아웃 구성: 좌우 2단 배치 (왼쪽: 분석 데이터, 오른쪽: 지도)
    left_col, right_col = st.columns([1, 1.2])

    with left_col:
        # 소득분위 지표 영역
        st.subheader("💡 소득분위 사각지대 지표")
        fig1 = px.scatter(df1, x="교외장학금 국가", y="총_생활비대출_금액",
                         hover_name="학교명", size="총_생활비대출_금액",
                         color="총_생활비대출_금액", color_continuous_scale="Blues",
                         title="국가장학금 vs 생활비 대출 상관관계")
        st.plotly_chart(fig1, use_container_width=True)

        st.divider()

        # 부담격차 영역
        st.subheader("🏛️ 설립유형별 부담 격차")
        avg_data = df2.groupby("설립별")[["평균등록금(원)", "총_대출_금액"]].mean().reset_index()
        fig2 = px.bar(avg_data, x="설립별", y="평균등록금(원)", color="설립별",
                     title="설립유형별 평균 등록금 비교", text_auto='.2s')
        st.plotly_chart(fig2, use_container_width=True)

    with right_col:
        # 우측 상단: 전국 학생 1인당 등록금 통계
        st.subheader("📍 전국 학생 1인당 등록금 현황")
        
        # 1인당 등록금 계산
        total_tuition = df2["평균등록금(원)"].sum()
        avg_tuition = df2["평균등록금(원)"].mean()
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("전국 대학 평균 등록금", f"{int(avg_tuition):,d}원")
        col_m2.metric("분석 대학 수", f"{len(df2):,d}개")
        
        st.write("")
        # 지도 영역 (팀원 코드 혹은 기존 지도 HTML 삽입 영역)
        st.info("지도를 클릭하면 상세 정보를 확인할 수 있습니다.")
        st.container(height=500).write("팀원의 지도를 이 영역에 삽입하세요.")

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
