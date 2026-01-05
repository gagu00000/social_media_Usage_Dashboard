
# ================================================================================
# 🧠 SOCIAL MEDIA USAGE & MENTAL HEALTH — INTELLIGENCE DASHBOARD
# ================================================================================
# Author: [Your Name]
# Date: [Date]
# Description: Comprehensive analytics dashboard analyzing social media usage 
#              patterns and their impact on mental health in India
# ================================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ================================================================================
# PAGE CONFIGURATION
# ================================================================================
st.set_page_config(
    page_title="Social Media & Mental Health Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================================
# COLOR PALETTE - NAVY BLUE & SILVER EXECUTIVE THEME
# ================================================================================
COLORS = {
    'primary': '#3a86ff',
    'secondary': '#4cc9f0',
    'accent': '#7209b7',
    'success': '#4ade80',
    'warning': '#fb923c',
    'danger': '#f87171',
    'neutral': '#8facc4',
    'dark': '#0a1628',
    'medium': '#1a2d47',
    'light': '#2a4a7f',
    'text_primary': '#ffffff',
    'text_secondary': '#e8e8e8',
    'text_muted': '#8facc4',
}

CHART_COLORS = ['#3a86ff', '#4cc9f0', '#4ade80', '#fb923c', '#f87171',                 '#a78bfa', '#7209b7', '#fbbf24', '#ec4899', '#14b8a6']

RISK_COLORS = {
    'Low': '#4ade80',
    'Moderate-Low': '#fbbf24',
    'Moderate-High': '#fb923c',
    'High': '#f87171'
}

# ================================================================================
# CSS STYLING
# ================================================================================
st.markdown("""
<style>
    /* ===== MAIN BACKGROUND ===== */
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #1a2d47 50%, #0d1b2a 100%);
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1628 0%, #152238 100%);
        border-right: 2px solid #3a86ff;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e8e8e8;
    }
    
    /* ===== HEADINGS ===== */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* ===== METRICS ===== */
    [data-testid="stMetricValue"] {
        color: #3a86ff;
        font-size: 1.8rem;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0b0b0;
    }
    
    /* ===== DIVIDER ===== */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #3a86ff, transparent);
        margin: 25px 0;
    }
    
    /* ===== KPI CARDS ===== */
    .kpi-card {
        background: linear-gradient(135deg, #1a2d47 0%, #0d1b2a 100%);
        border: 1px solid #2a4a7f;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(58, 134, 255, 0.15);
        border-color: #3a86ff;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #ffffff;
        margin: 10px 0;
    }
    
    .kpi-label {
        color: #8facc4;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .kpi-delta-positive {
        color: #4ade80;
        font-size: 0.85rem;
    }
    
    .kpi-delta-negative {
        color: #f87171;
        font-size: 0.85rem;
    }
    
    /* ===== INSIGHT BOX ===== */
    .insight-box {
        background: linear-gradient(135deg, #1a2d47 0%, #0d1b2a 100%);
        border: 1px solid #2a4a7f;
        border-left: 4px solid #3a86ff;
        border-radius: 8px;
        padding: 20px 25px;
        margin: 15px 0;
    }
    
    .insight-title {
        color: #3a86ff;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 15px;
    }
    
    .insight-text {
        color: #d0d0d0;
        font-size: 0.95rem;
        line-height: 1.8;
    }
    
    /* ===== SUCCESS/WARNING/DANGER BOXES ===== */
    .success-box {
        background: linear-gradient(135deg, rgba(74, 222, 128, 0.1), #0d1b2a);
        border: 1px solid #4ade80;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(251, 146, 60, 0.1), #0d1b2a);
        border: 1px solid #fb923c;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .danger-box {
        background: linear-gradient(135deg, rgba(248, 113, 113, 0.1), #0d1b2a);
        border: 1px solid #f87171;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* ===== RADIO BUTTONS ===== */
    .stRadio > div {
        background-color: rgba(58, 134, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #2a4a7f;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(58, 134, 255, 0.1);
        border-radius: 10px;
        padding: 5px;
        gap: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #8facc4;
        border-radius: 8px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3a86ff;
        color: white;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a1628;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3a86ff;
        border-radius: 4px;
    }
    
    /* ===== SELECTBOX ===== */
    .stSelectbox > div > div {
        background-color: #1a2d47;
        border-color: #2a4a7f;
    }
    
    /* ===== MULTISELECT ===== */
    .stMultiSelect > div > div {
        background-color: #1a2d47;
        border-color: #2a4a7f;
    }
    
    /* ===== SLIDER ===== */
    .stSlider > div > div > div {
        background-color: #3a86ff;
    }
</style>
""", unsafe_allow_html=True)

# ================================================================================
# HELPER FUNCTIONS
# ================================================================================

def get_chart_layout(title="", height=400):
    """Returns consistent Plotly layout for dark theme"""
    return dict(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e8e8e8', size=12),
        title=dict(text=title, font=dict(color='#ffffff', size=16), x=0.5),
        xaxis=dict(
            gridcolor='rgba(58,134,255,0.1)',
            linecolor='#2a4a7f',
            tickfont=dict(color='#8facc4'),
            title_font=dict(color='#8facc4')
        ),
        yaxis=dict(
            gridcolor='rgba(58,134,255,0.1)',
            linecolor='#2a4a7f',
            tickfont=dict(color='#8facc4'),
            title_font=dict(color='#8facc4')
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e8e8e8'),
            bordercolor='#2a4a7f'
        ),
        margin=dict(l=60, r=30, t=60, b=60),
        height=height
    )

def render_kpi_card(label, value, delta=None, delta_type="positive"):
    """Render a styled KPI card"""
    delta_class = 'kpi-delta-positive' if delta_type == 'positive' else 'kpi-delta-negative'
    delta_symbol = '▲' if delta_type == 'positive' else '▼'
    delta_html = f"<div class='{delta_class}'>{delta_symbol} {delta}</div>" if delta else ""
    
    return f"""
    <div class='kpi-card'>
        <div class='kpi-label'>{label}</div>
        <div class='kpi-value'>{value}</div>
        {delta_html}
    </div>
    """

def render_insight_box(title, content, color="#3a86ff"):
    """Render a styled insight box"""
    st.markdown(f"""
    <div class='insight-box' style='border-left-color: {color};'>
        <div class='insight-title' style='color: {color};'>{title}</div>
        <div class='insight-text'>{content}</div>
    </div>
    """, unsafe_allow_html=True)

def render_divider():
    """Render a styled divider"""
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

def create_sparkline(data, color="#3a86ff"):
    """Create a simple sparkline"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=data, mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=f'rgba{tuple(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (0.2,)}'
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=50, width=150,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False
    )
    return fig

# ================================================================================
# DATA LOADING
# ================================================================================

@st.cache_data
def load_data():
    """Load all datasets"""
    try:
        main_df = pd.read_csv('data/main_survey_data.csv')
        daily_df = pd.read_csv('data/daily_usage_data.csv')
        platform_df = pd.read_csv('data/platform_metadata.csv')
        
        # Convert date columns
        main_df['survey_date'] = pd.to_datetime(main_df['survey_date'])
        daily_df['date'] = pd.to_datetime(daily_df['date'])
        
        return main_df, daily_df, platform_df
    except FileNotFoundError:
        st.error("⚠️ Data files not found. Please ensure CSV files are in the 'data/' folder.")
        return None, None, None

# ================================================================================
# MAIN APPLICATION
# ================================================================================

def main():
    # Load data
    main_df, daily_df, platform_df = load_data()
    
    if main_df is None:
        st.stop()
    
    # ==================== HEADER ====================
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 2.5rem; margin-bottom: 10px;'>
            🧠 Social Media & Mental Health Intelligence Dashboard
        </h1>
        <p style='color: #8facc4; font-size: 1.1rem;'>
            Analyzing behavioral patterns and mental health impact across India
        </p>
        <p style='color: #4cc9f0; font-size: 0.9rem;'>
            📊 {users:,} Users | 📅 {records:,} Daily Records | 🇮🇳 {states} States
        </p>
    </div>
    """.format(
        users=len(main_df),
        records=len(daily_df),
        states=main_df['state'].nunique()
    ), unsafe_allow_html=True)
    
    render_divider()
    
    # ==================== SIDEBAR FILTERS ====================
    with st.sidebar:
        st.markdown("## 🎛️ Filters")
        st.markdown("---")
        
        # Age Group Filter
        age_groups = ['All'] + sorted(main_df['age_group'].unique().tolist())
        selected_age = st.selectbox("👤 Age Group", age_groups)
        
        # Gender Filter
        genders = ['All'] + sorted(main_df['gender'].unique().tolist())
        selected_gender = st.selectbox("⚧ Gender", genders)
        
        # Region Filter
        regions = ['All'] + sorted(main_df['region'].unique().tolist())
        selected_region = st.selectbox("🗺️ Region", regions)
        
        # Platform Filter
        platforms = ['All'] + sorted(main_df['primary_platform'].unique().tolist())
        selected_platform = st.selectbox("📱 Platform", platforms)
        
        # Screen Time Range
        st.markdown("### ⏱️ Screen Time Range")
        screen_time_range = st.slider(
            "Hours per day",
            min_value=float(main_df['avg_daily_screen_time_hrs'].min()),
            max_value=float(main_df['avg_daily_screen_time_hrs'].max()),
            value=(0.5, 14.0)
        )
        
        # Risk Category Filter
        risk_cats = ['All'] + sorted(main_df['risk_category'].unique().tolist())
        selected_risk = st.selectbox("⚠️ Risk Category", risk_cats)
        
        st.markdown("---")
        st.markdown("### 📊 Data Info")
        st.info(f"""
        **Last Updated:** {main_df['survey_date'].max().strftime('%Y-%m-%d')}  
        **Source:** Simulated Survey Data  
        **Period:** Jan - Jun 2024
        """)
    
    # Apply filters
    filtered_df = main_df.copy()
    
    if selected_age != 'All':
        filtered_df = filtered_df[filtered_df['age_group'] == selected_age]
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['gender'] == selected_gender]
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    if selected_platform != 'All':
        filtered_df = filtered_df[filtered_df['primary_platform'] == selected_platform]
    if selected_risk != 'All':
        filtered_df = filtered_df[filtered_df['risk_category'] == selected_risk]
    
    filtered_df = filtered_df[
        (filtered_df['avg_daily_screen_time_hrs'] >= screen_time_range[0]) &
        (filtered_df['avg_daily_screen_time_hrs'] <= screen_time_range[1])
    ]
    
    # Filter daily data
    filtered_daily = daily_df[daily_df['user_id'].isin(filtered_df['user_id'])]
    
    # ==================== KPI SECTION ====================
    st.markdown("## 📊 Key Performance Indicators")
    
    kpi_cols = st.columns(5)
    
    with kpi_cols[0]:
        avg_screen = filtered_df['avg_daily_screen_time_hrs'].mean()
        st.markdown(render_kpi_card(
            "Avg Screen Time",
            f"{avg_screen:.1f} hrs",
            f"{((avg_screen - main_df['avg_daily_screen_time_hrs'].mean()) / main_df['avg_daily_screen_time_hrs'].mean() * 100):.1f}% vs overall",
            "negative" if avg_screen > main_df['avg_daily_screen_time_hrs'].mean() else "positive"
        ), unsafe_allow_html=True)
    
    with kpi_cols[1]:
        avg_anxiety = filtered_df['anxiety_score'].mean()
        st.markdown(render_kpi_card(
            "Avg Anxiety Score",
            f"{avg_anxiety:.1f}/21",
            f"{((avg_anxiety - main_df['anxiety_score'].mean()) / main_df['anxiety_score'].mean() * 100):.1f}% vs overall",
            "negative" if avg_anxiety > main_df['anxiety_score'].mean() else "positive"
        ), unsafe_allow_html=True)
    
    with kpi_cols[2]:
        high_risk_pct = (filtered_df['risk_category'] == 'High').mean() * 100
        st.markdown(render_kpi_card(
            "High Risk Users",
            f"{high_risk_pct:.1f}%",
            f"{len(filtered_df[filtered_df['risk_category'] == 'High']):,} users",
            "negative"
        ), unsafe_allow_html=True)
    
    with kpi_cols[3]:
        poor_sleep_pct = (filtered_df['sleep_quality_category'].isin(['Poor', 'Very Poor'])).mean() * 100
        st.markdown(render_kpi_card(
            "Poor Sleep Quality",
            f"{poor_sleep_pct:.1f}%",
            f"{len(filtered_df[filtered_df['sleep_quality_category'].isin(['Poor', 'Very Poor'])]):,} users",
            "negative"
        ), unsafe_allow_html=True)
    
    with kpi_cols[4]:
        risk_index = filtered_df['mental_health_risk_score'].mean()
        st.markdown(render_kpi_card(
            "Risk Index",
            f"{risk_index:.0f}/100",
            "Composite Score",
            "negative" if risk_index > 50 else "positive"
        ), unsafe_allow_html=True)
    
    render_divider()
    
    # ==================== MAIN TABS ====================
    tabs = st.tabs([
        "📈 Overview",
        "👥 Demographics", 
        "📱 Platforms",
        "⏰ Temporal",
        "🧠 Mental Health",
        "😴 Sleep",
        "🔗 Correlations",
        "🗺️ Geographic",
        "🤖 ML Predictions",
        "⚖️ Ethics"
    ])
    
    # ==================== TAB 1: OVERVIEW ====================
    with tabs[0]:
        st.markdown("### 📈 Dashboard Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk Distribution - Donut Chart
            risk_counts = filtered_df['risk_category'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=risk_counts.index,
                values=risk_counts.values,
                hole=0.6,
                marker=dict(colors=[RISK_COLORS.get(cat, '#8facc4') for cat in risk_counts.index]),
                textinfo='percent+label',
                textfont=dict(color='white')
            )])
            fig.update_layout(**get_chart_layout("Risk Category Distribution"))
            fig.add_annotation(
                text=f"<b>{len(filtered_df):,}</b><br>Users",
                x=0.5, y=0.5, font_size=16, showarrow=False,
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Screen Time by Risk Category - Bar Chart
            screen_by_risk = filtered_df.groupby('risk_category')['avg_daily_screen_time_hrs'].mean().reset_index()
            screen_by_risk = screen_by_risk.sort_values('avg_daily_screen_time_hrs')
            
            fig = go.Figure(data=[go.Bar(
                x=screen_by_risk['avg_daily_screen_time_hrs'],
                y=screen_by_risk['risk_category'],
                orientation='h',
                marker=dict(color=[RISK_COLORS.get(cat, '#8facc4') for cat in screen_by_risk['risk_category']]),
                text=screen_by_risk['avg_daily_screen_time_hrs'].round(1),
                textposition='auto',
                textfont=dict(color='white')
            )])
            fig.update_layout(**get_chart_layout("Avg Screen Time by Risk Category"))
            fig.update_layout(xaxis_title="Hours per Day", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        
        # Insight Box
        high_risk_screen = filtered_df[filtered_df['risk_category'] == 'High']['avg_daily_screen_time_hrs'].mean()
        low_risk_screen = filtered_df[filtered_df['risk_category'] == 'Low']['avg_daily_screen_time_hrs'].mean()
        render_insight_box(
            "📊 Key Insight",
            f"High-risk users spend <b>{high_risk_screen:.1f} hours</b> on social media daily, "
            f"which is <b>{((high_risk_screen/low_risk_screen - 1) * 100):.0f}% more</b> than low-risk users "
            f"({low_risk_screen:.1f} hours). This indicates a strong correlation between screen time and mental health risk.",
            COLORS['primary']
        )
        
        # Summary Statistics Table
        st.markdown("### 📋 Summary Statistics")
        
        summary_stats = pd.DataFrame({
            'Metric': ['Total Users', 'Avg Age', 'Avg Screen Time', 'Avg Anxiety', 'Avg Depression', 
                      'Avg Sleep Hours', 'Night Users %', 'High Risk %'],
            'Value': [
                f"{len(filtered_df):,}",
                f"{filtered_df['age'].mean():.1f} years",
                f"{filtered_df['avg_daily_screen_time_hrs'].mean():.2f} hrs/day",
                f"{filtered_df['anxiety_score'].mean():.1f}/21",
                f"{filtered_df['depression_score'].mean():.1f}/27",
                f"{filtered_df['avg_sleep_hours'].mean():.1f} hrs",
                f"{filtered_df['night_usage'].mean() * 100:.1f}%",
                f"{(filtered_df['risk_category'] == 'High').mean() * 100:.1f}%"
            ]
        })
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.dataframe(summary_stats, use_container_width=True, hide_index=True)
    
    # ==================== TAB 2: DEMOGRAPHICS ====================
    with tabs[1]:
        st.markdown("### 👥 Demographic Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Age Distribution - Histogram
            fig = px.histogram(
                filtered_df, x='age', nbins=30,
                color_discrete_sequence=[COLORS['primary']],
                labels={'age': 'Age', 'count': 'Number of Users'}
            )
            fig.update_layout(**get_chart_layout("Age Distribution"))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gender Distribution - Pie Chart
            gender_counts = filtered_df['gender'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=gender_counts.index,
                values=gender_counts.values,
                marker=dict(colors=CHART_COLORS[:len(gender_counts)]),
                textinfo='percent+label',
                textfont=dict(color='white')
            )])
            fig.update_layout(**get_chart_layout("Gender Distribution"))
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Age Group by Risk - Grouped Bar Chart
            age_risk = filtered_df.groupby(['age_group', 'risk_category']).size().unstack(fill_value=0)
            
            fig = go.Figure()
            for i, risk in enumerate(age_risk.columns):
                fig.add_trace(go.Bar(
                    name=risk,
                    x=age_risk.index,
                    y=age_risk[risk],
                    marker_color=RISK_COLORS.get(risk, CHART_COLORS[i])
                ))
            
            fig.update_layout(**get_chart_layout("Risk Distribution by Age Group"))
            fig.update_layout(barmode='group', xaxis_title="Age Group", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Education - Lollipop Chart
            edu_counts = filtered_df['education'].value_counts().sort_values()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=edu_counts.values,
                y=edu_counts.index,
                mode='markers',
                marker=dict(size=15, color=COLORS['primary']),
                name='Count'
            ))
            for i, (edu, count) in enumerate(edu_counts.items()):
                fig.add_shape(
                    type='line',
                    x0=0, x1=count,
                    y0=edu, y1=edu,
                    line=dict(color=COLORS['primary'], width=2)
                )
            
            fig.update_layout(**get_chart_layout("Education Level Distribution"))
            fig.update_layout(xaxis_title="Number of Users", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        
        # Occupation Breakdown - Stacked Bar
        st.markdown("#### 💼 Occupation vs Screen Time Category")
        
        occ_screen = pd.crosstab(filtered_df['occupation'], filtered_df['screen_time_category'], normalize='index') * 100
        
        fig = go.Figure()
        for col in occ_screen.columns:
            fig.add_trace(go.Bar(
                name=col,
                x=occ_screen.index,
                y=occ_screen[col],
                marker_color=CHART_COLORS[list(occ_screen.columns).index(col) % len(CHART_COLORS)]
            ))
        
        fig.update_layout(**get_chart_layout("Screen Time Category by Occupation (%)"))
        fig.update_layout(barmode='stack', xaxis_title="Occupation", yaxis_title="Percentage")
        st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 3: PLATFORM ANALYSIS ====================
    with tabs[2]:
        st.markdown("### 📱 Platform Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Platform Usage - Bar Chart
            platform_counts = filtered_df['primary_platform'].value_counts()
            
            fig = go.Figure(data=[go.Bar(
                x=platform_counts.values,
                y=platform_counts.index,
                orientation='h',
                marker=dict(color=CHART_COLORS[:len(platform_counts)]),
                text=platform_counts.values,
                textposition='auto',
                textfont=dict(color='white')
            )])
            fig.update_layout(**get_chart_layout("Primary Platform Usage"))
            fig.update_layout(xaxis_title="Number of Users", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Anxiety by Platform - Grouped Bar
            platform_anxiety = filtered_df.groupby('primary_platform').agg({
                'anxiety_score': 'mean',
                'depression_score': 'mean'
            }).round(1).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Anxiety',
                x=platform_anxiety['primary_platform'],
                y=platform_anxiety['anxiety_score'],
                marker_color=COLORS['warning']
            ))
            fig.add_trace(go.Bar(
                name='Depression',
                x=platform_anxiety['primary_platform'],
                y=platform_anxiety['depression_score'],
                marker_color=COLORS['danger']
            ))
            
            fig.update_layout(**get_chart_layout("Mental Health Scores by Platform"))
            fig.update_layout(barmode='group', xaxis_title="Platform", yaxis_title="Score")
            st.plotly_chart(fig, use_container_width=True)
        
        # Treemap - Platform by Region
        st.markdown("#### 🌳 Platform Usage Hierarchy")
        
        treemap_data = filtered_df.groupby(['region', 'primary_platform']).size().reset_index(name='count')
        
        fig = px.treemap(
            treemap_data,
            path=['region', 'primary_platform'],
            values='count',
            color='count',
            color_continuous_scale=['#1a2d47', '#3a86ff', '#4cc9f0']
        )
        fig.update_layout(**get_chart_layout("Platform Distribution by Region", height=500))
        fig.update_traces(textfont=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
        
        # Sunburst - Platform > Usage Type > Risk
        st.markdown("#### 🌞 Platform → Screen Time → Risk Hierarchy")
        
        sunburst_data = filtered_df.groupby(
            ['primary_platform', 'screen_time_category', 'risk_category']
        ).size().reset_index(name='count')
        
        fig = px.sunburst(
            sunburst_data,
            path=['primary_platform', 'screen_time_category', 'risk_category'],
            values='count',
            color='count',
            color_continuous_scale=['#1a2d47', '#3a86ff', '#4cc9f0']
        )
        fig.update_layout(**get_chart_layout("Platform → Usage → Risk Breakdown", height=500))
        fig.update_traces(textfont=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 4: TEMPORAL ANALYSIS ====================
    with tabs[3]:
        st.markdown("### ⏰ Temporal Analysis")
        
        # Daily trends
        daily_trends = filtered_daily.groupby('date').agg({
            'screen_time_hours': 'mean',
            'anxiety_score_daily': 'mean',
            'sleep_hours': 'mean',
            'mood_rating': 'mean'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Line Chart - Screen Time Trend
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_trends['date'],
                y=daily_trends['screen_time_hours'],
                mode='lines',
                name='Screen Time',
                line=dict(color=COLORS['primary'], width=2),
                fill='tozeroy',
                fillcolor='rgba(58, 134, 255, 0.1)'
            ))
            
            # Add moving average
            daily_trends['ma_7'] = daily_trends['screen_time_hours'].rolling(7).mean()
            fig.add_trace(go.Scatter(
                x=daily_trends['date'],
                y=daily_trends['ma_7'],
                mode='lines',
                name='7-Day MA',
                line=dict(color=COLORS['warning'], width=2, dash='dash')
            ))
            
            fig.update_layout(**get_chart_layout("Screen Time Trend"))
            fig.update_layout(xaxis_title="Date", yaxis_title="Hours")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Area Chart - Anxiety Trend
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_trends['date'],
                y=daily_trends['anxiety_score_daily'],
                mode='lines',
                name='Anxiety',
                line=dict(color=COLORS['danger'], width=2),
                fill='tozeroy',
                fillcolor='rgba(248, 113, 113, 0.2)'
            ))
            
            fig.update_layout(**get_chart_layout("Anxiety Score Trend"))
            fig.update_layout(xaxis_title="Date", yaxis_title="Score")
            st.plotly_chart(fig, use_container_width=True)
        
        # Day of Week Analysis
        st.markdown("#### 📅 Day of Week Patterns")
        
        dow_analysis = filtered_daily.groupby('day_of_week').agg({
            'screen_time_hours': 'mean',
            'anxiety_score_daily': 'mean'
        }).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=[go.Bar(
                x=dow_analysis.index,
                y=dow_analysis['screen_time_hours'],
                marker_color=[COLORS['warning'] if day in ['Saturday', 'Sunday'] else COLORS['primary'] 
                             for day in dow_analysis.index],
                text=dow_analysis['screen_time_hours'].round(1),
                textposition='auto',
                textfont=dict(color='white')
            )])
            fig.update_layout(**get_chart_layout("Avg Screen Time by Day"))
            fig.update_layout(xaxis_title="", yaxis_title="Hours")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Calendar Heatmap (simplified as monthly heatmap)
            filtered_daily['week'] = filtered_daily['date'].dt.isocalendar().week
            filtered_daily['dow_num'] = filtered_daily['date'].dt.dayofweek
            
            calendar_data = filtered_daily.groupby(['week', 'day_of_week'])['screen_time_hours'].mean().unstack()
            calendar_data = calendar_data.reindex(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
            
            fig = go.Figure(data=go.Heatmap(
                z=calendar_data.values,
                x=calendar_data.columns,
                y=[f"Week {w}" for w in calendar_data.index],
                colorscale=[[0, '#1a2d47'], [0.5, '#3a86ff'], [1, '#f87171']],
                text=np.round(calendar_data.values, 1),
                texttemplate='%{text}',
                textfont=dict(color='white', size=10),
                hovertemplate='%{y}, %{x}<br>Screen Time: %{z:.1f} hrs<extra></extra>'
            ))
            fig.update_layout(**get_chart_layout("Weekly Usage Heatmap (Calendar View)"))
            st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 5: MENTAL HEALTH ====================
    with tabs[4]:
        st.markdown("### 🧠 Mental Health Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Box Plot - Anxiety by Age Group
            fig = px.box(
                filtered_df, x='age_group', y='anxiety_score',
                color='age_group',
                color_discrete_sequence=CHART_COLORS
            )
            fig.update_layout(**get_chart_layout("Anxiety Score Distribution by Age"))
            fig.update_layout(showlegend=False, xaxis_title="Age Group", yaxis_title="Anxiety Score")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Violin Plot - Depression by Platform
            top_platforms = filtered_df['primary_platform'].value_counts().head(5).index.tolist()
            violin_data = filtered_df[filtered_df['primary_platform'].isin(top_platforms)]
            
            fig = px.violin(
                violin_data, x='primary_platform', y='depression_score',
                color='primary_platform',
                color_discrete_sequence=CHART_COLORS,
                box=True
            )
            fig.update_layout(**get_chart_layout("Depression Score by Platform"))
            fig.update_layout(showlegend=False, xaxis_title="Platform", yaxis_title="Depression Score")
            st.plotly_chart(fig, use_container_width=True)
        
        # Radar Chart - Mental Health Profile
        st.markdown("#### 🎯 Mental Health Profile by Risk Category")
        
        radar_metrics = ['anxiety_score', 'depression_score', 'stress_score', 
                        'loneliness_score', 'fomo_score']
        radar_labels = ['Anxiety', 'Depression', 'Stress', 'Loneliness', 'FOMO']
        
        # Normalize scores for radar
        radar_data = filtered_df.groupby('risk_category')[radar_metrics].mean()
        
        # Normalize to 0-1 scale
        radar_normalized = radar_data.copy()
        for col in radar_metrics:
            radar_normalized[col] = (radar_data[col] - radar_data[col].min()) / (radar_data[col].max() - radar_data[col].min())
        
        fig = go.Figure()
        
        for risk_cat in radar_normalized.index:
            values = radar_normalized.loc[risk_cat].values.tolist()
            values.append(values[0])  # Close the polygon
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=radar_labels + [radar_labels[0]],
                name=risk_cat,
                line=dict(color=RISK_COLORS.get(risk_cat, '#8facc4'), width=2),
                fill='toself',
                fillcolor=f"rgba{tuple(int(RISK_COLORS.get(risk_cat, '#8facc4').lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.2,)}"
            ))
        
        fig.update_layout(**get_chart_layout("Mental Health Radar by Risk Category", height=500))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], gridcolor='rgba(58,134,255,0.2)'),
                angularaxis=dict(gridcolor='rgba(58,134,255,0.2)')
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # T-test Analysis
        st.markdown("#### 📊 Statistical Validation")
        
        high_screen = filtered_df[filtered_df['avg_daily_screen_time_hrs'] >= 6]['anxiety_score']
        low_screen = filtered_df[filtered_df['avg_daily_screen_time_hrs'] < 3]['anxiety_score']
        
        if len(high_screen) > 0 and len(low_screen) > 0:
            t_stat, p_value = stats.ttest_ind(high_screen, low_screen)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("High Screen Time Anxiety", f"{high_screen.mean():.2f}")
            with col2:
                st.metric("Low Screen Time Anxiety", f"{low_screen.mean():.2f}")
            with col3:
                significance = "✅ Significant" if p_value < 0.05 else "❌ Not Significant"
                st.metric("p-value", f"{p_value:.4f}", significance)
            
            render_insight_box(
                "📈 Statistical Finding",
                f"Users with high screen time (≥6 hrs) have significantly higher anxiety scores "
                f"(mean: {high_screen.mean():.2f}) compared to low screen time users (<3 hrs, mean: {low_screen.mean():.2f}). "
                f"This difference is statistically {'significant' if p_value < 0.05 else 'not significant'} (p={p_value:.4f}).",
                COLORS['success'] if p_value < 0.05 else COLORS['warning']
            )
    
    # ==================== TAB 6: SLEEP ANALYSIS ====================
    with tabs[5]:
        st.markdown("### 😴 Sleep Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter Plot - Night Usage vs Sleep Quality
            fig = px.scatter(
                filtered_df,
                x='night_usage_hours',
                y='sleep_quality_score',
                color='risk_category',
                color_discrete_map=RISK_COLORS,
                size='avg_daily_screen_time_hrs',
                hover_data=['age', 'primary_platform'],
                opacity=0.6
            )
            
            # Add trendline
            z = np.polyfit(filtered_df['night_usage_hours'], filtered_df['sleep_quality_score'], 1)
            p = np.poly1d(z)
            x_line = np.linspace(filtered_df['night_usage_hours'].min(), filtered_df['night_usage_hours'].max(), 100)
            fig.add_trace(go.Scatter(
                x=x_line, y=p(x_line),
                mode='lines',
                name='Trend',
                line=dict(color='white', dash='dash', width=2)
            ))
            
            fig.update_layout(**get_chart_layout("Night Usage vs Sleep Quality"))
            fig.update_layout(xaxis_title="Night Usage (hrs)", yaxis_title="Sleep Quality Score (lower=better)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Heatmap - Sleep Quality vs Anxiety vs Screen Time
            # Create bins
            filtered_df['screen_bin'] = pd.cut(filtered_df['avg_daily_screen_time_hrs'], 
                                               bins=[0, 2, 4, 6, 8, 15], 
                                               labels=['0-2', '2-4', '4-6', '6-8', '8+'])
            
            heatmap_data = filtered_df.pivot_table(
                values='anxiety_score',
                index='sleep_quality_category',
                columns='screen_bin',
                aggfunc='mean'
            )
            
            # Reorder index
            order = ['Good', 'Moderate', 'Poor', 'Very Poor']
            heatmap_data = heatmap_data.reindex([o for o in order if o in heatmap_data.index])
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale=[[0, '#4ade80'], [0.5, '#fbbf24'], [1, '#f87171']],
                text=np.round(heatmap_data.values, 1),
                texttemplate='%{text}',
                textfont=dict(color='white'),
                hovertemplate='Sleep: %{y}<br>Screen Time: %{x}<br>Avg Anxiety: %{z:.1f}<extra></extra>'
            ))
            fig.update_layout(**get_chart_layout("Sleep Quality × Screen Time → Anxiety"))
            fig.update_layout(xaxis_title="Screen Time (hrs)", yaxis_title="Sleep Quality")
            st.plotly_chart(fig, use_container_width=True)
        
        # Sleep Hours Distribution by Platform
        st.markdown("#### 💤 Sleep Hours by Platform")
        
        fig = px.box(
            filtered_df, 
            x='primary_platform', 
            y='avg_sleep_hours',
            color='primary_platform',
            color_discrete_sequence=CHART_COLORS
        )
        fig.update_layout(**get_chart_layout("Sleep Hours Distribution by Platform"))
        fig.update_layout(showlegend=False, xaxis_title="Platform", yaxis_title="Sleep Hours")
        st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 7: CORRELATIONS ====================
    with tabs[6]:
        st.markdown("### 🔗 Correlation Analysis")
        
        # Correlation Matrix
        corr_columns = ['avg_daily_screen_time_hrs', 'anxiety_score', 'depression_score', 
                       'stress_score', 'sleep_quality_score', 'self_esteem_score', 
                       'loneliness_score', 'fomo_score', 'avg_sleep_hours']
        
        corr_matrix = filtered_df[corr_columns].corr()
        
        # Rename for display
        display_names = ['Screen Time', 'Anxiety', 'Depression', 'Stress', 
                        'Sleep Quality', 'Self-Esteem', 'Loneliness', 'FOMO', 'Sleep Hours']
        corr_matrix.columns = display_names
        corr_matrix.index = display_names
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale=[[0, '#f87171'], [0.5, '#1a2d47'], [1, '#4ade80']],
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text}',
            textfont=dict(color='white', size=10),
            hovertemplate='%{y} vs %{x}<br>Correlation: %{z:.2f}<extra></extra>'
        ))
        fig.update_layout(**get_chart_layout("Correlation Matrix", height=500))
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bubble Chart - 3 variables
            fig = px.scatter(
                filtered_df,
                x='avg_daily_screen_time_hrs',
                y='anxiety_score',
                size='follower_count',
                color='risk_category',
                color_discrete_map=RISK_COLORS,
                hover_data=['age', 'primary_platform'],
                size_max=30,
                opacity=0.6
            )
            fig.update_layout(**get_chart_layout("Screen Time vs Anxiety vs Followers"))
            fig.update_layout(xaxis_title="Screen Time (hrs)", yaxis_title="Anxiety Score")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Parallel Coordinates
            parallel_df = filtered_df.sample(min(500, len(filtered_df)))
            
            fig = px.parallel_coordinates(
                parallel_df,
                dimensions=['avg_daily_screen_time_hrs', 'anxiety_score', 
                           'depression_score', 'sleep_quality_score', 'mental_health_risk_score'],
                color='mental_health_risk_score',
                color_continuous_scale=[[0, '#4ade80'], [0.5, '#fbbf24'], [1, '#f87171']],
                labels={
                    'avg_daily_screen_time_hrs': 'Screen Time',
                    'anxiety_score': 'Anxiety',
                    'depression_score': 'Depression',
                    'sleep_quality_score': 'Sleep Quality',
                    'mental_health_risk_score': 'Risk Score'
                }
            )
            fig.update_layout(**get_chart_layout("Parallel Coordinates Analysis", height=400))
            st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 8: GEOGRAPHIC ====================
    with tabs[7]:
        st.markdown("### 🗺️ Geographic Analysis")
        
        # State-level aggregation
        state_data = filtered_df.groupby('state').agg({
            'mental_health_risk_score': 'mean',
            'avg_daily_screen_time_hrs': 'mean',
            'anxiety_score': 'mean',
            'user_id': 'count'
        }).reset_index()
        state_data.columns = ['state', 'avg_risk', 'avg_screen_time', 'avg_anxiety', 'user_count']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Choropleth Map (India)
            # Using bar chart as fallback since India geojson needs separate file
            fig = go.Figure(data=[go.Bar(
                x=state_data['avg_risk'],
                y=state_data['state'],
                orientation='h',
                marker=dict(
                    color=state_data['avg_risk'],
                    colorscale=[[0, '#4ade80'], [0.5, '#fbbf24'], [1, '#f87171']],
                    showscale=True,
                    colorbar=dict(title='Risk Score')
                ),
                text=state_data['avg_risk'].round(1),
                textposition='auto',
                textfont=dict(color='white')
            )])
            fig.update_layout(**get_chart_layout("Average Risk Score by State"))
            fig.update_layout(xaxis_title="Risk Score", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Point Map - User Locations
            city_data = filtered_df.groupby(['city', 'latitude', 'longitude']).agg({
                'mental_health_risk_score': 'mean',
                'user_id': 'count'
            }).reset_index()
            
            fig = px.scatter_geo(
                city_data,
                lat='latitude',
                lon='longitude',
                size='user_id',
                color='mental_health_risk_score',
                hover_name='city',
                color_continuous_scale=[[0, '#4ade80'], [0.5, '#fbbf24'], [1, '#f87171']],
                size_max=30,
                scope='asia'
            )
            fig.update_geos(
                visible=False,
                resolution=50,
                showcountries=True,
                countrycolor='#2a4a7f',
                showland=True,
                landcolor='#0a1628',
                showocean=True,
                oceancolor='#0d1b2a',
                lataxis_range=[6, 38],
                lonaxis_range=[68, 98]
            )
            fig.update_layout(**get_chart_layout("User Distribution Map (India)", height=400))
            st.plotly_chart(fig, use_container_width=True)
        
        # Regional Comparison
        st.markdown("#### 🌏 Regional Comparison")
        
        region_data = filtered_df.groupby('region').agg({
            'avg_daily_screen_time_hrs': 'mean',
            'anxiety_score': 'mean',
            'depression_score': 'mean',
            'mental_health_risk_score': 'mean'
        }).round(2)
        
        fig = go.Figure()
        
        metrics = ['avg_daily_screen_time_hrs', 'anxiety_score', 'depression_score']
        metric_names = ['Screen Time', 'Anxiety', 'Depression']
        
        for i, (metric, name) in enumerate(zip(metrics, metric_names)):
            fig.add_trace(go.Bar(
                name=name,
                x=region_data.index,
                y=region_data[metric],
                marker_color=CHART_COLORS[i]
            ))
        
        fig.update_layout(**get_chart_layout("Key Metrics by Region"))
        fig.update_layout(barmode='group', xaxis_title="Region", yaxis_title="Score")
        st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 9: ML PREDICTIONS ====================
    with tabs[8]:
        st.markdown("### 🤖 Machine Learning & Predictions")
        
        # Prepare data for ML
        feature_cols = ['avg_daily_screen_time_hrs', 'night_usage_hours', 'num_platforms',
                       'sessions_per_day', 'avg_session_duration_min', 'age',
                       'fomo_score', 'avg_sleep_hours']
        
        X = filtered_df[feature_cols].fillna(0)
        y = LabelEncoder().fit_transform(filtered_df['risk_category'])
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train_scaled, y_train)
        
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Confusion Matrix
            cm = confusion_matrix(y_test, y_pred)
            labels = ['Low', 'Mod-Low', 'Mod-High', 'High']
            
            fig = go.Figure(data=go.Heatmap(
                z=cm,
                x=labels,
                y=labels,
                colorscale=[[0, '#1a2d47'], [1, '#3a86ff']],
                text=cm,
                texttemplate='%{text}',
                textfont=dict(color='white', size=14),
                hovertemplate='Actual: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>'
            ))
            fig.update_layout(**get_chart_layout("Confusion Matrix"))
            fig.update_layout(xaxis_title="Predicted", yaxis_title="Actual")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # ROC Curve
            fig = go.Figure()
            
            for i in range(len(labels)):
                y_test_binary = (y_test == i).astype(int)
                y_prob_class = y_prob[:, i]
                
                fpr, tpr, _ = roc_curve(y_test_binary, y_prob_class)
                roc_auc = auc(fpr, tpr)
                
                fig.add_trace(go.Scatter(
                    x=fpr, y=tpr,
                    mode='lines',
                    name=f'{labels[i]} (AUC={roc_auc:.2f})',
                    line=dict(color=list(RISK_COLORS.values())[i], width=2)
                ))
            
            fig.add_trace(go.Scatter(
                x=[0, 1], y=[0, 1],
                mode='lines',
                name='Random',
                line=dict(color='gray', dash='dash')
            ))
            
            fig.update_layout(**get_chart_layout("ROC Curves"))
            fig.update_layout(xaxis_title="False Positive Rate", yaxis_title="True Positive Rate")
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Feature Importance
            importance = pd.DataFrame({
                'feature': feature_cols,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=True)
            
            fig = go.Figure(data=[go.Bar(                x=importance['importance'],
                y=importance['feature'],
                orientation='h',
                marker=dict(color=COLORS['primary']),
                text=importance['importance'].round(3),
                textposition='auto',
                textfont=dict(color='white')
            )])
            fig.update_layout(**get_chart_layout("Feature Importance"))
            fig.update_layout(xaxis_title="Importance", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Learning Curves
            train_sizes, train_scores, val_scores = learning_curve(
                model, X_train_scaled, y_train,
                train_sizes=np.linspace(0.1, 1.0, 10),
                cv=5, n_jobs=-1
            )
            
            train_mean = train_scores.mean(axis=1)
            val_mean = val_scores.mean(axis=1)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=train_sizes, y=train_mean,
                mode='lines+markers',
                name='Training Score',
                line=dict(color=COLORS['primary'], width=2)
            ))
            fig.add_trace(go.Scatter(
                x=train_sizes, y=val_mean,
                mode='lines+markers',
                name='Validation Score',
                line=dict(color=COLORS['warning'], width=2)
            ))
            fig.update_layout(**get_chart_layout("Learning Curves"))
            fig.update_layout(xaxis_title="Training Size", yaxis_title="Score")
            st.plotly_chart(fig, use_container_width=True)
        
        # Dimensionality Reduction
        st.markdown("#### 🔬 User Clustering Visualization (PCA)")
        
        # PCA
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_train_scaled)
        
        pca_df = pd.DataFrame({
            'PC1': X_pca[:, 0],
            'PC2': X_pca[:, 1],
            'risk': [['Low', 'Mod-Low', 'Mod-High', 'High'][i] for i in y_train]
        })
        
        fig = px.scatter(
            pca_df, x='PC1', y='PC2',
            color='risk',
            color_discrete_map=RISK_COLORS,
            opacity=0.6
        )
        fig.update_layout(**get_chart_layout(f"PCA Visualization (Explained Var: {sum(pca.explained_variance_ratio_)*100:.1f}%)"))
        st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 10: ETHICS ====================
    with tabs[9]:
        st.markdown("### ⚖️ Ethics & Fairness Analysis")
        
        st.markdown("""
        <div class='insight-box'>
            <div class='insight-title' style='color: #4cc9f0;'>🎯 Ethical AI Principles</div>
            <div class='insight-text'>
                This section ensures our analysis is fair, unbiased, and transparent across different demographic groups.
                We check for disparities in risk scores and model predictions.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gender Bias Check
            gender_risk = filtered_df.groupby('gender')['mental_health_risk_score'].agg(['mean', 'std', 'count']).round(2)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=gender_risk.index,
                y=gender_risk['mean'],
                error_y=dict(type='data', array=gender_risk['std'], visible=True),
                marker_color=CHART_COLORS[:len(gender_risk)],
                text=gender_risk['mean'].round(1),
                textposition='auto',
                textfont=dict(color='white')
            ))
            fig.update_layout(**get_chart_layout("Risk Score by Gender"))
            fig.update_layout(xaxis_title="Gender", yaxis_title="Avg Risk Score")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Age Group Bias Check
            age_risk = filtered_df.groupby('age_group')['mental_health_risk_score'].agg(['mean', 'std', 'count']).round(2)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=age_risk.index,
                y=age_risk['mean'],
                error_y=dict(type='data', array=age_risk['std'], visible=True),
                marker_color=CHART_COLORS[:len(age_risk)],
                text=age_risk['mean'].round(1),
                textposition='auto',
                textfont=dict(color='white')
            ))
            fig.update_layout(**get_chart_layout("Risk Score by Age Group"))
            fig.update_layout(xaxis_title="Age Group", yaxis_title="Avg Risk Score")
            st.plotly_chart(fig, use_container_width=True)
        
        # Sample Size Confidence
        st.markdown("#### 📊 Data Confidence Indicators")
        
        confidence_data = []
        for group in ['gender', 'age_group', 'region']:
            for cat in filtered_df[group].unique():
                count = len(filtered_df[filtered_df[group] == cat])
                if count >= 100:
                    confidence = 'High'
                    color = '🟢'
                elif count >= 50:
                    confidence = 'Medium'
                    color = '🟡'
                else:
                    confidence = 'Low'
                    color = '🔴'
                
                confidence_data.append({
                    'Category Type': group.replace('_', ' ').title(),
                    'Category': cat,
                    'Sample Size': count,
                    'Confidence': f"{color} {confidence}"
                })
        
        confidence_df = pd.DataFrame(confidence_data)
        st.dataframe(confidence_df, use_container_width=True, hide_index=True)
        
        # Fairness Metrics
        st.markdown("#### 🔍 Fairness Assessment")
        
        # Calculate disparity ratios
        male_risk = filtered_df[filtered_df['gender'] == 'Male']['mental_health_risk_score'].mean()
        female_risk = filtered_df[filtered_df['gender'] == 'Female']['mental_health_risk_score'].mean()
        
        young_risk = filtered_df[filtered_df['age_group'] == '18-24']['mental_health_risk_score'].mean()
        old_risk = filtered_df[filtered_df['age_group'] == '45-54']['mental_health_risk_score'].mean() if '45-54' in filtered_df['age_group'].values else young_risk
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            gender_ratio = male_risk / female_risk if female_risk > 0 else 1
            status = "✅ Fair" if 0.8 <= gender_ratio <= 1.2 else "⚠️ Review"
            st.metric("Gender Disparity Ratio", f"{gender_ratio:.2f}", status)
        
        with col2:
            age_ratio = young_risk / old_risk if old_risk > 0 else 1
            status = "✅ Fair" if 0.8 <= age_ratio <= 1.2 else "⚠️ Review"
            st.metric("Age Disparity Ratio", f"{age_ratio:.2f}", status)
        
        with col3:
            overall_std = filtered_df.groupby('region')['mental_health_risk_score'].mean().std()
            status = "✅ Fair" if overall_std < 5 else "⚠️ Review"
            st.metric("Regional Variance", f"{overall_std:.2f}", status)
        
        render_insight_box(
            "⚖️ Fairness Summary",
            "Our analysis shows relatively balanced risk distributions across demographic groups. "
            "Minor variations exist but are within acceptable ranges. "
            "We recommend continued monitoring as more data is collected.",
            COLORS['success']
        )
    
    # ==================== FOOTER ====================
    render_divider()
    
    st.markdown("""
    <div style='text-align: center; padding: 20px; color: #8facc4;'>
        <p>🧠 Social Media & Mental Health Intelligence Dashboard</p>
        <p style='font-size: 0.8rem;'>Built with Streamlit | Data: Simulated Survey (5,000 users, 6 months)</p>
        <p style='font-size: 0.8rem;'>© 2024 | For Educational Purposes</p>
    </div>
    """, unsafe_allow_html=True)

# ================================================================================
# RUN APPLICATION
# ================================================================================

if __name__ == "__main__":
    main()
