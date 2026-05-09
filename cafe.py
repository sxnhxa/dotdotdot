import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import random

# 1. 페이지 설정
st.set_page_config(page_title="DOTDOTDOT.SEOUL.2", layout="wide")

# 2. 매장 인테리어(화이트/민트/실버)를 반영한 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=JetBrains+Mono:wght@400&display=swap');
    
    /* 전체 배경: 매장의 밝은 벽면 느낌 (Off-White) */
    .stApp { background-color: #F5F5F5; color: #1A1A1A; }
    
    /* 3점 로고 구현 (CSS) */
    .logo-container { display: flex; gap: 8px; margin-bottom: 10px; }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot.black { background-color: #1A1A1A; }
    .dot.mint { background-color: #00FFD1; box-shadow: 0 0 10px rgba(0, 255, 209, 0.5); }

    /* 헤더 스타일 */
    h1 { font-family: 'Inter', sans-serif; font-weight: 700; color: #1A1A1A !important; letter-spacing: -1px; }
    
    /* 티커 (상단 바) */
    .ticker-wrapper {
        width: 100%; overflow: hidden; background: #FFFFFF;
        padding: 12px 0; border-bottom: 1px solid #E0E0E0;
    }
    .ticker {
        display: inline-block; white-space: nowrap;
        animation: marquee 40s linear infinite;
        font-size: 14px; font-weight: 500; color: #666;
    }
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* 버튼 스타일: 매장의 민트 포인트 */
    .stButton>button {
        width: 100% !important;
        border-radius: 8px;
        background-color: #1A1A1A; border: none;
        color: #00FFD1; height: 55px; font-size: 18px; font-weight: 700;
        transition: all 0.2s;
    }
    .stButton>button:hover { background-color: #00FFD1 !important; color: #1A1A1A !important; }

    /* 추천 결과창 (영수증 감성) */
    .result-card {
        background-color: #FFFFFF; padding: 30px; border-radius: 12px;
        border: 1px solid #E0E0E0; border-left: 8px solid #00FFD1;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 메뉴 설정
menu_config = {
    "AMERICANO": {"color": "#4B3621", "desc": "깊고 진한 풍미의 데일리 커피"},
    "CAFE LATTE": {"color": "#D2B48C", "desc": "부드럽고 고소한 우유의 조화"},
    "EINSPANNER": {"color": "#1A1A1A", "desc": "달콤한 크림 뒤에 오는 묵직한 샷"},
    "STRAWBERRY LATTE": {"color": "#FFB6C1", "desc": "직접 만든 수제 청의 상큼함"},
    "COLD BREW": {"color": "#2F4F4F", "desc": "깔끔하고 청량한 긴 기다림의 맛"}
}
menus = list(menu_config.keys())

# 4. 상단 로고 & 티커
st.markdown('<div class="logo-container"><div class="dot black"></div><div class="dot black"></div><div class="dot mint"></div></div>', unsafe_allow_html=True)
ticker_text = "  /  ".join([f"{m} TRENDING" for m in menus])
st.markdown(f"<div class='ticker-wrapper'><div class='ticker'>{ticker_text}</div></div>", unsafe_allow_html=True)

# 5. 헤더
col1, col2 = st.columns([3, 1])
with col1:
    st.title("DOTDOTDOT TRADING VIEW")
    st.markdown("<p style='color: #666;'>실시간 메뉴 인기도 및 추천 시스템</p>", unsafe_allow_html=True)
with col2:
    st.markdown("<div style='text-align:right;'><p style='color:#999; margin:0;'>BREWING STATUS</p><h2 style='margin:0; color:#00FFD1;'>ACTIVE</h2></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. 차트 섹션
selected_menu = st.selectbox("어떤 메뉴의 지표를 확인할까요?", menus)
current_theme = menu_config[selected_menu]

# 데이터 생성
np.random.seed(len(selected_menu))
df = pd.DataFrame({
    'Time': pd.date_range(datetime.now().replace(hour=9, minute=0), periods=50, freq='5min'),
    'Index': np.random.randn(50).cumsum() + 100
})

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Time'], y=df['Index'],
    mode='lines',
    line=dict(color=current_theme['color'], width=4),
    fill='tozeroy',
    fillcolor=f"rgba({int(current_theme['color'][1:3], 16) if len(current_theme['color'])>4 else 255}, 100, 100, 0.05)"
))

fig.update_layout(
    plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(showgrid=False, color='#999'),
    yaxis=dict(showgrid=True, gridcolor='#F0F0F0', color='#999', side='right'),
    height=300
)
st.plotly_chart(fig, use_container_width=True)

# 7. 추천 버튼
st.markdown("<br>", unsafe_allow_html=True)
if st.button("오늘 나에게 맞는 메뉴 찾기 (AI PICK)", use_container_width=True):
    with st.spinner("최적의 밸런스를 분석 중..."):
        time.sleep(1)
        picked = random.choice(menus)
        picked_info = menu_config[picked]
        
        st.markdown(f"""
            <div class="result-card">
                <p style="color: #00FFD1; font-weight: 700; margin-bottom: 5px;">SELECTION CONFIRMED</p>
                <h1 style="margin: 0; font-size: 36px;">{picked}</h1>
                <p style="color: #666; margin-top: 10px;">{picked_info['desc']}</p>
                <hr style="border: 0.5px solid #EEE; margin: 20px 0;">
                <p style="color: #999; font-size: 12px; text-align: right;">ANALYZED BY DOTDOTDOT DATA LAB</p>
            </div>
        """, unsafe_allow_html=True)