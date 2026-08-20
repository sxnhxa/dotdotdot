import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import random

# 1. 페이지 설정
st.set_page_config(page_title="DOTDOTDOT.SEOUL.2", layout="wide")

# 2. 모바일 최적화 & 브랜드 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=JetBrains+Mono:wght@400&display=swap');
    
    .stApp { background-color: #F5F5F5; color: #1A1A1A; }
    
    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 900px;
    }

    /* 3점 로고 */
    .logo-container { display: flex; gap: 8px; margin-bottom: 15px; }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot.black { background-color: #1A1A1A; }
    .dot.mint { background-color: #00FFD1; box-shadow: 0 0 10px rgba(0, 255, 209, 0.5); }

    h1 { font-family: 'Inter', sans-serif; font-weight: 700; color: #1A1A1A !important; letter-spacing: -1px; }
    .status-text { color: #666; font-size: 14px; margin-top: -15px; }
    
    /* 티커 */
    .ticker-wrapper {
        width: 100%; overflow: hidden; background: #FFFFFF;
        padding: 10px 0; border-bottom: 1px solid #E0E0E0;
        margin-bottom: 25px;
    }
    .ticker {
        display: inline-block; white-space: nowrap;
        animation: marquee 35s linear infinite;
        font-size: 12px; font-weight: 500; color: #888;
    }
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* 버튼 스타일 */
    div.stButton > button {
        width: 100% !important;
        border-radius: 8px !important;
        background-color: #1A1A1A !important;
        border: none !important;
        color: #00FFD1 !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin-top: 10px;
    }

    .result-card {
        background-color: #FFFFFF; padding: 25px; border-radius: 12px;
        border: 1px solid #E0E0E0; border-left: 8px solid #00FFD1;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-top: 25px;
    }

    @media (max-width: 768px) {
        .main .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
        h1 { font-size: 22px !important; }
        .stPlotlyChart { height: 320px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 메뉴 및 랭킹 데이터
menu_config = {
    "AMERICANO": {"color": "#4B3621", "desc": "깊고 진한 풍미의 데일리 커피"},
    "CAFE LATTE": {"color": "#D2B48C", "desc": "부드럽고 고소한 우유의 조화"},
    "EINSPANNER": {"color": "#1A1A1A", "desc": "달콤한 크림 뒤에 오는 묵직한 샷"},
    "STRAWBERRY LATTE": {"color": "#FFB6C1", "desc": "직접 만든 수제 청의 상큼함"},
    "COLD BREW": {"color": "#2F4F4F", "desc": "깔끔하고 청량한 긴 기다림의 맛"}
}
menus = list(menu_config.keys())

# 데이터에서 구체적인 수치는 빼고 순위만 정렬해서 사용
ranking_df = pd.DataFrame({
    "menu": ["EINSPANNER", "STRAWBERRY LATTE", "AMERICANO", "CAFE LATTE", "COLD BREW"],
    "value": [5, 4, 3, 2, 1] # 순위 표현을 위한 가중치 (숫자는 화면에 안 나옴)
}).sort_values("value", ascending=True)

# 4. 로고 & 티커
st.markdown('<div class="logo-container"><div class="dot black"></div><div class="dot black"></div><div class="dot mint"></div></div>', unsafe_allow_html=True)
ticker_text = "  ///  ".join([f"{m} HOT" for m in menus])
st.markdown(f"<div class='ticker-wrapper'><div class='ticker'>{ticker_text}</div></div>", unsafe_allow_html=True)

# 5. 헤더
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.title("DOTDOTDOT TRADING VIEW")
    st.markdown("<p class='status-text'>메뉴 트랜드 (데모)</p>", unsafe_allow_html=True)
with col_h2:
    st.markdown("<div style='text-align:right;'><p style='color:#999; margin:0; font-size:11px;'>SYSTEM</p><h2 style='margin:0; color:#00FFD1; font-size:22px;'>ACTIVE</h2></div>", unsafe_allow_html=True)

# 6. 실시간 메뉴 랭킹 차트 (숫자 제거 버전)
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("🏆 TODAY'S TRENDING")

# 색상 설정 (1위만 민트색 강조)
colors = ['#E0E0E0'] * 4 + ['#00FFD1'] 

fig = go.Figure(go.Bar(
    x=ranking_df['value'],
    y=ranking_df['menu'],
    orientation='h',
    marker_color=colors,
    # text 제거: 숫자 지표 안 보이게 설정
    hoverinfo='none' # 마우스 올려도 숫자 안 나오게
))

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=10, t=10, b=0),
    xaxis=dict(showgrid=False, visible=False), # X축(숫자) 완전 삭제
    yaxis=dict(
        showgrid=False, 
        tickfont=dict(size=13, color="#333", family='Inter'),
        autorange="reversed"
    ),
    height=350,
    hovermode=False
)
st.plotly_chart(fig, use_container_width=True)

# 7. 메뉴 상세
st.markdown("---")
selected_menu = st.selectbox("자세히 알아볼 메뉴를 선택하세요", menus)
current_theme = menu_config[selected_menu]
st.info(f"💡 {selected_menu}: {current_theme['desc']}")

# 8. AI 추천 버튼
st.markdown("<br>", unsafe_allow_html=True)
if st.button("오늘의 메뉴 뽑기 (랜덤)", use_container_width=True):
    with st.spinner("분석 중..."):
        time.sleep(1)
        picked = random.choice(menus)
        picked_info = menu_config[picked]
        
        st.markdown(f"""
            <div class="result-card">
                <p style="color: #00FFD1; font-weight: 700; margin-bottom: 5px; font-size:11px;">MATCHING COMPLETED</p>
                <h1 style="margin: 0; font-size: 26px !important;">{picked}</h1>
                <p style="color: #666; margin-top: 10px; font-size:14px;">{picked_info['desc']}</p>
                <hr style="border: 0.5px solid #EEE; margin: 20px 0;">
                <p style="color: #CCC; font-size: 10px; text-align: right; font-family: 'JetBrains Mono';">
                    POWERED BY SEUNGHA DATA LAB
                </p>
            </div>
        """, unsafe_allow_html=True)
        
