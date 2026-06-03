import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="대학생 장학금 사각지대 분석", layout="wide")

# 제목 부분
st.title("📊 국가장학금 사각지대 및 대출 의존도 분석")
st.markdown("---")

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    df1 = pd.read_csv("Q1_사각지대_생활비대출_분석용.csv")
    df2 = pd.read_csv("Q2_설립유형별_부담격차_대출_분석용.csv")
    return df1, df2

try:
    df1, df2 = load_data()

    # 탭 생성
    tab1, tab2 = st.tabs(["💡 소득분위 사각지대 분석", "🏛️ 설립유형별 부담 격차"])

    with tab1:
        st.header("1. 장학금 사각지대와 생활비 대출의 상관관계")
        
        # 핵심 지표 카드 생성
        col1, col2, col3 = st.columns(3)
        col1.metric("분석 대상 대학", f"{len(df1):,d}개")
        col2.metric("평균 생활비 대출", f"{int(df1['총_생활비대출_금액'].mean()):,d}원")
        col3.metric("대출 규모 최대 학교", df1.loc[df1['총_생활비대출_금액'].idxmax(), '학교명'])
        
        st.write("") # 간격
        
        # 그래프 설정 (팀원 디자인과 조화를 위해 파란색 계열 사용)
        fig1 = px.scatter(df1, 
                         x="교외장학금 국가", 
                         y="총_생활비대출_금액",
                         hover_name="학교명",
                         size="총_생활비대출_금액",
                         color="총_생활비대출_금액",
                         color_continuous_scale="Blues",
                         title="국가장학금 수혜액 vs 생활비 대출 규모")
        st.plotly_chart(fig1, use_container_width=True)
        
        with st.expander("데이터 상세 보기"):
            st.dataframe(df1, use_container_width=True)

    with tab2:
        st.header("2. 국공립 vs 사립대 등록금 및 대출 격차")
        
        avg_data = df2.groupby("설립별")[["평균등록금(원)", "총_대출_금액"]].mean().reset_index()
        
        col_a, col_b = st.columns(2)
        with col_a:
            fig2 = px.bar(avg_data, x="설립별", y="평균등록금(원)", 
                         title="설립유형별 평균 등록금",
                         color="설립별",
                         text_auto='.2s')
            st.plotly_chart(fig2, use_container_width=True)
            
        with col_b:
            fig3 = px.bar(avg_data, x="설립별", y="총_대출_금액", 
                         title="설립유형별 평균 총 대출 규모",
                         color="설립별",
                         text_auto='.2s')
            st.plotly_chart(fig3, use_container_width=True)
            
        st.subheader("대학별 상세 데이터")
        st.dataframe(df2, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
