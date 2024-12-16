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
if "game3_started" not in st.session_state:
    st.session_state.game3_started = False
if "bet_amount" not in st.session_state or st.session_state.bet_amount > st.session_state.balance:
    st.session_state.bet_amount = min(1000, st.session_state.balance)  # 최소값으로 초기화
if "draw_results" not in st.session_state:
    st.session_state.draw_results = []

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
st.title("게임 3: 주머니 공 뽑기")
st.write("주머니 2개에 각각 검은 공 2개와 흰 공 1개가 들어 있습니다.")
st.write("두 주머니에서 모두 검은 공을 뽑으면 베팅 금액의 2배를 얻고, 그렇지 않으면 베팅 금액을 잃습니다.")
st.image("gong.png", use_container_width=True)

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
    """게임을 시작하면서 게임비를 차감하고 상태를 초기화"""
    if deduct_game_fee():  # 게임비 차감
        st.session_state.game3_started = True
        st.session_state.draw_results = []  # 공 뽑기 결과 초기화
        st.success("게임이 시작되었습니다! 베팅 금액을 설정하고 결과를 확인하세요.")
    else:
        st.session_state.game3_started = False  # 잔액 부족 시 게임 시작 불가

# 공 뽑기 로직
def draw_balls():
    """두 주머니에서 공을 뽑아 결과를 반환"""
    results = []
    for i in range(2):  # 두 주머니
        bag = ["검은 공", "검은 공", "흰 공"]  # 각 주머니의 공 구성
        results.append(random.choice(bag))  # 무작위로 공 뽑기
    return results

# 게임 진행
if not st.session_state.game3_started:  # 게임이 시작되지 않은 경우
    if st.session_state.balance < 5000:
        st.error("잔액이 부족하여 게임을 시작할 수 없습니다.")
    elif st.button("게임 시작 (5,000원 차감)"):
        start_game()  # 게임 시작 함수 호출
else:
    # 잔액이 부족할 경우
    if st.session_state.balance <= 0:
        st.error("잔액이 부족합니다! 더 이상 게임을 진행할 수 없습니다.")
    else:
        # 베팅 금액 입력
        st.write("### 베팅 금액을 입력하세요.")
        st.session_state.bet_amount = st.number_input(
            "베팅할 금액을 입력하세요 (잔액 내에서):",
            min_value=1000,
            max_value=st.session_state.balance,
            step=1000,
            value=st.session_state.bet_amount,
        )

        # 결과 확인 버튼
        if st.button("공 뽑기 결과 확인"):
            if st.session_state.bet_amount > st.session_state.balance:
                st.error("베팅 금액이 잔액보다 많습니다! 베팅 금액을 줄이세요.")
            else:
                st.session_state.draw_results = draw_balls()  # 두 주머니에서 공 뽑기
                st.write("### 결과:")
                st.write(f"**첫 번째 주머니:** {st.session_state.draw_results[0]}")
                st.write(f"**두 번째 주머니:** {st.session_state.draw_results[1]}")

                # 결과 처리
                if all(ball == "검은 공" for ball in st.session_state.draw_results):
                    winnings = st.session_state.bet_amount * 2
                    st.session_state.balance += winnings
                    st.session_state.balance_history.append(st.session_state.balance)
                    st.success(f"축하합니다! 두 주머니에서 모두 검은 공을 뽑았습니다! {winnings:,}원을 얻으셨습니다!")
                else:
                    st.session_state.dealer_balance += st.session_state.bet_amount
                    st.session_state.balance -= st.session_state.bet_amount
                    st.session_state.balance_history.append(st.session_state.balance)
                    st.session_state.dealer_earnings_history.append(st.session_state.dealer_balance)
                    st.error(f"아쉽습니다! 주머니에서 흰 공이 나왔습니다. {st.session_state.bet_amount:,}원이 수학왕에게 넘어갑니다.")

                # 결과 표시
                st.write(f"**최종 소지금액:** {st.session_state.balance:,}원")
                st.write(f"**수학왕이 번 금액:** {st.session_state.dealer_balance:,}원")

    # "새 게임 시작" 버튼은 게임이 한 번 이상 진행된 후에만 표시
    if st.session_state.draw_results:
        if st.button("새 게임 시작 (5,000원 차감)"):
            start_game()
