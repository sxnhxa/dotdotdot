import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import random

# 1. 페이지 설정 및 성수동 다크 테마 CSS
st.set_page_config(page_title="DOTDOTDOT.SEOUL.2", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* 전체 배경 및 폰트 */
    .main { background-color: #000000; }
    html, body, [class*="css"]  {
        font-family: 'JetBrains Mono', monospace;
        color: #00FF41; /* 기본 포인트 컬러 */
    }
    
    /* 상단 티커 애니메이션 */
    .ticker-wrapper {
        width: 100%; overflow: hidden; background: #111;
        padding: 10px 0; border-bottom: 1px solid #333;
    }
    .ticker {
        display: inline-block; white-space: nowrap;
        animation: marquee 30s linear infinite;
        font-size: 16px; font-weight: bold;
    }
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    
    /* 성수동 스타일 버튼 */
    .stButton>button {
        width: 100%; border-radius: 0px;
        background-color: transparent; border: 2px solid #00FF41;
        color: #00FF41; height: 50px; font-size: 20px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #00FF41 !important; color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 메뉴별 고유 컬러 설정 (Seed.sql의 메뉴 리스트 참고)
menu_config = {
    "AMERICANO": {"color": "#4B3621", "rgba": "rgba(75, 54, 33, 0.3)"},
    "CAFE LATTE": {"color": "#C2B280", "rgba": "rgba(194, 178, 128, 0.3)"},
    "EINSPANNER": {"color": "#FFFFFF", "rgba": "rgba(255, 255, 255, 0.3)"},
    "STRAWBERRY LATTE": {"color": "#FF69B4", "rgba": "rgba(255, 105, 180, 0.3)"},
    "COLD BREW": {"color": "#008080", "rgba": "rgba(0, 128, 128, 0.3)"}
}
menus = list(menu_config.keys())

# 3. 실시간 가상 데이터 생성 로직
def get_stock_data(menu_name):
    # 메뉴 이름에 따라 다른 패턴을 보이도록 랜덤 시드 고정
    np.random.seed(len(menu_name))
    prices = np.random.randn(50).cumsum() + 100
    dates = pd.date_range(datetime.now().replace(hour=9, minute=0), periods=50, freq='5min')
    return pd.DataFrame({'Date': dates, 'Price': prices})

# 4. 상단 티커 (주요 지수)
ticker_items = [f"{m} {np.random.uniform(-5, 5):+.2f}%" for m in menus]
st.markdown(f"<div class='ticker-wrapper'><div class='ticker'>{' | '.join(ticker_items)}</div></div>", unsafe_allow_html=True)

# 5. 헤더 섹션
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📟 DOTDOTDOT TRADING VIEW")
    st.caption("LIVE MARKET DATA BASED ON CAFE LOGS")
with col2:
    st.metric(label="MARKET STATUS", value="OPEN", delta="Stable")

st.markdown("---")

# 6. 메인 차트 섹션
selected_menu = st.selectbox("SELECT ASSET (MENU)", menus)
df = get_stock_data(selected_menu)

# 현재 선택된 메뉴의 색상 가져오기
current_color = menu_config[selected_menu]["color"]
current_rgba = menu_config[selected_menu]["rgba"]

# Plotly 차트 설정
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Date'], 
    y=df['Price'], 
    mode='lines', 
    line=dict(color=current_color, width=3), # 선 색상 변경
    fill='tozeroy', 
    fillcolor=current_rgba # 채우기 색상 변경
))

fig.update_layout(
    plot_bgcolor='black', paper_bgcolor='black',
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(showgrid=False, color='#444'),
    yaxis=dict(showgrid=True, gridcolor='#222', color='#444', side='right'),
    height=300
)
st.plotly_chart(fig, use_container_width=True)

# 7. 매수 버튼 (메뉴 추천)
if st.button("EXECUTE TRADE (MENU RECOMMEND)"):
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1)
    
    picked = random.choice(menus)
    # 추천된 메뉴의 색상을 결과창 테두리에 적용
    picked_color = menu_config[picked]["color"]
    
    st.markdown(f"""
        <div style="border: 2px solid {picked_color}; padding: 20px; text-align: center; background-color: rgba(0,0,0,0.5);">
            <h2 style="margin:0; color: white;">TRADE CONFIRMED</h2>
            <h1 style="color: {picked_color}; font-size: 40px; margin: 10px 0;">{picked}</h1>
            <p style="color: #888;">BUY PRICE: MARKET PRICE | SLIPPAGE: 0.01%</p>
        </div>
    """, unsafe_allow_html=True)