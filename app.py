import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 기본 설정
st.set_page_config(page_title="명동 상품권 통합 시세", layout="wide", page_icon="🎫")

# 시세 데이터 (이 부분에 나중에 크롤링 로직을 연결합니다)
def fetch_data():
    data = [
        {"매장": "우천사", "롯데": 96700, "신세계": 97100, "현대": 97050, "전화": "02-779-8589", "주소": "남대문로 64-1"},
        {"매장": "명인상품권", "롯데": 96800, "신세계": 97100, "현대": 97000, "전화": "02-318-3526", "주소": "남대문로7길 29"},
        {"매장": "중앙상품권", "롯데": 96750, "신세계": 97200, "현대": 97100, "전화": "02-774-4554", "주소": "명동8나길 49"},
        {"매장": "베스트상품권", "롯데": 96650, "신세계": 97000, "현대": 97150, "전화": "02-755-3007", "주소": "퇴계로 108"},
        {"매장": "우현상품권", "롯데": 96600, "신세계": 97100, "현대": 97050, "전화": "02-778-8504", "주소": "남대문로 60"},
    ]
    return pd.DataFrame(data)

df = fetch_data()

# --- 화면 구현 ---
st.title("🏙️ 명동 상품권 실시간 통합 시세")
st.info("명동 주요 매장의 시세를 실시간으로 비교하여 최적의 거래처를 추천합니다.")

# 1. 전체 요약 (Best Pick)
st.subheader("🏆 종목별 최고가 매장")
c1, c2, c3 = st.columns(3)
c1.metric("롯데 최고가", f"{df['롯데'].max():,.0}원", df.loc[df['롯데'].idxmax(), '매장'])
c2.metric("신세계 최고가", f"{df['신세계'].max():,.0}원", df.loc[df['신세계'].idxmax(), '매장'])
c3.metric("현대 최고가", f"{df['현대'].max():,.0}원", df.loc[df['현대'].idxmax(), '매장'])

st.divider()

# 2. 통합 비교표
st.subheader("📊 전체 매장 시세 비교 (10만원권 기준)")
# 최고가 하이라이트 적용
st.dataframe(df.style.highlight_max(axis=0, subset=['롯데', '신세계', '현대'], color='#D4EDDA'), use_container_width=True)

# 3. 매장별 상세 정보
st.subheader("📍 매장별 상세 정보")
for i in range(0, len(df), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(df):
            row = df.iloc[i + j]
            with cols[j]:
                with st.expander(f"🏢 {row['매장']}"):
                    st.write(f"📞 **전화:** {row['전화']}")
                    st.write(f"🏠 **주소:** {row['주소']}")
                    st.write(f"💰 **롯데:** {row['롯데']:,.0} | **신세계:** {row['신세계']:,.0} | **현대:** {row['현대']:,.0}")

# 4. 계산기 (사이드바)
st.sidebar.header("🧮 실시간 환전 계산기")
target_val = st.sidebar.number_input("보유 상품권 총액", value=1000000, step=100000)
target_shop = st.sidebar.selectbox("방문할 매장 선택", df['매장'])
selected_rate = df[df['매장'] == target_shop]['롯데'].values[0] / 100000
st.sidebar.success(f"예상 현금 수령액: {target_val * selected_rate:,.0}원")