import streamlit as st
import random

# 딜러 금액 초기화
if "dealer_balance" not in st.session_state:
    st.session_state.dealer_balance = 0

# 사용자 금액 변화 기록 초기화
if "balance_history" not in st.session_state:
    st.session_state.balance_history = [50000]  # 초기 소지 금액 기록
if "dealer_earnings_history" not in st.session_state:
    st.session_state.dealer_earnings_history = [0]  # 초기 수학왕 수익 기록

# 게임 상태 초기화
if "game4_started" not in st.session_state:
    st.session_state.game4_started = False
if "chosen_door" not in st.session_state:
    st.session_state.chosen_door = None
if "opened_door" not in st.session_state:
    st.session_state.opened_door = None
if "final_choice" not in st.session_state:
    st.session_state.final_choice = None
if "car_door" not in st.session_state:
    st.session_state.car_door = None

# 로그인 확인
if "ID" not in st.session_state or "balance" not in st.session_state:
    st.warning("로그인 후 이용 가능합니다.")
    st.stop()

# 왼쪽 사이드바에 사용자 정보 표시
st.sidebar.title("사용자 정보")
st.sidebar.write(f"**ID:** {st.session_state.ID}")
st.sidebar.write(f"**잔액:** {st.session_state.balance:,}원")
st.sidebar.write(f"**수학왕 금액:** {st.session_state.dealer_balance:,}원")

# 페이지 제목
st.title("게임 4: 몬티 홀 문제")
st.write("세 개의 문 중 하나를 선택하세요! 자동차를 찾으면 10,000원을 얻고, 틀리면 8,000원을 잃습니다.")
st.image("car.png", use_container_width=True)

# 게임비 차감 함수
def deduct_game_fee():
    """게임비 5000원을 차감하고 딜러 금액에 추가"""
    if st.session_state.balance >= 5000:
        st.session_state.balance -= 5000
        st.session_state.dealer_balance += 5000
        st.session_state.balance_history.append(st.session_state.balance)
        st.session_state.dealer_earnings_history.append(st.session_state.dealer_balance)
        return True
    else:
        st.error("잔액이 부족하여 게임을 시작할 수 없습니다!")
        return False

# 게임 시작 함수
def start_game():
    """게임을 시작하면서 게임비를 차감하고 상태를 초기화"""
    if deduct_game_fee():  # 게임비 차감
        st.session_state.game4_started = True
        st.session_state.car_door = random.randint(1, 3)  # 자동차가 있는 문 설정
        st.session_state.chosen_door = None
        st.session_state.opened_door = None
        st.session_state.final_choice = None
        st.success("게임이 시작되었습니다! 문을 선택하세요.")
    else:
        st.session_state.game4_started = False  # 잔액 부족 시 게임 시작 불가

# 게임 진행
if not st.session_state.game4_started:  # 게임이 시작되지 않은 경우
    if st.button("게임 시작 (5,000원 차감)"):
        start_game()
else:
    # 첫 번째 선택
    st.write("### 첫 번째 선택:")
    chosen_door = st.radio(
        "문을 선택하세요:",
        options=[1, 2, 3],
        index=0 if st.session_state.chosen_door is None else st.session_state.chosen_door - 1,
        key="initial_choice",
    )
    if st.button("선택 확인") and st.session_state.chosen_door is None:
        st.session_state.chosen_door = chosen_door
        # 사회자가 염소가 있는 문을 연다
        doors = [1, 2, 3]
        doors.remove(st.session_state.chosen_door)
        if st.session_state.car_door in doors:
            doors.remove(st.session_state.car_door)
        st.session_state.opened_door = random.choice(doors)
        st.success(f"문 {st.session_state.opened_door}번은 염소가 있습니다!")

    # 최종 선택
    if st.session_state.opened_door is not None:
        st.write("### 최종 선택:")
        remaining_doors = [1, 2, 3]
        remaining_doors.remove(st.session_state.opened_door)
        final_choice = st.radio(
            "최종 선택을 하세요 (문 변경 가능):",
            options=remaining_doors,
            index=0 if st.session_state.final_choice is None else remaining_doors.index(st.session_state.final_choice),
            key="final_choice_widget",
        )
        if st.button("최종 선택 확인"):
            st.session_state.final_choice = final_choice
            # 결과 확인
            if st.session_state.final_choice == st.session_state.car_door:
                st.session_state.balance += 10000
                st.session_state.balance_history.append(st.session_state.balance)
                st.success(f"축하합니다! 자동차를 찾았습니다! 10,000원을 얻으셨습니다!")
            else:
                st.session_state.balance -= 8000
                st.session_state.dealer_balance += 8000
                st.session_state.balance_history.append(st.session_state.balance)
                st.session_state.dealer_earnings_history.append(st.session_state.dealer_balance)
                st.error(f"아쉽습니다! 선택한 문에 염소가 있었습니다. 8,000원이 수학왕에게 넘어갑니다.")

            # 결과 표시
            st.write(f"**자동차가 있는 문:** {st.session_state.car_door}번")
            st.write(f"**최종 소지금액:** {st.session_state.balance:,}원")
            st.write(f"**수학왕이 번 금액:** {st.session_state.dealer_balance:,}원")

    # 새 게임 버튼
    if st.session_state.final_choice is not None:
        if st.button("새 게임 시작 (5,000원 차감)"):
            start_game()
