import streamlit as st
import random

# 필수 변수 초기화
if "ID" not in st.session_state:
    st.session_state.ID = None
if "balance" not in st.session_state:
    st.session_state.balance = 50000  # 초기 잔액
if "dealer_balance" not in st.session_state:
    st.session_state.dealer_balance = 0
if "balance_history" not in st.session_state:
    st.session_state.balance_history = [50000]  # 초기 소지 금액 기록
if "dealer_earnings_history" not in st.session_state:
    st.session_state.dealer_earnings_history = [0]  # 초기 수학왕 수익 기록
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "bet_amount" not in st.session_state or st.session_state.bet_amount > st.session_state.balance:
    st.session_state.bet_amount = min(1000, st.session_state.balance)  # 최소값으로 초기화
if "choice" not in st.session_state:
    st.session_state.choice = None
if "coin_result" not in st.session_state:
    st.session_state.coin_result = None

# 로그인 확인
if not st.session_state.ID:
    st.warning("로그인 후 이용 가능합니다.")
    st.stop()

# 잔액 부족 확인 함수
def check_balance(required_amount):
    """잔액이 충분한지 확인."""
    if st.session_state.balance < required_amount:
        st.warning(f"잔액이 부족합니다! 최소 {required_amount:,}원이 필요합니다.")
        return False
    return True

# 게임비 차감 함수
def deduct_game_fee():
    """게임비 5000원을 차감."""
    if check_balance(5000):
        st.session_state.balance -= 5000
        st.session_state.dealer_balance += 5000
        st.session_state.balance_history.append(st.session_state.balance)
        st.session_state.dealer_earnings_history.append(st.session_state.dealer_balance)
        st.session_state.bet_amount = min(1000, st.session_state.balance)  # 초기화
        return True
    return False

# 왼쪽 사이드바에 사용자 정보 표시
st.sidebar.title("사용자 정보")
st.sidebar.write(f"**ID:** {st.session_state.ID}")
st.sidebar.write(f"**잔액:** {st.session_state.balance:,}원")
st.sidebar.write(f"**수학왕 금액:** {st.session_state.dealer_balance:,}원")

# 페이지 제목
st.title("게임 1: 동전 앞면/뒷면 게임")
st.write("동전 게임에 오신 것을 환영합니다!")

# 게임 진행
if not st.session_state.game_started:  # 게임이 시작되지 않은 경우
    if st.button("게임 시작 (5,000원 차감)"):
        if deduct_game_fee():
            st.session_state.game_started = True
            st.success("게임이 시작되었습니다! 베팅 금액을 설정하고 동전을 선택하세요.")
else:
    # 잔액이 부족할 경우
    if st.session_state.balance <= 0:
        st.error("잔액이 부족합니다! 더 이상 게임을 진행할 수 없습니다.")
    else:
        # 베팅 금액 입력
        st.session_state.bet_amount = st.number_input(
            "베팅할 금액을 입력하세요:",
            min_value=1000,
            max_value=st.session_state.balance,  # 항상 잔액과 동기화
            step=1000,
            value=st.session_state.bet_amount,
        )

        # 동전 선택
        st.session_state.choice = st.radio(
            "동전의 앞면(Head) 또는 뒷면(Tail)을 선택하세요:",
            ("앞면", "뒷면"),
            index=0 if st.session_state.choice is None else ["앞면", "뒷면"].index(st.session_state.choice),
        )

        # 동전 던지기 버튼
        if st.button("동전 던지기!"):
            if not check_balance(st.session_state.bet_amount):
                st.stop()

            # 동전 결과 생성
            st.session_state.coin_result = random.choice(["앞면", "뒷면"])
            st.write(f"**동전 결과:** {st.session_state.coin_result}")

            # 결과 처리
            if st.session_state.choice == st.session_state.coin_result:
                winnings = st.session_state.bet_amount * 2
                st.session_state.balance += winnings
                st.success(f"축하합니다! 정답을 맞추셨습니다. {winnings:,}원을 얻으셨습니다!")
            else:
                st.session_state.dealer_balance += st.session_state.bet_amount
                st.session_state.balance -= st.session_state.bet_amount
                st.error(f"아쉽습니다! 틀리셨습니다. {st.session_state.bet_amount:,}원이 수학왕에게 넘어갑니다.")

            # 소지 금액과 수학왕 수익 변화 기록
            st.session_state.balance_history.append(st.session_state.balance)
            st.session_state.dealer_earnings_history.append(st.session_state.dealer_balance)

            # 결과 표시
            st.write("### 게임 결과")
            st.write(f"**최종 소지금액:** {st.session_state.balance:,}원")
            st.write(f"**수학왕이 번 금액:** {st.session_state.dealer_balance:,}원")

    # "새 게임 시작" 버튼
    if st.button("새 게임 시작 (5,000원 차감)"):
        if deduct_game_fee():
            st.session_state.game_started = True
            st.success("새 게임이 시작되었습니다! 베팅 금액을 설정하고 동전을 선택하세요.")
            st.session_state.bet_amount = min(1000, st.session_state.balance)  # 새 게임 시작 시 초기화
            st.session_state.choice = None
            st.session_state.coin_result = None
