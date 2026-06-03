import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="대학생 장학금 사각지대 분석", layout="wide")

# 제목 부분
st.title("📊 국가장학금 사각지대 및 대출 의존도 분석")

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    # 파일 이름을 정확히 대조하세요. GitHub에 올라간 파일 이름과 완전히 똑같아야 합니다.
    df1 = pd.read_csv("Q1_사각지대_생활비대출_분석용.csv")
    df2 = pd.read_csv("Q2_설립유형별_부담격차_대출_분석용.csv")
    return df1, df2

try:
    df1, df2 = load_data()

    # 탭 생성
    tab1, tab2 = st.tabs(["💡 소득분위 사각지대 분석", "🏛️ 설립유형별 부담 격차"])

    with tab1:
        st.header("1. 장학금 사각지대와 생활비 대출의 상관관계")
        # 데이터가 잘 들어왔는지 확인하기 위해 상단 5줄 출력
        st.dataframe(df1.head()) 
        
        fig1 = px.scatter(df1, 
                         x="교외장학금 국가", 
                         y="총_생활비대출_금액",
                         hover_name="학교명",
                         title="국가장학금 수혜액 vs 생활비 대출 규모")
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        st.header("2. 국공립 vs 사립대 등록금 및 대출 격차")
        st.dataframe(df2.head())
        
        avg_data = df2.groupby("설립별")[["평균등록금(원)", "총_대출_금액"]].mean().reset_index()
        fig2 = px.bar(avg_data, x="설립별", y="평균등록금(원)", title="평균 등록금 비교")
        st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"에러가 발생했습니다: {e}")
    st.write("CSV 파일 이름이 코드에 적힌 것과 일치하는지, 파일이 같은 폴더에 있는지 확인해주세요.")
