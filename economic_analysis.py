import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import fredapi as fa
import seaborn as sns
from fredapi import Fred

# FRED API 키 설정
fred = Fred(api_key=st.secrets["fred_api_key"])

# 주요 지표 설정
indicators = {
    "TLT": "^TYX",  # 30-year Treasury Yield
    "DXY": "DX-Y.NYB",  # US Dollar Index
    "SPY": "SPY",  # S&P 500 ETF
    "QQQ": "QQQ",  # Nasdaq 100 ETF
    "VIX": "^VIX",  # Volatility Index
}

# FRED 데이터 시리즈 설정
fred_series = {
    "Fed_Reserve_Balances": "WRESBAL",
    "Fed_Total_Assets": "WALCL",
    "Treasury_Cash": "WTREGEN",
    "Reverse_Repo": "RRPONTSYD",
}

# 데이터 가져오기
start_date = "2020-01-01"
end_date = datetime.now().strftime("%Y-%m-%d")


@st.cache_data
def load_data():
    data = pd.DataFrame()
    for name, ticker in indicators.items():
        df = yf.download(ticker, start=start_date, end=end_date)["Adj Close"]
        data[name] = df
    for name, series in fred_series.items():
        df = fred.get_series(
            series, observation_start=start_date, observation_end=end_date
        )
        data[name] = df
    return data.ffill().bfill()


data = load_data()

# 데이터 정규화
normalized_data = data / data.iloc[0] * 100

st.title("Economic Indicators Analysis and Investment Strategy")

# 정규화된 데이터 시각화
st.subheader("Normalized Economic Indicators Trend (2020-Present)")
fig, ax = plt.subplots(figsize=(15, 10))
for column in normalized_data.columns:
    ax.plot(normalized_data.index, normalized_data[column], label=column)
ax.set_xlabel("Date")
ax.set_ylabel("Normalized Value (Starting Point = 100)")
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
ax.grid(True)
plt.tight_layout()
st.pyplot(fig)

st.write(
    """
### 그래프 해석:
1. 코로나19 이후 Fed의 총자산과 지급준비금이 급격히 증가했으며, 이는 대규모 양적완화 정책을 반영합니다.
2. 역레포 시장의 급격한 성장은 시중 유동성 증가와 연관이 있습니다.
3. S&P 500(SPY)과 나스닥 100(QQQ)은 전반적으로 상승 추세를 보이고 있으나, 변동성이 큽니다.
4. 달러 인덱스(DXY)는 2022년 중반 이후 강세를 보이다가 최근 약세로 전환되었습니다.
5. VIX 지수는 주기적으로 스파이크를 보이며, 시장의 불안정성을 나타냅니다.
"""
)

# 상관관계 분석
st.subheader("Correlation Between Indicators")
correlation = data.pct_change().corr()
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(correlation, annot=True, cmap="coolwarm", vmin=-1, vmax=1, center=0, ax=ax)
plt.title("Correlation Heatmap of Economic Indicators")
st.pyplot(fig)

st.write(
    """
### 상관관계 해석:
1. Fed의 총자산과 지급준비금은 높은 양의 상관관계를 보입니다.
2. S&P 500과 나스닥 100은 매우 강한 양의 상관관계를 가집니다.
3. VIX 지수는 대부분의 지표와 음의 상관관계를 보이며, 특히 주식 시장과 강한 음의 상관관계를 갖습니다.
4. 달러 인덱스는 주식 시장과 약한 음의 상관관계를 보입니다.
"""
)


st.subheader("Monthly Investment Strategy (Oct 2024 - Mar 2025)")

strategy = """
### 월별 ETF 투자 전략 (8천만원 기준):

1. 2024년 10월:
   - KODEX 미국채10년물(H): 20% (16,000,000원)
   - KODEX 미국달러선물: 15% (12,000,000원)
   - KODEX 인버스: 10% (8,000,000원)
   - KODEX 미국S&P500TR: 20% (16,000,000원)
   - Invesco QQQ Trust ETF: 20% (16,000,000원)
   - TIGER 글로벌리튬&2차전지SOLACTIVE: 15% (12,000,000원)
   
   근거: 양적 긴축 종료 예상에 따른 주식 시장 반등 기대, 달러 강세 대비

2. 2024년 11월:
   - KODEX 미국채10년물(H): 15% (12,000,000원)
   - KODEX 미국달러선물: 15% (12,000,000원)
   - KODEX 인버스: 5% (4,000,000원)
   - KODEX 미국S&P500TR: 25% (20,000,000원)
   - Invesco QQQ Trust ETF: 25% (20,000,000원)
   - TIGER 글로벌리튬&2차전지SOLACTIVE: 15% (12,000,000원)
   
   근거: 주식 시장 모멘텀 유지 예상, 안전자산 비중 소폭 감소

3. 2024년 12월:
   - KODEX 미국채10년물(H): 15% (12,000,000원)
   - KODEX 미국달러선물: 10% (8,000,000원)
   - KODEX 골드선물(H): 10% (8,000,000원)
   - KODEX 미국S&P500TR: 25% (20,000,000원)
   - Invesco QQQ Trust ETF: 25% (20,000,000원)
   - TIGER 글로벌리튬&2차전지SOLACTIVE: 15% (12,000,000원)
   
   근거: 연말 랠리 기대, 골드 추가로 경제 불확실성 대비

4. 2025년 1월:
   - KODEX 미국채10년물(H): 20% (16,000,000원)
   - KODEX 미국달러선물: 10% (8,000,000원)
   - KODEX 골드선물(H): 10% (8,000,000원)
   - KODEX 미국S&P500TR: 20% (16,000,000원)
   - Invesco QQQ Trust ETF: 20% (16,000,000원)
   - TIGER 글로벌리튬&2차전지SOLACTIVE: 20% (16,000,000원)
   
   근거: 새해 불확실성 대비 안전자산 비중 증가, 성장 산업 비중 확대

5. 2025년 2월:
   - KODEX 미국채10년물(H): 25% (20,000,000원)
   - KODEX 미국달러선물: 10% (8,000,000원)
   - KODEX 골드선물(H): 15% (12,000,000원)
   - KODEX 미국S&P500TR: 15% (12,000,000원)
   - Invesco QQQ Trust ETF: 15% (12,000,000원)
   - TIGER 글로벌리튬&2차전지SOLACTIVE: 20% (16,000,000원)
   
   근거: 경기 둔화 우려에 따른 안전자산 비중 증가

6. 2025년 3월:
   - KODEX 미국채10년물(H): 30% (24,000,000원)
   - KODEX 미국달러선물: 10% (8,000,000원)
   - KODEX 골드선물(H): 15% (12,000,000원)
   - KODEX 미국S&P500TR: 15% (12,000,000원)
   - Invesco QQQ Trust ETF: 15% (12,000,000원)
   - TIGER 글로벌리튬&2차전지SOLACTIVE: 15% (12,000,000원)
   
   근거: 금리 인하 기대감에 따른 채권 비중 증가, 주식 시장 변동성 대비

주의: 이 전략은 현재 시점의 예측을 바탕으로 한 것이며, 실제 시장 상황에 따라 유연하게 조정해야 합니다. 
또한, 개인의 위험 선호도와 투자 목표에 따라 비중을 조절해야 합니다.
"""

st.write(strategy)

st.write(
    """
### 투자 전략 근거:
1. 연준의 양적 긴축이 2024년 상반기에 종료될 것으로 예상됨에 따라, 하반기부터는 시장 유동성 개선 기대
2. KODEX 미국채10년물(H)를 통해 안정적인 수익과 금리 변동 대비
3. KODEX 미국달러선물과 KODEX 골드선물(H)을 통해 경제 불확실성에 대한 헤지
4. KODEX 미국S&P500TR과 Invesco QQQ Trust ETF를 통해 미국 주식 시장의 성장에 대한 노출
5. TIGER 글로벌리튬&2차전지SOLACTIVE를 통해 미래 성장 산업에 대한 투자
6. 경제 상황과 시장 분위기에 따라 안전자산과 위험자산의 비중을 조절
7. 정기적인 리밸런싱을 통해 위험 관리 및 수익 최적화
"""
)

# %%
