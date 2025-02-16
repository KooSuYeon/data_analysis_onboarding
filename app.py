import streamlit as st
import pandas as pd
from analysis import (
    get_silver_before_2024, get_final_pass, get_average_among_final_pass,
    get_top_count_and_user_id_by_type, get_average_first_interval,
    get_final_pass_groupby_course, get_diff_between_hanghae_and_nbc,
    get_pass_probability_by_type_and_course, get_suitable_course_depends_on_type
)

# 데이터 불러오기
csv_ = pd.read_csv("dataset.csv")
df = pd.DataFrame(csv_)

# 페이지 설정
st.set_page_config(page_title="취업코칭 대시보드", layout="wide")

# 세션 상태 초기화 (첫 로딩 시에만)
if 'question_count' not in st.session_state:
    st.session_state.question_count = {}

# 제목 중앙 정렬
st.markdown("<h1 style='text-align:center;'>취업코칭 데이터 분석 대시보드</h1>", unsafe_allow_html=True)

# 첫 번째 섹션: 사용자가 선택할 수 있는 질문
st.markdown("<h3 style='text-align:center;'>✨ 원하는 데이터를 선택하세요!</h3>", unsafe_allow_html=True)

# 첫 번째 선택지 (사용자 선택 가능)
user_choice = st.selectbox(
    "원하는 질문을 선택해주세요",
    ["2024년 이전에 취업코칭 서비스 활용한 인원", 
     "최종 합격 인원과 평균 코칭 신청 횟수",
     "이력서 진단/면접 코칭을 가장 많이 활용한 인원",
     "첫 취업코칭 신청 이후, 다음 코칭까지의 평균 기간",
     "course별 최종 합격 인원과 차이점",
     "course 별 합격 시기",
     "type별 course의 최종 합격률"]
)

# 질문 선택 후 카운트 증가
if user_choice:
    if user_choice not in st.session_state.question_count:
        st.session_state.question_count[user_choice] = 0
    st.session_state.question_count[user_choice] += 1

# 선택한 질문 결과 표시
if user_choice == "2024년 이전에 취업코칭 서비스 활용한 인원":
    st.markdown(f"**결과:** {get_silver_before_2024(df)}")
elif user_choice == "최종 합격 인원과 평균 코칭 신청 횟수":
    st.markdown(f"**최종 합격 인원:** {get_final_pass(df)}")
    st.markdown(f"**평균 횟수:** {get_average_among_final_pass(df)}")
elif user_choice == "이력서 진단/면접 코칭을 가장 많이 활용한 인원":
    st.table(get_top_count_and_user_id_by_type(df))
elif user_choice == "첫 취업코칭 신청 이후, 다음 코칭까지의 평균 기간":
    st.markdown(f"**평균 기간:** {get_average_first_interval(df)}")
elif user_choice == "course별 최종 합격 인원과 차이점":
    st.table(get_final_pass_groupby_course(df))
elif user_choice == "course 별 합격 시기":
    st.table(get_diff_between_hanghae_and_nbc(df))
elif user_choice == "type별 course의 최종 합격률":
    st.table(get_pass_probability_by_type_and_course(df))

# 두 번째 섹션: 추천 과정
st.markdown("<h3 style='text-align:center;'>🎯 최적의 코칭 과정 추천</h3>", unsafe_allow_html=True)

user_type = st.radio("원하시는 type을 선택해주세요", ["resume", "interview"])

# 타입 선택 후 카운트 증가
if user_type:
    if user_type not in st.session_state.question_count:
        st.session_state.question_count[user_type] = 0
    st.session_state.question_count[user_type] += 1

# Submit 버튼 생성
if st.button("추천 과정 보기"):
    suitable_course = get_suitable_course_depends_on_type(df, user_type)
    st.markdown(f"**추천 과정:** {suitable_course}")

# 다른 데이터 섹션들을 카드 형식으로 표시 (글자 크기 줄이기)
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("📊 7월 3일~12월 31일까지, 인텔리픽의 취업코칭 서비스를 한 번 이상 활용한 인원은 몇 명인가요?")
    st.markdown(f"**결과:** {get_silver_before_2024(df)}")
    st.markdown(f"👁 조회 횟수: {st.session_state.question_count.get('2024년 이전에 취업코칭 서비스 활용한 인원', 0)}회")

with col2:
    st.subheader("🏆 최종 합격 인원과, 최종 합격 그룹의 이력서 진단 / 면접 코칭 신청 평균 횟수는?")
    st.markdown(f"**최종 합격 인원:** {get_final_pass(df)}")
    st.markdown(f"**평균 횟수:** {get_average_among_final_pass(df)}")
    st.markdown(f"👁 조회 횟수: {st.session_state.question_count.get('최종 합격 인원과 평균 코칭 신청 횟수', 0)}회")

with col3:
    st.subheader("📊 이력서 진단 + 면접 코칭을 가장 많이 활용한 인원의 각 횟수는 몇 번이며, 해당 인원의 id 값은?")
    st.table(get_top_count_and_user_id_by_type(df))
    st.markdown(f"👁 조회 횟수: {st.session_state.question_count.get('이력서 진단/면접 코칭을 가장 많이 활용한 인원', 0)}회")

with col4:
    st.subheader("⏳ 첫 취업코칭 신청 이후, 다음 코칭을 받기까지의 평균 기간은?")
    st.markdown(f"**평균 기간:** {get_average_first_interval(df)}")
    st.markdown(f"👁 조회 횟수: {st.session_state.question_count.get('첫 취업코칭 신청 이후, 다음 코칭까지의 평균 기간', 0)}회")

# 두 번째 줄
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.subheader("🎓 course별 최종 합격 인원과 차이점은?")
    st.table(get_final_pass_groupby_course(df))
    st.markdown(f"👁 조회 횟수: {st.session_state.question_count.get('course별 최종 합격 인원과 차이점', 0)}회")

with col6:
    st.subheader("📅 course 별 합격 시기 분석")
    st.table(get_diff_between_hanghae_and_nbc(df))
    st.markdown(f"👁 조회 횟수: {st.session_state.question_count.get('course 별 합격 시기', 0)}회")

with col7:
    st.subheader("📈 type별 course의 최종 합격률")
    st.table(get_pass_probability_by_type_and_course(df))
    st.markdown(f"👁 조회 횟수: {st.session_state.question_count.get('type별 course의 최종 합격률', 0)}회")
