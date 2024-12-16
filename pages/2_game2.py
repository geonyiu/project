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
if "game2_started" not in st.session_state:
    st.session_state.game2_started = False
if "bet_amount" not in st.session_state or st.session_state.bet_amount > st.session_state.balance:
    st.session_state.bet_amount = min(1000, st.session_state.balance)  # 최소값으로 초기화
if "selected_card" not in st.session_state:
    st.session_state.selected_card = None
if "red_card_position" not in st.session_state:
    st.session_state.red_card_position = None

# 로그인 확인
if not st.session_state.ID:
    st.warning("로그인 후 이용 가능합니다.")
    st.stop()

# 왼쪽 사이드바에 사용자 정보 표시
st.sidebar.title("사용자 정보")
st.sidebar.write(f"**ID:** {st.session_state.ID}")
st.sidebar.write(f"**잔액:** {st.session_state.balance:,}원")
st.sidebar.write(f"**수학왕 금액:** {st.session_state.dealer_balance:,}원")

# 페이지 제목
st.title("게임 2: 빨간색 하트 찾기")
st.write("4장의 카드 중 1장은 빨간색 하트, 나머지 3장은 검은색 하트입니다.")
st.write("빨간색 하트를 찾으면 베팅 금액의 2배를 얻고, 틀리면 베팅 금액을 잃습니다.")
st.image("cardheart.png", use_container_width=True)

# 게임비 차감 함수
def deduct_game_fee():
    """게임비 5000원을 차감하고 수학왕 금액에 추가"""
    if st.session_state.balance >= 5000:
        st.session_state.balance -= 5000
        st.session_state.dealer_balance += 5000
        st.session_state.balance_history.append(st.session_state.balance)
        st.session_state.dealer_earnings_history.append(st.session_state.dealer_balance)
        st.session_state.bet_amount = min(1000, st.session_state.balance)  # 초기화
        return True
    else:
        st.error("잔액이 부족하여 게임을 시작할 수 없습니다!")
        return False

# 게임 시작 함수
def start_game():
    """게임 시작 시 상태 초기화 및 게임비 차감"""
    if deduct_game_fee():
        st.session_state.game2_started = True
        st.session_state.red_card_position = random.randint(1, 4)  # 빨간색 하트 카드 위치
        st.success("게임이 시작되었습니다! 베팅 금액을 설정하고 카드를 선택하세요.")
    else:
        st.session_state.game2_started = False

# 게임 진행
if not st.session_state.game2_started:  # 게임이 시작되지 않은 경우
    if st.button("게임 시작 (5,000원 차감)"):
        start_game()
else:
    # 잔액이 부족할 경우
    if st.session_state.balance <= 0:
        st.error("잔액이 부족합니다! 더 이상 게임을 진행할 수 없습니다.")
    else:
        # 베팅 금액 입력
        st.write("### 베팅 금액을 입력하고 카드를 선택하세요.")
        st.session_state.bet_amount = st.number_input(
            "베팅할 금액을 입력하세요 (잔액 내에서):",
            min_value=1000,
            max_value=st.session_state.balance,
            step=1000,
            value=st.session_state.bet_amount,
        )

        # 카드 선택
        st.session_state.selected_card = st.radio(
            "카드를 선택하세요 (1 ~ 4):",
            options=[1, 2, 3, 4],
            index=0 if st.session_state.selected_card is None else st.session_state.selected_card - 1,
        )

        # 카드 결과 확인 버튼
        if st.button("카드 열기"):
            selected_card = st.session_state.selected_card
            red_card_position = st.session_state.red_card_position

            if selected_card == red_card_position:
                winnings = st.session_state.bet_amount * 2
                st.session_state.balance += winnings
                st.success(f"축하합니다! 빨간색 하트를 찾았습니다! {winnings:,}원을 얻으셨습니다!")
            else:
                st.session_state.dealer_balance += st.session_state.bet_amount
                st.session_state.balance -= st.session_state.bet_amount
                st.error(f"아쉽습니다! 선택한 카드는 검은색 하트였습니다. {st.session_state.bet_amount:,}원이 수학왕에게 넘어갑니다.")

            # 소지 금액과 수학왕 수익 변화 기록
            st.session_state.balance_history.append(st.session_state.balance)
            st.session_state.dealer_earnings_history.append(st.session_state.dealer_balance)

            # 결과 표시
            st.write("### 결과")
            st.write(f"**빨간색 하트 위치:** 카드 {red_card_position}")
            st.write(f"**최종 소지금액:** {st.session_state.balance:,}원")
            st.write(f"**수학왕이 번 금액:** {st.session_state.dealer_balance:,}원")

    # 새 게임 버튼 표시
    if st.session_state.selected_card is not None:
        if st.button("새 게임 시작 (5,000원 차감)"):
            start_game()
