import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import random

# 1. 페이지 설정 (최상단)
st.set_page_config(page_title="DOTDOTDOT.SEOUL.2", layout="wide")

# 2. 모바일 최적화 및 인테리어 반영 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=JetBrains+Mono:wght@400&display=swap');
    
    /* 기본 배경 및 텍스트 설정 */
    .stApp { background-color: #F5F5F5; color: #1A1A1A; }
    
    /* 메인 컨테이너 여백 최적화 (짤림 방지) */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1000px; /* 너무 넓게 퍼지지 않게 제한 */
    }

    /* 3점 로고 스타일 */
    .logo-container { display: flex; gap: 8px; margin-bottom: 15px; }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot.black { background-color: #1A1A1A; }
    .dot.mint { background-color: #00FFD1; box-shadow: 0 0 10px rgba(0, 255, 209, 0.5); }

    /* 헤더 및 타이틀 */
    h1 { font-family: 'Inter', sans-serif; font-weight: 700; color: #1A1A1A !important; letter-spacing: -1px; }
    
    /* 티커 (상단 흐르는 바) */
    .ticker-wrapper {
        width: 100%; overflow: hidden; background: #FFFFFF;
        padding: 10px 0; border-bottom: 1px solid #E0E0E0;
        margin-bottom: 20px;
    }
    .ticker {
        display: inline-block; white-space: nowrap;
        animation: marquee 30s linear infinite;
        font-size: 13px; font-weight: 500; color: #666;
    }
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* 버튼 스타일 (무조건 가로 꽉 채우기) */
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

    /* 결과 카드 */
    .result-card {
        background-color: #FFFFFF; padding: 25px; border-radius: 12px;
        border: 1px solid #E0E0E0; border-left: 8px solid #00FFD1;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        margin-top: 20px;
    }

    /* 🔥 모바일 전용 스타일 (반응형) 🔥 */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        h1 { font-size: 24px !important; }
        .stPlotlyChart { height: 280px !important; }
        .status-box { text-align: left !important; margin-top: 10px; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 메뉴 데이터 설정
menu_config = {
    "AMERICANO": {"color": "#4B3621", "desc": "깊고 진한 풍미의 데일리 커피"},
    "CAFE LATTE": {"color": "#D2B48C", "desc": "부드럽고 고소한 우유의 조화"},
    "EINSPANNER": {"color": "#1A1A1A", "desc": "달콤한 크림 뒤에 오는 묵직한 샷"},
    "STRAWBERRY LATTE": {"color": "#FFB6C1", "desc": "직접 만든 수제 청의 상큼함"},
    "COLD BREW": {"color": "#2F4F4F", "desc": "깔끔하고 청량한 긴 기다림의 맛"}
}
menus = list(menu_config.keys())

# 4. 상단 브랜드 섹션 (로고 & 티커)
st.markdown('<div class="logo-container"><div class="dot black"></div><div class="dot black"></div><div class="dot mint"></div></div>', unsafe_allow_html=True)
ticker_text = "  //  ".join([f"{m} TRENDING" for m in menus])
st.markdown(f"<div class='ticker-wrapper'><div class='ticker'>{ticker_text}</div></div>", unsafe_allow_html=True)

# 5. 메인 헤더 (모바일 대응 레이아웃)
col1, col2 = st.columns([2, 1])
with col1:
    st.title("DOTDOTDOT TRADING VIEW")
    st.markdown("<p style='color: #666; margin-top:-10px;'>실시간 메뉴 인기도 및 추천 시스템</p>", unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class='status-box' style='text-align:right;'>
            <p style='color:#999; margin:0; font-size:12px;'>BREWING STATUS</p>
            <h2 style='margin:0; color:#00FFD1; font-size:24px;'>ACTIVE</h2>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. 인터랙티브 차트 섹션
selected_menu = st.selectbox("어떤 메뉴의 지표를 확인할까요?", menus)
current_theme = menu_config[selected_menu]

# 가상 데이터 생성 (실제 서비스 시 API 연동 가능)
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
    fillcolor=f"rgba({int(current_theme['color'][1:3], 16) if len(current_theme['color'])>4 else 100}, 100, 100, 0.05)"
))

fig.update_layout(
    plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(showgrid=False, color='#999', tickfont=dict(size=10)),
    yaxis=dict(showgrid=True, gridcolor='#F0F0F0', color='#999', side='right', tickfont=dict(size=10)),
    height=300,
    hovermode='x unified'
)
st.plotly_chart(fig, use_container_width=True)

# 7. 추천 로직 및 결과 출력
st.markdown("<br>", unsafe_allow_html=True)
if st.button("오늘 나에게 맞는 메뉴 찾기 (AI PICK)", use_container_width=True):
    with st.spinner("최적의 밸런스를 분석 중..."):
        time.sleep(1)
        picked = random.choice(menus)
        picked_info = menu_config[picked]
        
        st.markdown(f"""
            <div class="result-card">
                <p style="color: #00FFD1; font-weight: 700; margin-bottom: 5px; font-size:12px;">SELECTION CONFIRMED</p>
                <h1 style="margin: 0; font-size: 28px !important;">{picked}</h1>
                <p style="color: #666; margin-top: 10px; font-size:14px;">{picked_info['desc']}</p>
                <hr style="border: 0.5px solid #EEE; margin: 15px 0;">
                <p style="color: #BBB; font-size: 11px; text-align: right; font-family: 'JetBrains Mono';">
                    ANALYZED BY DOTDOTDOT DATA LAB
                </p>
            </div>
        """, unsafe_allow_html=True)
        

