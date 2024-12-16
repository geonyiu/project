import streamlit as st
import pandas as pd

st.set_page_config(page_title="도박중독 예방 플랫폼", layout="centered")

st.title("나에게 도박도박 걸어온 확률과 수학")
st.image("image.png", use_container_width=True)

# CSV 파일 불러오기
try:
    data = pd.read_csv("members.csv")
except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다. `members.csv` 파일을 확인하세요.")
    st.stop()

# 로그인 상태 변수 초기화
if "ID" not in st.session_state:
    st.session_state.ID = ""
if "PW" not in st.session_state:
    st.session_state.PW = ""
if "login_success" not in st.session_state:
    st.session_state.login_success = False
if "balance" not in st.session_state:
    st.session_state.balance = 0

# 로그인 상태에 따라 화면 분기
if not st.session_state.login_success:
    st.subheader("로그인")
    with st.form("login_form", clear_on_submit=True):
        ID = st.text_input("ID", placeholder="아이디를 입력하세요")
        PW = st.text_input("Password", type="password", placeholder="비밀번호를 입력하세요")
        submit_button = st.form_submit_button("로그인")

    if submit_button:
        if not ID or not PW:
            st.warning("ID와 비밀번호를 모두 입력해주세요.")
        else:
            # 데이터 정리
            data["ID"] = data["ID"].astype(str).str.strip()
            data["PW"] = data["PW"].astype(str).str.strip()
            ID = ID.strip()
            PW = PW.strip()

            # 로그인 체크
            user = data[(data["ID"] == ID) & (data["PW"] == PW)]
            if not user.empty:
                st.session_state.login_success = True
                st.session_state.ID = ID  # 로그인 성공 시 ID 유지
                st.session_state.PW = ""  # 비밀번호 초기화
                st.session_state.balance = 50000  # 초기 게임 머니 지급
                st.success(f"{ID}님 환영합니다!")
            else:
                st.warning("아이디 또는 비밀번호가 일치하지 않습니다.")
else:
    st.sidebar.title("게임 선택")
    st.sidebar.success(f"환영합니다, {st.session_state.ID}님!")
    st.sidebar.write(f"잔액: {st.session_state.balance}원")

    # 메인 화면
    st.subheader("도박 중독 예방 플랫폼에 오신 것을 환영합니다.")
    st.write("게임을 즐기기 전에 도박 중독 예방에 대한 정보를 확인하세요.")
    st.info("좌측 상단 메뉴에서 게임 페이지를 선택할 수 있습니다.")
