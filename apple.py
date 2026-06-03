apple.txt
import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="대학생 장학금 사각지대 분석", layout="wide")

# 제목 부분
st.title("📊 국가장학금 사각지대 및 대출 의존도 분석")
st.markdown("""
본 대시보드는 **국가장학금 산정 기준(소득분위)에서 벗어난 사각지대 청년들**이 
비싼 등록금과 생활비를 어떻게 대출로 감당하고 있는지 분석한 결과입니다.
""")

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    df1 = pd.read_csv("Q1_사각지대_생활비대출_분석용.csv")
    df2 = pd.read_csv("Q2_설립유형별_부담격차_대출_분석용.csv")
    return df1, df2

try:
    df1, df2 = load_data()

    # 탭 생성 (두 가지 분석 문제를 분리)
    tab1, tab2 = st.tabs(["💡 소득분위 사각지대 분석", "🏛️ 설립유형별 부담 격차"])

    # --- 첫 번째 탭: 사각지대 분석 ---
    with tab1:
        st.header("1. 장학금 사각지대와 생활비 대출의 상관관계")
        st.info("""
        **핵심 지표 설명:**
        - **국가장학금/저소득층장학금 수혜액이 적다:** 소득분위 9~10구간에 속해 지원을 못 받는 학생이 많음을 의미 (프록시 데이터).
        - **생활비 대출 금액:** 장학금 사각지대 학생들이 실질적인 생계 유지를 위해 받는 대출.
        """)

        # 시각화: 산점도 (Scatter Plot)
        # 국가장학금 수혜액과 생활비 대출의 관계
        fig1 = px.scatter(df1, 
                         x="교외장학금 국가 (원)", 
                         y="총_생활비대출_금액",
                         hover_name="대학명",
                         size="전체 대출 금액",
                         color="총_생활비대출_금액",
                         title="국가장학금 수혜액 vs 생활비 대출 규모 (대학별)",
                         labels={"교외장학금 국가 (원)": "국가장학금 총액", "총_생활비대출_금액": "생활비 대출 총액"})
        st.plotly_chart(fig1, use_container_width=True)

        st.write("▲ **분석 결과:** 장학금 총액이 적은 대학(왼쪽)에서 생활비 대출 비중이 어떻게 나타나는지 확인할 수 있습니다.")

    # --- 두 번째 탭: 설립유형별 분석 ---
    with tab2:
        st.header("2. 국공립 vs 사립대 등록금 및 대출 격차")
        
        # 설립유형별 평균 비교 (그룹화)
        avg_data = df2.groupby("설립별")[["평균등록금(원)", "총_대출_금액", "총_등록금대출_금액"]].mean().reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("설립유형별 평균 등록금")
            fig2 = px.bar(avg_data, x="설립별", y="평균등록금(원)", color="설립별",
                         text_auto='.2s', title="평균 등록금 비교")
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            st.subheader("설립유형별 총 대출 규모")
            fig3 = px.bar(avg_data, x="설립별", y="총_대출_금액", color="설립별",
                         text_auto='.2s', title="평균 대출 규모 비교")
            st.plotly_chart(fig3, use_container_width=True)

        st.success("사립대학교의 높은 등록금이 학생들의 대출 의존도를 높이는 직접적인 원인이 됨을 보여줍니다.")

except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다. GitHub 저장소에 파일이 있는지 확인해주세요.")

# 하단 안내
st.divider()
st.caption("Data Source: 대학알리미 공시 정보 데이터 가공 분석")
