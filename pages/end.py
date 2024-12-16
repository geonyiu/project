import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 학습자의 게임 기록이 있는지 확인
if "balance_history" not in st.session_state or len(st.session_state.balance_history) == 0:
    st.warning("아직 기록된 게임 데이터가 없습니다. 게임을 진행해 주세요!")
    st.stop()

if "dealer_earnings_history" not in st.session_state:
    st.session_state.dealer_earnings_history = [0]

# 데이터 길이 맞추기
while len(st.session_state.dealer_earnings_history) < len(st.session_state.balance_history):
    st.session_state.dealer_earnings_history.append(st.session_state.dealer_balance)

# 페이지 제목
st.title("사용자 소지 금액과 수학왕 수익 변화")
st.write("아래는 각 게임 진행 상황에 따라 사용자 소지 금액과 수학왕이 번 돈의 변화를 보여줍니다.")

# 데이터프레임 생성
df = pd.DataFrame({
    "게임 번호": list(range(1, len(st.session_state.balance_history) + 1)),
    "소지 금액": st.session_state.balance_history,
    "수학왕 수익": st.session_state.dealer_earnings_history,
})

# 꺾은선 그래프 생성 (Plotly)
fig = go.Figure()

# 사용자 소지 금액 꺾은선
fig.add_trace(go.Scatter(
    x=df["게임 번호"],
    y=df["소지 금액"],
    mode='lines+markers',
    name='소지 금액',
    line=dict(color='blue', width=2),
    marker=dict(size=6)
))

# 수학왕 수익 꺾은선
fig.add_trace(go.Scatter(
    x=df["게임 번호"],
    y=df["수학왕 수익"],
    mode='lines+markers',
    name='수학왕 수익',
    line=dict(color='red', width=2, dash='dash'),
    marker=dict(size=6)
))

# 그래프 레이아웃 설정
fig.update_layout(
    title="사용자 소지 금액 vs 수학왕 수익 변화",
    xaxis=dict(title="게임 번호"),
    yaxis=dict(
        title="금액 (원)",
        tickformat=",",  # 세로축 숫자에 쉼표 추가 (예: 50000 → 50,000)
        ticksuffix="원",  # 숫자 뒤에 '원' 추가
    ),
    legend=dict(title="범례", x=0.1, y=1.1, orientation="h"),
    template="plotly_white"
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 데이터 요약
st.write(f"**최종 소지 금액:** {st.session_state.balance:,}원")
st.write(f"**수학왕이 번 금액:** {st.session_state.dealer_balance:,}원")


# 학생 소감 입력1
st.write("### 1. 어떤 게임이 여러분에게 가장 유리할까요?")
feedback = st.text_area(
    "어떤 게임이 유리할까?",
    placeholder="여기에 작성하고 모둠별로 이야기를 나눠봅시다. 예: game1은 승리 확률이 00으로 가장 유리합니다.",
    height=150,
)


# 학생 소감 입력
st.write("### 2.게임을 하고 그래프를 보니 어떤 생각이 드셨나요?")
feedback = st.text_area(
    "소감을 입력해주세요:",
    placeholder="여기에 소감을 작성하세요. 예: 처음엔 재밌었지만 수학왕에게 돈을 다 잃어서 슬펐어요!",
    height=150,
)

# 소감 저장 (필요 시)
if st.button("소감 제출"):
    if feedback.strip():
        st.success("소감 제출 완료! 오늘 수업도 수학적 배움이 충분했나요?? :)")
    else:
        st.warning("소감을 입력해주세요!")
