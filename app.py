import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# 1. 페이지 설정 및 데이터 연결
st.set_page_config(page_title="공공자전거 데이터 대시보드", layout="wide")
st.title("🚲 공공자전거 이용현황 시각화 대시보드")

db_path = 'bicycle.db'

# 데이터베이스 존재 확인
if not os.path.exists(db_path):
    st.error(f"🚨 '{db_path}' 파일을 찾을 수 없습니다. DB 파일이 같은 폴더에 있는지 확인해주세요!")
    st.stop()

def run_query(q):
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql(q, conn)

# --- 섹션 1: 이용자 패턴 분석 (Demographics) ---
st.header("1. 이용자 패턴 분석")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("연령대별 이용 비중")
    sql1_1 = "SELECT 연령대코드, SUM(이용건수) as 총이용건수 FROM 이용정보 GROUP BY 연령대코드"
    df1_1 = run_query(sql1_1)
    fig1_1 = px.pie(df1_1, values='총이용건수', names='연령대코드', hole=0.5)
    st.plotly_chart(fig1_1, use_container_width=True)
    st.code(sql1_1, language='sql')
    st.info("💡 인사이트: 특정 연령층(예: 2030)에 편중되어 있다면 해당 타겟 맞춤 마케팅이 유효합니다.")

with col2:
    st.subheader("권종별 이용 패턴")
    sql1_2 = "SELECT 대여구분코드, SUM(이용건수) as 총이용건수 FROM 이용정보 GROUP BY 대여구분코드"
    df1_2 = run_query(sql1_2)
    fig1_2 = px.pie(df1_2, values='총이용건수', names='대여구분코드')
    st.plotly_chart(fig1_2, use_container_width=True)
    st.code(sql1_2, language='sql')
    st.info("💡 인사이트: 정기권 비중이 높으면 출퇴근용, 일일권이 높으면 관광/레저용 도시입니다.")

with col3:
    st.subheader("성별 이용 현황")
    sql1_3 = "SELECT 성별, SUM(이용건수) as 총이용건수 FROM 이용정보 WHERE 성별 != '' GROUP BY 성별"
    df1_3 = run_query(sql1_3)
    fig1_3 = px.bar(df1_3, x='성별', y='총이용건수', color='성별')
    st.plotly_chart(fig1_3, use_container_width=True)
    st.code(sql1_3, language='sql')
    st.info("💡 인사이트: 성별에 따른 이용 격차를 확인하여 공공 서비스의 포용성을 진단합니다.")

st.divider()

# --- 섹션 2: 지역 및 인프라 분석 (Location) ---
st.header("2. 지역 및 인프라 분석")
col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("자치구별 이용량")
    sql2_1 = """
    SELECT b.자치구, SUM(i.이용건수) as 총이용건수 
    FROM 이용정보 i JOIN 대여소 b ON i.대여소번호 = b.대여소번호 
    GROUP BY b.자치구 ORDER BY 총이용건수 DESC
    """
    df2_1 = run_query(sql2_1)
    fig2_1 = px.bar(df2_1, x='총이용건수', y='자치구', orientation='h', color='총이용건수')
    st.plotly_chart(fig2_1, use_container_width=True)
    st.code(sql2_1, language='sql')
    st.info("💡 인사이트: 이용량이 많은 자치구에는 대여소 증설 및 자전거 배치 최적화가 필요합니다.")

with col5:
    st.subheader("운영방식별 선호도")
    sql2_2 = """
    SELECT b.운영방식, SUM(i.이용건수) as 총이용건수 
    FROM 이용정보 i JOIN 대여소 b ON i.대여소번호 = b.대여소번호 
    GROUP BY b.운영방식
    """
    df2_2 = run_query(sql2_2)
    fig2_2 = px.bar(df2_2, x='운영방식', y='총이용건수', color='운영방식')
    st.plotly_chart(fig2_2, use_container_width=True)
    st.code(sql2_2, language='sql')
    st.info("💡 인사이트: QR 등 신규 방식의 이용률이 높다면 구형(LCD) 교체 속도를 높여야 합니다.")

with col6:
    st.subheader("대여소 규모별 이용량")
    sql2_3 = """
    SELECT (LCD + QR) as 거치대수, SUM(이용건수) as 총이용건수 
    FROM 대여소 b JOIN 이용정보 i ON b.대여소번호 = i.대여소번호 
    GROUP BY b.대여소번호
    """
    df2_3 = run_query(sql2_3)
    fig2_3 = px.scatter(df2_3, x='거치대수', y='총이용건수', trendline="ols")
    st.plotly_chart(fig2_3, use_container_width=True)
    st.code(sql2_3, language='sql')
    st.info("💡 인사이트: 거치대 수와 이용량의 상관관계를 통해 적정 대여소 규모를 판단합니다.")

st.divider()

# --- 섹션 3: 이용 효율 및 환경 분석 (Efficiency) ---
st.header("3. 이용 효율 및 환경 분석")
col7, col8, col9 = st.columns(3)

with col7:
    st.subheader("이동거리 분포")
    sql3_1 = "SELECT 이동거리 FROM 이용정보"
    df3_1 = run_query(sql3_1)
    fig3_1 = px.histogram(df3_1, x='이동거리', nbins=30)
    st.plotly_chart(fig3_1, use_container_width=True)
    st.code(sql3_1, language='sql')
    st.info("💡 인사이트: 주된 이동거리 구간을 확인하여 자전거가 주로 '라스트 마일' 수단인지 확인합니다.")

with col8:
    st.subheader("월별 탄소 절감량")
    sql3_2 = "SELECT 대여일자, SUM(탄소량) as 총탄소량 FROM 이용정보 GROUP BY 대여일자"
    df3_2 = run_query(sql3_2)
    fig3_2 = px.line(df3_2, x='대여일자', y='총탄소량', markers=True)
    st.plotly_chart(fig3_2, use_container_width=True)
    st.code(sql3_2, language='sql')
    st.info("💡 인사이트: 자전거 이용을 통한 탄소 절감 효과를 월별로 추적하여 환경 정책 지표로 활용합니다.")

with col9:
    st.subheader("연령대별 평균 운동량")
    sql3_3 = "SELECT 연령대코드, AVG(운동량) as 평균운동량 FROM 이용정보 GROUP BY 연령대코드"
    df3_3 = run_query(sql3_3)
    fig3_3 = px.bar(df3_3, x='연령대코드', y='평균운동량', color='연령대코드')
    st.plotly_chart(fig3_3, use_container_width=True)
    st.code(sql3_3, language='sql')
    st.info("💡 인사이트: 어떤 연령층이 자전거를 가장 열정적으로(운동 목적) 타는지 분석합니다.")