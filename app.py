# ============================================================
# AI IN THE FUTURE OF WORK - INTERACTIVE DASHBOARD
# India & UAE Workforce Analysis
# ============================================================
# Complete Streamlit Dashboard with 7 Pages & 39 Visualizations
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI & Future of Work Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# COLORBLIND-SAFE COLOR PALETTES
# ============================================================

COLORS = {
    # IBM Design Library - Colorblind Safe
    'categorical': ['#648FFF', '#785EF0', '#DC267F', '#FE6100', '#FFB000', 
                    '#22A884', '#414487', '#7AD151'],
    
    # Extended categorical (for more categories)
    'categorical_extended': ['#648FFF', '#785EF0', '#DC267F', '#FE6100', '#FFB000',
                             '#22A884', '#414487', '#7AD151', '#2E91E5', '#E15F99',
                             '#1CA71C', '#FB0D0D'],
    
    # Sequential (for continuous data - low to high)
    'sequential_blue': ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', 
                        '#6baed6', '#4292c6', '#2171b5', '#084594'],
    
    # Diverging (for data with meaningful center)
    'diverging': ['#d73027', '#f46d43', '#fdae61', '#fee08b', 
                  '#ffffbf', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850'],
    
    # Risk scale (low to high risk)
    'risk': ['#1a9850', '#66bd63', '#a6d96a', '#d9ef8b', 
             '#fee08b', '#fdae61', '#f46d43', '#d73027'],
    
    # Binary comparisons
    'india_uae': ['#648FFF', '#DC267F'],
    
    # Positive/Negative
    'pos_neg': ['#1a9850', '#d73027'],
    
    # Single highlight
    'primary': '#648FFF',
    'secondary': '#DC267F',
    'accent': '#FFB000',
    
    # Background colors for insights
    'insight_bg': '#f0f7ff',
    'insight_border': '#648FFF'
}

# ============================================================
# CUSTOM CSS STYLING
# ============================================================

st.markdown("""
<style>
    /* Main container */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }
    
    /* Headers */
    h1 {
        color: #1f4e79;
        font-weight: 700;
        border-bottom: 3px solid #648FFF;
        padding-bottom: 10px;
    }
    
    h2 {
        color: #2e5a8a;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #3a6a9a;
        font-weight: 500;
    }
    
    /* KPI Card Styling */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Insight Box */
    .insight-box {
        background-color: #f0f7ff;
        border-left: 4px solid #648FFF;
        padding: 15px 20px;
        margin: 15px 0;
        border-radius: 0 8px 8px 0;
    }
    
    .insight-title {
        color: #648FFF;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 8px;
    }
    
    .insight-text {
        color: #333;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f5f7fa;
    }
    
    /* Metric delta colors */
    [data-testid="stMetricDelta"] svg {
        stroke: currentColor;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def display_insight(finding: str, implication: str):
    """Display a formatted insight box after each chart"""
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">📌 Key Insight</div>
        <div class="insight-text">
            <strong>Finding:</strong> {finding}<br><br>
            <strong>Implication:</strong> {implication}
        </div>
    </div>
    """, unsafe_allow_html=True)

def format_number(num, prefix="", suffix=""):
    """Format large numbers with K, M suffixes"""
    if num >= 1_000_000:
        return f"{prefix}{num/1_000_000:.1f}M{suffix}"
    elif num >= 1_000:
        return f"{prefix}{num/1_000:.1f}K{suffix}"
    else:
        return f"{prefix}{num:.1f}{suffix}"

def create_kpi_card(value, label, delta=None, delta_color="normal"):
    """Create a styled KPI metric"""
    st.metric(label=label, value=value, delta=delta, delta_color=delta_color)

def get_risk_color(score):
    """Return color based on risk score"""
    if score < 30:
        return '#1a9850'  # Green - Low risk
    elif score < 50:
        return '#a6d96a'  # Light green
    elif score < 70:
        return '#fdae61'  # Orange
    else:
        return '#d73027'  # Red - High risk

def generate_sparkline(data, color='#648FFF'):
    """Generate a simple sparkline figure"""
    fig = go.Figure(go.Scatter(
        y=data,
        mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=f'rgba(100, 143, 255, 0.2)'
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=50,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# Standard Plotly configuration for interactivity
PLOTLY_CONFIG = {
    'displayModeBar': True,
    'modeBarButtonsToInclude': ['zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d',
                                 'autoScale2d', 'resetScale2d', 'toImage'],
    'displaylogo': False,
    'responsive': True
}

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    """Load and cache the dataset"""
    df = pd.read_csv('ai_future_of_work_india_uae.csv')
    return df

# ============================================================
# GEOJSON DATA FOR MAPS
# ============================================================

@st.cache_data
def load_india_geojson():
    """Load India states GeoJSON"""
    # Simplified India GeoJSON - coordinates for major states
    # In production, use full GeoJSON file
    india_geojson = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "properties": {"state_name": "Maharashtra", "state_code": "MH"}, 
             "geometry": {"type": "Point", "coordinates": [75.7139, 19.7515]}},
            {"type": "Feature", "properties": {"state_name": "Karnataka", "state_code": "KA"}, 
             "geometry": {"type": "Point", "coordinates": [75.7139, 15.3173]}},
            {"type": "Feature", "properties": {"state_name": "Tamil Nadu", "state_code": "TN"}, 
             "geometry": {"type": "Point", "coordinates": [78.6569, 11.1271]}},
            {"type": "Feature", "properties": {"state_name": "Telangana", "state_code": "TG"}, 
             "geometry": {"type": "Point", "coordinates": [79.0193, 18.1124]}},
            {"type": "Feature", "properties": {"state_name": "Delhi NCT", "state_code": "DL"}, 
             "geometry": {"type": "Point", "coordinates": [77.1025, 28.7041]}},
            {"type": "Feature", "properties": {"state_name": "Gujarat", "state_code": "GJ"}, 
             "geometry": {"type": "Point", "coordinates": [71.1924, 22.2587]}},
            {"type": "Feature", "properties": {"state_name": "Haryana", "state_code": "HR"}, 
             "geometry": {"type": "Point", "coordinates": [76.0856, 29.0588]}},
            {"type": "Feature", "properties": {"state_name": "West Bengal", "state_code": "WB"}, 
             "geometry": {"type": "Point", "coordinates": [87.8550, 22.9868]}},
            {"type": "Feature", "properties": {"state_name": "Uttar Pradesh", "state_code": "UP"}, 
             "geometry": {"type": "Point", "coordinates": [80.9462, 26.8467]}},
            {"type": "Feature", "properties": {"state_name": "Kerala", "state_code": "KL"}, 
             "geometry": {"type": "Point", "coordinates": [76.2711, 10.8505]}},
            {"type": "Feature", "properties": {"state_name": "Rajasthan", "state_code": "RJ"}, 
             "geometry": {"type": "Point", "coordinates": [74.2179, 27.0238]}},
            {"type": "Feature", "properties": {"state_name": "Madhya Pradesh", "state_code": "MP"}, 
             "geometry": {"type": "Point", "coordinates": [78.6569, 22.9734]}},
            {"type": "Feature", "properties": {"state_name": "Punjab", "state_code": "PB"}, 
             "geometry": {"type": "Point", "coordinates": [75.3412, 31.1471]}},
            {"type": "Feature", "properties": {"state_name": "Andhra Pradesh", "state_code": "AP"}, 
             "geometry": {"type": "Point", "coordinates": [79.7400, 15.9129]}},
            {"type": "Feature", "properties": {"state_name": "Bihar", "state_code": "BR"}, 
             "geometry": {"type": "Point", "coordinates": [85.3131, 25.0961]}},
        ]
    }
    return india_geojson

@st.cache_data  
def load_uae_geojson():
    """Load UAE emirates GeoJSON"""
    uae_geojson = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "properties": {"emirate_name": "Dubai", "emirate_code": "DXB"}, 
             "geometry": {"type": "Point", "coordinates": [55.2708, 25.2048]}},
            {"type": "Feature", "properties": {"emirate_name": "Abu Dhabi", "emirate_code": "AUH"}, 
             "geometry": {"type": "Point", "coordinates": [54.3773, 24.4539]}},
            {"type": "Feature", "properties": {"emirate_name": "Sharjah", "emirate_code": "SHJ"}, 
             "geometry": {"type": "Point", "coordinates": [55.4033, 25.3463]}},
            {"type": "Feature", "properties": {"emirate_name": "Ajman", "emirate_code": "AJM"}, 
             "geometry": {"type": "Point", "coordinates": [55.5136, 25.4052]}},
            {"type": "Feature", "properties": {"emirate_name": "Ras Al Khaimah", "emirate_code": "RAK"}, 
             "geometry": {"type": "Point", "coordinates": [55.9432, 25.7895]}},
            {"type": "Feature", "properties": {"emirate_name": "Fujairah", "emirate_code": "FUJ"}, 
             "geometry": {"type": "Point", "coordinates": [56.3264, 25.1288]}},
            {"type": "Feature", "properties": {"emirate_name": "Umm Al Quwain", "emirate_code": "UAQ"}, 
             "geometry": {"type": "Point", "coordinates": [55.5475, 25.5647]}},
        ]
    }
    return uae_geojson

# State coordinates for India map
INDIA_STATE_COORDS = {
    'Maharashtra': [19.7515, 75.7139],
    'Karnataka': [15.3173, 75.7139],
    'Tamil Nadu': [11.1271, 78.6569],
    'Telangana': [18.1124, 79.0193],
    'Delhi NCT': [28.7041, 77.1025],
    'Gujarat': [22.2587, 71.1924],
    'Haryana': [29.0588, 76.0856],
    'West Bengal': [22.9868, 87.8550],
    'Uttar Pradesh': [26.8467, 80.9462],
    'Kerala': [10.8505, 76.2711],
    'Rajasthan': [27.0238, 74.2179],
    'Madhya Pradesh': [22.9734, 78.6569],
    'Punjab': [31.1471, 75.3412],
    'Andhra Pradesh': [15.9129, 79.7400],
    'Bihar': [25.0961, 85.3131],
    'Odisha': [20.9517, 85.0985],
    'Jharkhand': [23.6102, 85.2799],
    'Chhattisgarh': [21.2787, 81.8661],
    'Assam': [26.2006, 92.9376],
    'Uttarakhand': [30.0668, 79.0193],
    'Himachal Pradesh': [31.1048, 77.1734],
    'Goa': [15.2993, 74.1240],
    'Chandigarh': [30.7333, 76.7794],
    'Puducherry': [11.9416, 79.8083],
    'Jammu and Kashmir': [33.7782, 76.5762],
    'Tripura': [23.9408, 91.9882],
    'Meghalaya': [25.4670, 91.3662],
    'Manipur': [24.6637, 93.9063],
    'Nagaland': [26.1584, 94.5624],
    'Arunachal Pradesh': [28.2180, 94.7278],
    'Mizoram': [23.1645, 92.9376],
    'Sikkim': [27.5330, 88.5122],
    'Ladakh': [34.1526, 77.5771],
    'Andaman and Nicobar Islands': [11.7401, 92.6586],
    'Lakshadweep': [10.5667, 72.6417],
    'Dadra and Nagar Haveli and Daman and Diu': [20.1809, 73.0169]
}

# UAE emirate coordinates
UAE_EMIRATE_COORDS = {
    'Dubai': [25.2048, 55.2708],
    'Abu Dhabi': [24.4539, 54.3773],
    'Sharjah': [25.3463, 55.4033],
    'Ajman': [25.4052, 55.5136],
    'Ras Al Khaimah': [25.7895, 55.9432],
    'Fujairah': [25.1288, 56.3264],
    'Umm Al Quwain': [25.5647, 55.5475]
}

# ============================================================
# LOAD DATA
# ============================================================

df = load_data()

# ============================================================
# SIDEBAR - FILTERS & NAVIGATION
# ============================================================

st.sidebar.title("🤖 AI & Future of Work")
st.sidebar.markdown("---")

# Page Navigation
st.sidebar.subheader("📑 Navigation")
page = st.sidebar.radio(
    "Select Page:",
    [
        "📌 Executive Summary",
        "📊 Automation Risk Analysis",
        "💼 Skills & Training",
        "💰 Economic Impact",
        "🧠 Workforce Sentiment",
        "🌍 Geographic Analysis",
        "🤖 AI/ML Analytics"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Global Filters
st.sidebar.subheader("🔍 Filters")

# Country Filter
country_options = ['All'] + sorted(df['country'].unique().tolist())
selected_country = st.sidebar.selectbox("Country", country_options)

# State/Emirate Filter (dynamic based on country)
if selected_country == 'All':
    state_options = ['All'] + sorted(df['state_emirate'].unique().tolist())
elif selected_country == 'India':
    state_options = ['All'] + sorted(df[df['country'] == 'India']['state_emirate'].unique().tolist())
else:
    state_options = ['All'] + sorted(df[df['country'] == 'UAE']['state_emirate'].unique().tolist())
selected_state = st.sidebar.selectbox("State/Emirate", state_options)

# Industry Filter
industry_options = ['All'] + sorted(df['industry'].unique().tolist())
selected_industry = st.sidebar.selectbox("Industry", industry_options)

# Job Level Filter
job_level_options = ['All'] + sorted(df['job_level'].unique().tolist(), 
                                      key=lambda x: ['Entry', 'Junior', 'Mid', 'Senior', 
                                                     'Lead', 'Manager', 'Director', 'Executive'].index(x))
selected_job_level = st.sidebar.selectbox("Job Level", job_level_options)

# Company Size Filter
company_size_options = ['All'] + ['Startup', 'Small', 'Medium', 'Large', 'Enterprise']
selected_company_size = st.sidebar.selectbox("Company Size", company_size_options)

# Age Group Filter
age_options = ['All'] + sorted(df['age_group'].unique().tolist())
selected_age = st.sidebar.selectbox("Age Group", age_options)

# Year Range Filter
year_min = int(df['observation_year'].min())
year_max = int(df['observation_year'].max())
selected_years = st.sidebar.slider("Observation Year", year_min, year_max, (year_min, year_max))

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['country'] == selected_country]

if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['state_emirate'] == selected_state]

if selected_industry != 'All':
    filtered_df = filtered_df[filtered_df['industry'] == selected_industry]

if selected_job_level != 'All':
    filtered_df = filtered_df[filtered_df['job_level'] == selected_job_level]

if selected_company_size != 'All':
    filtered_df = filtered_df[filtered_df['company_size'] == selected_company_size]

if selected_age != 'All':
    filtered_df = filtered_df[filtered_df['age_group'] == selected_age]

filtered_df = filtered_df[
    (filtered_df['observation_year'] >= selected_years[0]) & 
    (filtered_df['observation_year'] <= selected_years[1])
]

# Show filter summary
st.sidebar.markdown("---")
st.sidebar.markdown(f"**📊 Filtered Records:** {len(filtered_df):,} / {len(df):,}")

# Download filtered data
st.sidebar.markdown("---")
st.sidebar.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='filtered_workforce_data.csv',
    mime='text/csv'
)

# ============================================================
# PAGE 1: EXECUTIVE SUMMARY
# ============================================================

if page == "📌 Executive Summary":
    
    st.title("📌 Executive Summary")
    st.markdown("### AI Impact on Workforce: India & UAE Overview")
    st.markdown("---")
    
    # ========== ROW 1: KPI CARDS WITH SPARKLINES ==========
    
    st.subheader("Key Performance Indicators")
    
    kpi_cols = st.columns(5)
    
    with kpi_cols[0]:
        st.metric(
            label="Total Workers Analyzed",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df)/len(df)*100:.0f}% of dataset"
        )
        # Sparkline - records by year
        yearly_counts = filtered_df.groupby('observation_year').size().values
        if len(yearly_counts) > 1:
            st.plotly_chart(generate_sparkline(yearly_counts), use_container_width=True, config={'displayModeBar': False})
    
    with kpi_cols[1]:
        avg_risk = filtered_df['automation_risk_score'].mean()
        st.metric(
            label="Avg. Automation Risk",
            value=f"{avg_risk:.1f}",
            delta=f"{avg_risk - df['automation_risk_score'].mean():.1f} vs overall",
            delta_color="inverse"
        )
        # Sparkline
        risk_by_year = filtered_df.groupby('observation_year')['automation_risk_score'].mean().values
        if len(risk_by_year) > 1:
            st.plotly_chart(generate_sparkline(risk_by_year, '#DC267F'), use_container_width=True, config={'displayModeBar': False})
    
    with kpi_cols[2]:
        avg_salary = filtered_df['annual_salary_usd'].mean()
        st.metric(
            label="Avg. Salary (USD)",
            value=f"${avg_salary:,.0f}",
            delta=f"{((avg_salary/df['annual_salary_usd'].mean())-1)*100:.1f}%"
        )
        # Sparkline
        salary_by_year = filtered_df.groupby('observation_year')['annual_salary_usd'].mean().values
        if len(salary_by_year) > 1:
            st.plotly_chart(generate_sparkline(salary_by_year, '#22A884'), use_container_width=True, config={'displayModeBar': False})
    
    with kpi_cols[3]:
        avg_ai_lit = filtered_df['ai_literacy_score'].mean()
        st.metric(
            label="Avg. AI Literacy",
            value=f"{avg_ai_lit:.1f}",
            delta=f"{avg_ai_lit - df['ai_literacy_score'].mean():.1f} vs overall"
        )
        # Sparkline
        ai_by_year = filtered_df.groupby('observation_year')['ai_literacy_score'].mean().values
        if len(ai_by_year) > 1:
            st.plotly_chart(generate_sparkline(ai_by_year, '#785EF0'), use_container_width=True, config={'displayModeBar': False})
    
    with kpi_cols[4]:
        high_growth_pct = (filtered_df['demand_forecast_2030'].isin(['Growing', 'High Growth'])).mean() * 100
        st.metric(
            label="Jobs with Growth Outlook",
            value=f"{high_growth_pct:.1f}%",
            delta="2030 Forecast"
        )
        # Sparkline
        growth_by_year = filtered_df.groupby('observation_year').apply(
            lambda x: (x['demand_forecast_2030'].isin(['Growing', 'High Growth'])).mean() * 100
        ).values
        if len(growth_by_year) > 1:
            st.plotly_chart(generate_sparkline(growth_by_year, '#FFB000'), use_container_width=True, config={'displayModeBar': False})
    
    display_insight(
        f"The filtered dataset contains {len(filtered_df):,} workers with an average automation risk of {avg_risk:.1f}/100 and average salary of ${avg_salary:,.0f}.",
        f"With {high_growth_pct:.1f}% of jobs showing positive growth outlook for 2030, targeted upskilling in AI-related competencies can help secure workforce stability."
    )
    
    st.markdown("---")
    
    # ========== ROW 2: PIE CHART & DONUT CHART ==========
    
    col1, col2 = st.columns(2)
    
    # 1.2 PIE CHART - Country Distribution
    with col1:
        st.subheader("Country Distribution")
        
        country_counts = filtered_df['country'].value_counts()
        
        fig_pie = px.pie(
            values=country_counts.values,
            names=country_counts.index,
            color_discrete_sequence=COLORS['india_uae'],
            hole=0  # Solid pie chart
        )
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>'
        )
        fig_pie.update_layout(
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=-0.2),
            margin=dict(t=20, b=20, l=20, r=20),
            height=350
        )
        st.plotly_chart(fig_pie, use_container_width=True, config=PLOTLY_CONFIG)
        
        india_pct = country_counts.get('India', 0) / len(filtered_df) * 100
        uae_pct = country_counts.get('UAE', 0) / len(filtered_df) * 100
        
        display_insight(
            f"India represents {india_pct:.1f}% of the workforce data while UAE accounts for {uae_pct:.1f}%.",
            "This distribution reflects the relative workforce sizes and provides substantial data for meaningful country-level comparisons."
        )
    
    # 1.3 DONUT CHART - Employment Type
    with col2:
        st.subheader("Employment Type Distribution")
        
        emp_counts = filtered_df['employment_type'].value_counts()
        
        fig_donut = px.pie(
            values=emp_counts.values,
            names=emp_counts.index,
            color_discrete_sequence=COLORS['categorical'],
            hole=0.5  # Donut chart
        )
        fig_donut.update_traces(
            textposition='outside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>'
        )
        fig_donut.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            height=350,
            annotations=[dict(text=f'{len(filtered_df):,}<br>Workers', 
                             x=0.5, y=0.5, font_size=16, showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True, config=PLOTLY_CONFIG)
        
        fulltime_pct = emp_counts.get('Full-time', 0) / len(filtered_df) * 100
        
        display_insight(
            f"Full-time employment dominates at {fulltime_pct:.1f}%, with contract and freelance work representing the gig economy segment.",
            "The growing gig economy requires different AI adoption strategies and reskilling approaches compared to traditional employment."
        )
    
    st.markdown("---")
    
    # ========== ROW 3: BAR CHART - TOP INDUSTRIES ==========
    
    st.subheader("Workforce Distribution by Industry")
    
    industry_counts = filtered_df['industry'].value_counts().head(10)
    industry_risk = filtered_df.groupby('industry')['automation_risk_score'].mean()
    
    fig_bar = go.Figure()
    
    # Add bars with color based on risk
    colors = [get_risk_color(industry_risk.get(ind, 50)) for ind in industry_counts.index]
    
    fig_bar.add_trace(go.Bar(
        x=industry_counts.values,
        y=industry_counts.index,
        orientation='h',
        marker_color=colors,
        text=[f'{v:,} ({v/len(filtered_df)*100:.1f}%)' for v in industry_counts.values],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Workers: %{x:,}<br>Avg Risk: %{customdata:.1f}<extra></extra>',
        customdata=[industry_risk.get(ind, 0) for ind in industry_counts.index]
    ))
    
    fig_bar.update_layout(
        title=dict(text='Top 10 Industries by Workforce Size (Color = Risk Level)', font=dict(size=14)),
        xaxis_title='Number of Workers',
        yaxis_title='',
        height=450,
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis=dict(categoryorder='total ascending'),
        showlegend=False
    )
    
    st.plotly_chart(fig_bar, use_container_width=True, config=PLOTLY_CONFIG)
    
    top_industry = industry_counts.index[0]
    top_industry_risk = industry_risk.get(top_industry, 0)
    
    display_insight(
        f"{top_industry} leads with {industry_counts.values[0]:,} workers ({industry_counts.values[0]/len(filtered_df)*100:.1f}%). Industries are colored by automation risk (green=low, red=high).",
        f"Workers in high-risk (red) industries should prioritize developing AI-complementary skills to enhance job security."
    )
    
    st.markdown("---")
    
    # ========== ROW 4: LINE CHART - TRENDS OVER TIME ==========
    
    st.subheader("Key Metrics Trend Over Observation Years")
    
    yearly_metrics = filtered_df.groupby('observation_year').agg({
        'automation_risk_score': 'mean',
        'ai_literacy_score': 'mean',
        'annual_salary_usd': 'mean',
        'skill_gap_index': 'mean'
    }).reset_index()
    
    fig_line = go.Figure()
    
    # Normalize for comparison (0-100 scale)
    yearly_metrics['salary_normalized'] = (yearly_metrics['annual_salary_usd'] / yearly_metrics['annual_salary_usd'].max()) * 100
    
    fig_line.add_trace(go.Scatter(
        x=yearly_metrics['observation_year'],
        y=yearly_metrics['automation_risk_score'],
        name='Automation Risk',
        line=dict(color=COLORS['categorical'][2], width=3),
        mode='lines+markers',
        hovertemplate='Year: %{x}<br>Risk Score: %{y:.1f}<extra></extra>'
    ))
    
    fig_line.add_trace(go.Scatter(
        x=yearly_metrics['observation_year'],
        y=yearly_metrics['ai_literacy_score'],
        name='AI Literacy',
        line=dict(color=COLORS['categorical'][1], width=3),
        mode='lines+markers',
        hovertemplate='Year: %{x}<br>AI Literacy: %{y:.1f}<extra></extra>'
    ))
    
    fig_line.add_trace(go.Scatter(
        x=yearly_metrics['observation_year'],
        y=yearly_metrics['skill_gap_index'],
        name='Skill Gap',
        line=dict(color=COLORS['categorical'][3], width=3),
        mode='lines+markers',
        hovertemplate='Year: %{x}<br>Skill Gap: %{y:.1f}<extra></extra>'
    ))
    
    fig_line.update_layout(
        title=dict(text='Trend Analysis: Risk, AI Literacy, and Skill Gap (2020-2030)', font=dict(size=14)),
        xaxis_title='Observation Year',
        yaxis_title='Score (0-100)',
        height=400,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        hovermode='x unified',
        margin=dict(l=20, r=20, t=80, b=20)
    )
    
    st.plotly_chart(fig_line, use_container_width=True, config=PLOTLY_CONFIG)
    
    if len(yearly_metrics) > 1:
        risk_change = yearly_metrics['automation_risk_score'].iloc[-1] - yearly_metrics['automation_risk_score'].iloc[0]
        ai_change = yearly_metrics['ai_literacy_score'].iloc[-1] - yearly_metrics['ai_literacy_score'].iloc[0]
        
        display_insight(
            f"From {int(yearly_metrics['observation_year'].iloc[0])} to {int(yearly_metrics['observation_year'].iloc[-1])}: Automation risk changed by {risk_change:+.1f} points while AI literacy shifted by {ai_change:+.1f} points.",
            "Tracking these trends helps organizations anticipate workforce transformation needs and plan proactive upskilling initiatives."
        )
    
    st.markdown("---")
    
    # ========== ROW 5: HISTOGRAM - RISK DISTRIBUTION ==========
    
    st.subheader("Automation Risk Score Distribution")
    
    fig_hist = px.histogram(
        filtered_df,
        x='automation_risk_score',
        nbins=30,
        color_discrete_sequence=[COLORS['primary']],
        marginal='box'
    )
    
    fig_hist.update_traces(
        hovertemplate='Risk Score: %{x:.0f}<br>Count: %{y}<extra></extra>'
    )
    
    fig_hist.update_layout(
        title=dict(text='Distribution of Automation Risk Scores Across Workforce', font=dict(size=14)),
        xaxis_title='Automation Risk Score (0-100)',
        yaxis_title='Number of Workers',
        height=400,
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    # Add vertical lines for quartiles
    q1 = filtered_df['automation_risk_score'].quantile(0.25)
    median = filtered_df['automation_risk_score'].median()
    q3 = filtered_df['automation_risk_score'].quantile(0.75)
    
    fig_hist.add_vline(x=median, line_dash="dash", line_color=COLORS['secondary'], 
                       annotation_text=f"Median: {median:.1f}")
    
    st.plotly_chart(fig_hist, use_container_width=True, config=PLOTLY_CONFIG)
    
    low_risk = (filtered_df['automation_risk_score'] < 40).sum()
    high_risk = (filtered_df['automation_risk_score'] >= 70).sum()
    
    display_insight(
        f"The risk distribution shows {low_risk:,} workers ({low_risk/len(filtered_df)*100:.1f}%) in the low-risk zone (<40) and {high_risk:,} workers ({high_risk/len(filtered_df)*100:.1f}%) in the high-risk zone (≥70). Median risk is {median:.1f}.",
        f"Organizations should prioritize reskilling programs for the {high_risk:,} high-risk workers while leveraging AI augmentation for those in medium-risk roles."
    )

    # ============================================================
# PAGE 2: AUTOMATION RISK ANALYSIS
# ============================================================

elif page == "📊 Automation Risk Analysis":
    
    st.title("📊 Automation Risk Analysis")
    st.markdown("### Understanding Job Vulnerability to AI & Automation")
    st.markdown("---")
    
    # ========== 2.1 HORIZONTAL BAR CHART - Risk by Industry ==========
    
    st.subheader("2.1 Automation Risk by Industry")
    
    industry_risk = filtered_df.groupby('industry').agg({
        'automation_risk_score': 'mean',
        'record_id': 'count'
    }).reset_index()
    industry_risk.columns = ['Industry', 'Avg Risk Score', 'Worker Count']
    industry_risk = industry_risk.sort_values('Avg Risk Score', ascending=True)
    
    # Create color array based on risk
    colors = [get_risk_color(score) for score in industry_risk['Avg Risk Score']]
    
    fig_ind_risk = go.Figure()
    
    fig_ind_risk.add_trace(go.Bar(
        x=industry_risk['Avg Risk Score'],
        y=industry_risk['Industry'],
        orientation='h',
        marker_color=colors,
        text=[f"{score:.1f}" for score in industry_risk['Avg Risk Score']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Avg Risk Score: %{x:.1f}<br>Workers: %{customdata:,}<extra></extra>',
        customdata=industry_risk['Worker Count']
    ))
    
    fig_ind_risk.update_layout(
        title=dict(
            text='Average Automation Risk Score by Industry<br><sup>Color Scale: Green (Low Risk) → Red (High Risk)</sup>',
            font=dict(size=14)
        ),
        xaxis_title='Average Automation Risk Score (0-100)',
        yaxis_title='',
        height=500,
        margin=dict(l=20, r=80, t=80, b=20),
        xaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig_ind_risk, use_container_width=True, config=PLOTLY_CONFIG)
    
    highest_risk_ind = industry_risk.iloc[-1]
    lowest_risk_ind = industry_risk.iloc[0]
    
    display_insight(
        f"'{highest_risk_ind['Industry']}' has the highest automation risk ({highest_risk_ind['Avg Risk Score']:.1f}), while '{lowest_risk_ind['Industry']}' has the lowest ({lowest_risk_ind['Avg Risk Score']:.1f}). The gap of {highest_risk_ind['Avg Risk Score'] - lowest_risk_ind['Avg Risk Score']:.1f} points indicates significant variation across industries.",
        f"Workers in {highest_risk_ind['Industry']} ({highest_risk_ind['Worker Count']:,} workers) face urgent reskilling needs. Organizations should prioritize AI augmentation training to transition these roles rather than replace them."
    )
    
    st.markdown("---")
    
    # ========== 2.2 BUBBLE CHART - Risk vs Salary vs Count ==========
    
    st.subheader("2.2 Risk vs Salary Analysis (Bubble Size = Worker Count)")
    
    bubble_data = filtered_df.groupby('job_category').agg({
        'automation_risk_score': 'mean',
        'annual_salary_usd': 'mean',
        'record_id': 'count',
        'ai_augmentation_potential': 'mean'
    }).reset_index()
    bubble_data.columns = ['Job Category', 'Avg Risk', 'Avg Salary', 'Count', 'AI Augmentation']
    
    fig_bubble = px.scatter(
        bubble_data,
        x='Avg Risk',
        y='Avg Salary',
        size='Count',
        color='AI Augmentation',
        color_continuous_scale='RdYlGn',
        hover_name='Job Category',
        size_max=60,
        text='Job Category'
    )
    
    fig_bubble.update_traces(
        textposition='top center',
        textfont_size=9,
        hovertemplate='<b>%{hovertext}</b><br>Risk Score: %{x:.1f}<br>Avg Salary: $%{y:,.0f}<br>Workers: %{marker.size:,}<br>AI Augmentation: %{marker.color:.1f}<extra></extra>'
    )
    
    # Add quadrant lines
    median_risk = bubble_data['Avg Risk'].median()
    median_salary = bubble_data['Avg Salary'].median()
    
    fig_bubble.add_hline(y=median_salary, line_dash="dash", line_color="gray", opacity=0.5)
    fig_bubble.add_vline(x=median_risk, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add quadrant annotations
    fig_bubble.add_annotation(x=25, y=bubble_data['Avg Salary'].max()*0.95, 
                              text="🟢 LOW RISK<br>HIGH PAY", showarrow=False, font=dict(size=10, color='green'))
    fig_bubble.add_annotation(x=75, y=bubble_data['Avg Salary'].max()*0.95, 
                              text="🔴 HIGH RISK<br>HIGH PAY", showarrow=False, font=dict(size=10, color='red'))
    fig_bubble.add_annotation(x=25, y=bubble_data['Avg Salary'].min()*1.1, 
                              text="🟡 LOW RISK<br>LOW PAY", showarrow=False, font=dict(size=10, color='orange'))
    fig_bubble.add_annotation(x=75, y=bubble_data['Avg Salary'].min()*1.1, 
                              text="⚠️ HIGH RISK<br>LOW PAY", showarrow=False, font=dict(size=10, color='darkred'))
    
    fig_bubble.update_layout(
        title=dict(
            text='Job Categories: Automation Risk vs. Salary<br><sup>Bubble Size = Worker Count | Color = AI Augmentation Potential</sup>',
            font=dict(size=14)
        ),
        xaxis_title='Average Automation Risk Score (0-100)',
        yaxis_title='Average Annual Salary (USD)',
        height=550,
        margin=dict(l=20, r=20, t=80, b=20),
        coloraxis_colorbar=dict(title='AI Augment<br>Potential')
    )
    
    st.plotly_chart(fig_bubble, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Find concerning quadrant (high risk, low pay)
    high_risk_low_pay = bubble_data[(bubble_data['Avg Risk'] > median_risk) & (bubble_data['Avg Salary'] < median_salary)]
    safe_jobs = bubble_data[(bubble_data['Avg Risk'] < median_risk) & (bubble_data['Avg Salary'] > median_salary)]
    
    display_insight(
        f"The quadrant analysis reveals {len(high_risk_low_pay)} job categories in the 'High Risk-Low Pay' zone requiring urgent attention, while {len(safe_jobs)} categories enjoy 'Low Risk-High Pay' positions.",
        "Workers in the high-risk, low-pay quadrant face a double challenge. Priority should be given to reskilling programs that transition these workers toward AI-augmented roles with better compensation."
    )
    
    st.markdown("---")
    
    # ========== 2.3 VIOLIN PLOT - Risk by Country ==========
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("2.3 Risk Distribution by Country")
        
        fig_violin = px.violin(
            filtered_df,
            x='country',
            y='automation_risk_score',
            color='country',
            color_discrete_sequence=COLORS['india_uae'],
            box=True,
            points='outliers'
        )
        
        fig_violin.update_traces(
            hovertemplate='Country: %{x}<br>Risk Score: %{y:.1f}<extra></extra>'
        )
        
        fig_violin.update_layout(
            title=dict(text='Automation Risk Score Distribution', font=dict(size=13)),
            xaxis_title='',
            yaxis_title='Automation Risk Score',
            height=400,
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig_violin, use_container_width=True, config=PLOTLY_CONFIG)
        
        india_risk = filtered_df[filtered_df['country'] == 'India']['automation_risk_score']
        uae_risk = filtered_df[filtered_df['country'] == 'UAE']['automation_risk_score']
        
        display_insight(
            f"India shows median risk of {india_risk.median():.1f} (IQR: {india_risk.quantile(0.25):.1f}-{india_risk.quantile(0.75):.1f}) vs UAE's {uae_risk.median():.1f} (IQR: {uae_risk.quantile(0.25):.1f}-{uae_risk.quantile(0.75):.1f}).",
            "The distribution shapes reveal workforce composition differences. Wider distributions indicate more diverse job markets in terms of automation exposure."
        )
    
    # ========== 2.4 BOX PLOT - Years to Automation ==========
    
    with col2:
        st.subheader("2.4 Years to Significant Automation")
        
        fig_box = px.box(
            filtered_df,
            x='country',
            y='estimated_years_to_significant_automation',
            color='country',
            color_discrete_sequence=COLORS['india_uae'],
            notched=True
        )
        
        fig_box.update_traces(
            hovertemplate='Country: %{x}<br>Years: %{y}<extra></extra>'
        )
        
        fig_box.update_layout(
            title=dict(text='Timeline to Significant Job Automation', font=dict(size=13)),
            xaxis_title='',
            yaxis_title='Estimated Years',
            height=400,
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig_box, use_container_width=True, config=PLOTLY_CONFIG)
        
        avg_years = filtered_df.groupby('country')['estimated_years_to_significant_automation'].median()
        
        display_insight(
            f"Median time to significant automation: India = {avg_years.get('India', 0):.0f} years, UAE = {avg_years.get('UAE', 0):.0f} years.",
            "This timeline provides a window for workforce transformation. Organizations should use this lead time strategically for structured reskilling programs."
        )
    
    st.markdown("---")
    
    # ========== 2.5 TREEMAP - Job Titles by Risk ==========
    
    st.subheader("2.5 Job Titles Treemap by Automation Risk")
    
    treemap_data = filtered_df.groupby(['job_category', 'job_title']).agg({
        'automation_risk_score': 'mean',
        'record_id': 'count'
    }).reset_index()
    treemap_data.columns = ['Job Category', 'Job Title', 'Avg Risk', 'Count']
    
    fig_treemap = px.treemap(
        treemap_data,
        path=['Job Category', 'Job Title'],
        values='Count',
        color='Avg Risk',
        color_continuous_scale='RdYlGn_r',  # Reversed: green=low, red=high
        hover_data={'Avg Risk': ':.1f', 'Count': ':,'}
    )
    
    fig_treemap.update_traces(
        hovertemplate='<b>%{label}</b><br>Workers: %{value:,}<br>Avg Risk: %{color:.1f}<extra></extra>'
    )
    
    fig_treemap.update_layout(
        title=dict(
            text='Hierarchical View: Job Categories → Job Titles<br><sup>Size = Worker Count | Color = Automation Risk (Green=Low, Red=High)</sup>',
            font=dict(size=14)
        ),
        height=500,
        margin=dict(l=20, r=20, t=80, b=20)
    )
    
    st.plotly_chart(fig_treemap, use_container_width=True, config=PLOTLY_CONFIG)
    
    highest_risk_job = treemap_data.loc[treemap_data['Avg Risk'].idxmax()]
    lowest_risk_job = treemap_data.loc[treemap_data['Avg Risk'].idxmin()]
    
    display_insight(
        f"Highest risk job: '{highest_risk_job['Job Title']}' ({highest_risk_job['Avg Risk']:.1f} risk, {highest_risk_job['Count']:,} workers). Lowest risk: '{lowest_risk_job['Job Title']}' ({lowest_risk_job['Avg Risk']:.1f} risk).",
        "The treemap enables drill-down analysis from broad categories to specific roles. Click on categories to explore job-level automation risks and identify specific reskilling targets."
    )
    
    st.markdown("---")
    
    # ========== 2.6 SUNBURST CHART - Hierarchy ==========
    
    st.subheader("2.6 Industry → Job Category → Job Level Hierarchy")
    
    sunburst_data = filtered_df.groupby(['industry', 'job_category', 'job_level']).agg({
        'automation_risk_score': 'mean',
        'record_id': 'count'
    }).reset_index()
    sunburst_data.columns = ['Industry', 'Job Category', 'Job Level', 'Avg Risk', 'Count']
    
    fig_sunburst = px.sunburst(
        sunburst_data,
        path=['Industry', 'Job Category', 'Job Level'],
        values='Count',
        color='Avg Risk',
        color_continuous_scale='RdYlGn_r',
        hover_data={'Avg Risk': ':.1f'}
    )
    
    fig_sunburst.update_traces(
        hovertemplate='<b>%{label}</b><br>Workers: %{value:,}<br>Avg Risk: %{color:.1f}<extra></extra>'
    )
    
    fig_sunburst.update_layout(
        title=dict(
            text='Hierarchical Workforce Structure<br><sup>Click to drill down: Industry → Job Category → Job Level</sup>',
            font=dict(size=14)
        ),
        height=550,
        margin=dict(l=20, r=20, t=80, b=20)
    )
    
    st.plotly_chart(fig_sunburst, use_container_width=True, config=PLOTLY_CONFIG)
    
    display_insight(
        "The sunburst chart reveals the nested structure of the workforce across industries, job categories, and seniority levels. Inner rings represent broader groupings while outer rings show detailed breakdowns.",
        "This hierarchical view helps identify where automation risk concentrates across organizational structures. Use this to design targeted interventions at the appropriate level—industry-wide, department-specific, or role-based."
    )
    
    st.markdown("---")
    
    # ========== 2.7 SCATTER PLOT - Risk vs AI Augmentation ==========
    
    st.subheader("2.7 Automation Risk vs AI Augmentation Potential")
    
    fig_scatter = px.scatter(
        filtered_df.sample(min(1000, len(filtered_df))),  # Sample for performance
        x='automation_risk_score',
        y='ai_augmentation_potential',
        color='job_category',
        color_discrete_sequence=COLORS['categorical_extended'],
        opacity=0.6,
        hover_data=['job_title', 'industry', 'annual_salary_usd']
    )
    
    fig_scatter.update_traces(
        marker=dict(size=8),
        hovertemplate='<b>%{customdata[0]}</b><br>Industry: %{customdata[1]}<br>Risk: %{x:.1f}<br>Augmentation: %{y:.1f}<br>Salary: $%{customdata[2]:,.0f}<extra></extra>'
    )
    
    # Add trend line
    fig_scatter.add_trace(go.Scatter(
        x=[0, 100],
        y=[100, 0],
        mode='lines',
        line=dict(color='gray', dash='dash', width=1),
        name='Inverse Relationship',
        hoverinfo='skip'
    ))
    
    fig_scatter.update_layout(
        title=dict(
            text='Automation Risk vs AI Augmentation Potential<br><sup>Each point represents a worker | Dashed line shows inverse relationship</sup>',
            font=dict(size=14)
        ),
        xaxis_title='Automation Risk Score (Higher = More Replaceable)',
        yaxis_title='AI Augmentation Potential (Higher = More Enhancement)',
        height=500,
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5),
        margin=dict(l=20, r=20, t=80, b=100)
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True, config=PLOTLY_CONFIG)
    
    correlation = filtered_df['automation_risk_score'].corr(filtered_df['ai_augmentation_potential'])
    
    display_insight(
        f"The correlation between automation risk and AI augmentation potential is {correlation:.2f}, indicating {'a strong inverse' if correlation < -0.5 else 'a moderate inverse' if correlation < -0.3 else 'a weak'} relationship.",
        "Jobs with high automation risk tend to have lower augmentation potential, meaning they're more likely to be replaced rather than enhanced by AI. Focus reskilling efforts on transitioning workers toward high-augmentation roles."
    )

    # ============================================================
# PAGE 3: SKILLS & TRAINING ANALYSIS
# ============================================================

elif page == "💼 Skills & Training":
    
    st.title("💼 Skills & Training Analysis")
    st.markdown("### Workforce Capabilities and Development Needs")
    st.markdown("---")
    
    # ========== 3.1 GROUPED BAR CHART - Skill Scores ==========
    
    st.subheader("3.1 Average Skill Scores by Country")
    
    skill_cols = ['technical_skill_score', 'soft_skill_score', 'digital_literacy_score', 'ai_literacy_score']
    skill_labels = ['Technical Skills', 'Soft Skills', 'Digital Literacy', 'AI Literacy']
    
    skill_by_country = filtered_df.groupby('country')[skill_cols].mean().reset_index()
    
    fig_skills = go.Figure()
    
    for i, (col, label) in enumerate(zip(skill_cols, skill_labels)):
        fig_skills.add_trace(go.Bar(
            name=label,
            x=skill_by_country['country'],
            y=skill_by_country[col],
            text=[f"{v:.1f}" for v in skill_by_country[col]],
            textposition='outside',
            marker_color=COLORS['categorical'][i],
            hovertemplate=f'<b>{label}</b><br>Country: %{{x}}<br>Score: %{{y:.1f}}<extra></extra>'
        ))
    
    fig_skills.update_layout(
        title=dict(text='Skill Score Comparison: India vs UAE', font=dict(size=14)),
        xaxis_title='',
        yaxis_title='Average Score (0-100)',
        barmode='group',
        height=450,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        margin=dict(l=20, r=20, t=80, b=20),
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig_skills, use_container_width=True, config=PLOTLY_CONFIG)
    
    india_ai = skill_by_country[skill_by_country['country'] == 'India']['ai_literacy_score'].values[0] if 'India' in skill_by_country['country'].values else 0
    uae_ai = skill_by_country[skill_by_country['country'] == 'UAE']['ai_literacy_score'].values[0] if 'UAE' in skill_by_country['country'].values else 0
    
    display_insight(
        f"AI Literacy scores: India ({india_ai:.1f}) vs UAE ({uae_ai:.1f}). The gap of {abs(india_ai - uae_ai):.1f} points highlights different levels of AI readiness across the two markets.",
        "AI literacy consistently scores lowest among all skill categories, indicating a critical training gap. Organizations should prioritize AI literacy programs to prepare their workforce for the evolving job market."
    )
    
    st.markdown("---")
    
    # ========== 3.2 HEATMAP - Skill Gap by Industry ==========
    
    st.subheader("3.2 Skill Gap Index by Industry and Job Level")
    
    heatmap_data = filtered_df.pivot_table(
        values='skill_gap_index',
        index='industry',
        columns='job_level',
        aggfunc='mean'
    )
    
    # Reorder columns
    level_order = ['Entry', 'Junior', 'Mid', 'Senior', 'Lead', 'Manager', 'Director', 'Executive']
    heatmap_data = heatmap_data[[col for col in level_order if col in heatmap_data.columns]]
    
    fig_heatmap = px.imshow(
        heatmap_data,
        color_continuous_scale='RdYlGn_r',  # Red = high gap (bad), Green = low gap (good)
        aspect='auto',
        text_auto='.1f'
    )
    
    fig_heatmap.update_traces(
        hovertemplate='Industry: %{y}<br>Job Level: %{x}<br>Skill Gap Index: %{z:.1f}<extra></extra>'
    )
    
    fig_heatmap.update_layout(
        title=dict(
            text='Skill Gap Index Heatmap<br><sup>Higher values (Red) indicate greater skill gaps requiring training</sup>',
            font=dict(size=14)
        ),
        xaxis_title='Job Level',
        yaxis_title='Industry',
        height=500,
        margin=dict(l=20, r=20, t=80, b=20),
        coloraxis_colorbar=dict(title='Skill Gap<br>Index')
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True, config=PLOTLY_CONFIG)
    
    max_gap = heatmap_data.max().max()
    max_gap_loc = heatmap_data.stack().idxmax()
    
    display_insight(
        f"The highest skill gap ({max_gap:.1f}) is observed in {max_gap_loc[0]} at the {max_gap_loc[1]} level. Entry and Junior levels generally show higher gaps across industries.",
        "This heatmap guides targeted training investments. Focus on the red zones where skill gaps are most acute, particularly for entry-level workers in high-risk industries."
    )
    
    st.markdown("---")
    
    # ========== 3.3 AREA CHART - Training Investment Trend ==========
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("3.3 Training Investment Over Time")
        
        training_trend = filtered_df.groupby('observation_year').agg({
            'employer_training_investment_usd': 'mean',
            'annual_training_hours': 'mean'
        }).reset_index()
        
        fig_area = go.Figure()
        
        fig_area.add_trace(go.Scatter(
            x=training_trend['observation_year'],
            y=training_trend['employer_training_investment_usd'],
            fill='tozeroy',
            name='Training Investment (USD)',
            line=dict(color=COLORS['primary'], width=2),
            fillcolor='rgba(100, 143, 255, 0.3)',
            hovertemplate='Year: %{x}<br>Investment: $%{y:,.0f}<extra></extra>'
        ))
        
        fig_area.update_layout(
            title=dict(text='Employer Training Investment Trend', font=dict(size=13)),
            xaxis_title='Year',
            yaxis_title='Avg Investment (USD)',
            height=400,
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=False
        )
        
        st.plotly_chart(fig_area, use_container_width=True, config=PLOTLY_CONFIG)
        
        if len(training_trend) > 1:
            investment_change = ((training_trend['employer_training_investment_usd'].iloc[-1] / 
                                  training_trend['employer_training_investment_usd'].iloc[0]) - 1) * 100
            display_insight(
                f"Training investment has changed by {investment_change:+.1f}% from {int(training_trend['observation_year'].iloc[0])} to {int(training_trend['observation_year'].iloc[-1])}.",
                "Increasing training investment correlates with better AI readiness. Organizations maintaining or growing L&D budgets are better positioned for workforce transformation."
            )
    
    # ========== 3.4 SCATTER - AI Literacy vs Risk ==========
    
    with col2:
        st.subheader("3.4 AI Literacy vs Automation Risk")
        
        fig_ai_risk = px.scatter(
            filtered_df.sample(min(800, len(filtered_df))),
            x='ai_literacy_score',
            y='automation_risk_score',
            color='education_level',
            color_discrete_sequence=COLORS['categorical'],
            opacity=0.6,
            trendline='ols'
        )
        
        fig_ai_risk.update_traces(
            marker=dict(size=7),
            hovertemplate='AI Literacy: %{x:.1f}<br>Risk Score: %{y:.1f}<extra></extra>'
        )
        
        fig_ai_risk.update_layout(
            title=dict(text='Does AI Literacy Reduce Automation Risk?', font=dict(size=13)),
            xaxis_title='AI Literacy Score',
            yaxis_title='Automation Risk Score',
            height=400,
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(orientation='h', yanchor='bottom', y=-0.35, xanchor='center', x=0.5, font=dict(size=9))
        )
        
        st.plotly_chart(fig_ai_risk, use_container_width=True, config=PLOTLY_CONFIG)
        
        corr = filtered_df['ai_literacy_score'].corr(filtered_df['automation_risk_score'])
        
        display_insight(
            f"Correlation between AI literacy and automation risk: {corr:.3f}. {'Higher AI literacy is associated with lower automation risk.' if corr < 0 else 'The relationship is more nuanced than expected.'}",
            "This validates the importance of AI literacy training as a protective factor against job displacement. Investing in AI skills development can reduce workforce vulnerability."
        )
    
    st.markdown("---")
    
    # ========== 3.5 CORRELATION MATRIX ==========
    
    st.subheader("3.5 Skill Variables Correlation Matrix")
    
    corr_cols = ['technical_skill_score', 'soft_skill_score', 'digital_literacy_score', 
                 'ai_literacy_score', 'skill_gap_index', 'automation_risk_score',
                 'annual_training_hours', 'certifications_held']
    
    corr_labels = ['Technical', 'Soft Skills', 'Digital Lit.', 'AI Literacy', 
                   'Skill Gap', 'Auto. Risk', 'Training Hrs', 'Certifications']
    
    corr_matrix = filtered_df[corr_cols].corr()
    corr_matrix.index = corr_labels
    corr_matrix.columns = corr_labels
    
    fig_corr = px.imshow(
        corr_matrix,
        color_continuous_scale='RdBu_r',
        zmin=-1, zmax=1,
        text_auto='.2f',
        aspect='equal'
    )
    
    fig_corr.update_traces(
        hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.3f}<extra></extra>'
    )
    
    fig_corr.update_layout(
        title=dict(
            text='Correlation Matrix: Skills, Training & Risk Variables<br><sup>Blue = Positive Correlation | Red = Negative Correlation</sup>',
            font=dict(size=14)
        ),
        height=500,
        margin=dict(l=20, r=20, t=80, b=20),
        coloraxis_colorbar=dict(title='Correlation')
    )
    
    st.plotly_chart(fig_corr, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Find strongest correlations
    corr_unstacked = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)).unstack()
    strongest_pos = corr_unstacked.idxmax()
    strongest_neg = corr_unstacked.idxmin()
    
    display_insight(
        f"Strongest positive correlation: {strongest_pos[0]} ↔ {strongest_pos[1]} ({corr_unstacked.max():.2f}). Strongest negative correlation: {strongest_neg[0]} ↔ {strongest_neg[1]} ({corr_unstacked.min():.2f}).",
        "The correlation matrix reveals which skills move together and which are inversely related. Use these relationships to design holistic training programs that address multiple skill dimensions."
    )
    
    st.markdown("---")
    
    # ========== 3.6 STACKED BAR - Certifications by Level ==========
    
    st.subheader("3.6 Certifications Distribution by Job Level")
    
    # Bin certifications
    filtered_df['cert_group'] = pd.cut(
        filtered_df['certifications_held'],
        bins=[-1, 0, 2, 5, 100],
        labels=['None', '1-2', '3-5', '6+']
    )
    
    cert_by_level = pd.crosstab(
        filtered_df['job_level'],
        filtered_df['cert_group'],
        normalize='index'
    ) * 100
    
    # Reorder
    level_order = ['Entry', 'Junior', 'Mid', 'Senior', 'Lead', 'Manager', 'Director', 'Executive']
    cert_by_level = cert_by_level.reindex([l for l in level_order if l in cert_by_level.index])
    
    fig_stack = go.Figure()
    
    for i, col in enumerate(cert_by_level.columns):
        fig_stack.add_trace(go.Bar(
            name=f'{col} Certs',
            y=cert_by_level.index,
            x=cert_by_level[col],
            orientation='h',
            marker_color=COLORS['categorical'][i],
            text=[f'{v:.0f}%' for v in cert_by_level[col]],
            textposition='inside',
            hovertemplate=f'<b>{col} Certifications</b><br>Job Level: %{{y}}<br>Percentage: %{{x:.1f}}%<extra></extra>'
        ))
    
    fig_stack.update_layout(
        title=dict(text='Certification Holdings by Job Level (Percentage)', font=dict(size=14)),
        xaxis_title='Percentage of Workers',
        yaxis_title='',
        barmode='stack',
        height=450,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        margin=dict(l=20, r=20, t=80, b=20),
        xaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig_stack, use_container_width=True, config=PLOTLY_CONFIG)
    
    exec_6plus = cert_by_level.loc['Executive', '6+'] if 'Executive' in cert_by_level.index and '6+' in cert_by_level.columns else 0
    entry_none = cert_by_level.loc['Entry', 'None'] if 'Entry' in cert_by_level.index and 'None' in cert_by_level.columns else 0
    
    display_insight(
        f"Executive level shows {exec_6plus:.1f}% with 6+ certifications, while {entry_none:.1f}% of Entry-level workers have no certifications.",
        "Career progression correlates strongly with certification accumulation. Organizations should create certification pathways that support advancement and reduce the skill gap at entry levels."
    )

    # ============================================================
# PAGE 4: ECONOMIC IMPACT ANALYSIS
# ============================================================

elif page == "💰 Economic Impact":
    
    st.title("💰 Economic Impact Analysis")
    st.markdown("### Financial Implications of AI on the Workforce")
    st.markdown("---")
    
    # ========== 4.1 GROUPED BAR - Salary by Country & Level ==========
    
    st.subheader("4.1 Average Salary by Country and Job Level")
    
    salary_by_level = filtered_df.groupby(['country', 'job_level'])['annual_salary_usd'].mean().reset_index()
    
    # Ensure proper ordering
    level_order = ['Entry', 'Junior', 'Mid', 'Senior', 'Lead', 'Manager', 'Director', 'Executive']
    salary_by_level['job_level'] = pd.Categorical(salary_by_level['job_level'], categories=level_order, ordered=True)
    salary_by_level = salary_by_level.sort_values('job_level')
    
    fig_salary = px.bar(
        salary_by_level,
        x='job_level',
        y='annual_salary_usd',
        color='country',
        barmode='group',
        color_discrete_sequence=COLORS['india_uae'],
        text_auto=',.0f'
    )
    
    fig_salary.update_traces(
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Country: %{data.name}<br>Salary: $%{y:,.0f}<extra></extra>'
    )
    
    fig_salary.update_layout(
        title=dict(text='Salary Comparison: India vs UAE Across Job Levels', font=dict(size=14)),
        xaxis_title='Job Level',
        yaxis_title='Average Annual Salary (USD)',
        height=450,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        margin=dict(l=20, r=20, t=80, b=20)
    )
    
    st.plotly_chart(fig_salary, use_container_width=True, config=PLOTLY_CONFIG)
    
    india_exec = salary_by_level[(salary_by_level['country'] == 'India') & (salary_by_level['job_level'] == 'Executive')]['annual_salary_usd'].values
    uae_exec = salary_by_level[(salary_by_level['country'] == 'UAE') & (salary_by_level['job_level'] == 'Executive')]['annual_salary_usd'].values
    
    india_exec_val = india_exec[0] if len(india_exec) > 0 else 0
    uae_exec_val = uae_exec[0] if len(uae_exec) > 0 else 0
    
    display_insight(
        f"Executive salaries: UAE (${uae_exec_val:,.0f}) vs India (${india_exec_val:,.0f}), a {((uae_exec_val/india_exec_val)-1)*100:.0f}% premium. The gap widens at senior levels.",
        "The UAE commands significant salary premiums, especially at senior levels. This reflects cost of living differences and the premium for international talent in Gulf markets."
    )
    
    st.markdown("---")
    
    # ========== 4.2 BOX PLOT - Salary Distribution ==========
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("4.2 Salary Distribution by Country")
        
        fig_sal_box = px.box(
            filtered_df,
            x='country',
            y='annual_salary_usd',
            color='country',
            color_discrete_sequence=COLORS['india_uae'],
            notched=True,
            points='outliers'
        )
        
        fig_sal_box.update_traces(
            hovertemplate='Country: %{x}<br>Salary: $%{y:,.0f}<extra></extra>'
        )
        
        fig_sal_box.update_layout(
            title=dict(text='Salary Distribution with Outliers', font=dict(size=13)),
            xaxis_title='',
            yaxis_title='Annual Salary (USD)',
            height=400,
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig_sal_box, use_container_width=True, config=PLOTLY_CONFIG)
        
        india_median = filtered_df[filtered_df['country'] == 'India']['annual_salary_usd'].median()
        uae_median = filtered_df[filtered_df['country'] == 'UAE']['annual_salary_usd'].median()
        
        display_insight(
            f"Median salaries: India (${india_median:,.0f}) vs UAE (${uae_median:,.0f}). UAE shows {((uae_median/india_median)-1)*100:.0f}% higher median compensation.",
            "The notched box plots show statistically significant differences in medians. Outliers indicate presence of highly compensated specialists in both markets."
        )
    
    # ========== 4.3 BAR CHART - Wage Premium for AI Skills ==========
    
    with col2:
        st.subheader("4.3 Wage Premium for AI Skills")
        
        premium_by_industry = filtered_df.groupby('industry')['wage_premium_for_ai_skills'].mean().sort_values(ascending=True)
        
        fig_premium = go.Figure()
        
        fig_premium.add_trace(go.Bar(
            x=premium_by_industry.values,
            y=premium_by_industry.index,
            orientation='h',
            marker_color=COLORS['primary'],
            text=[f'{v:.1f}%' for v in premium_by_industry.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>AI Skill Premium: %{x:.1f}%<extra></extra>'
        ))
        
        fig_premium.update_layout(
            title=dict(text='Salary Premium for AI Skills by Industry', font=dict(size=13)),
            xaxis_title='Wage Premium (%)',
            yaxis_title='',
            height=400,
            margin=dict(l=20, r=80, t=50, b=20)
        )
        
        st.plotly_chart(fig_premium, use_container_width=True, config=PLOTLY_CONFIG)
        
        highest_premium = premium_by_industry.iloc[-1]
        highest_premium_ind = premium_by_industry.index[-1]
        
        display_insight(
            f"The highest AI skill premium is in {highest_premium_ind} at {highest_premium:.1f}%. Average premium across industries: {premium_by_industry.mean():.1f}%.",
            "AI skills command measurable salary premiums across all industries. Workers investing in AI competencies can expect tangible financial returns on their learning investment."
        )
    
    st.markdown("---")
    
    # ========== 4.4 SLOPE CHART - Current vs 2030 Salary ==========
    
    st.subheader("4.4 Salary Projection: Current vs 2030")
    
    # Aggregate by job category for cleaner visualization
    salary_projection = filtered_df.groupby('job_category').agg({
        'annual_salary_usd': 'mean',
        'projected_salary_2030_usd': 'mean'
    }).reset_index()
    
    fig_slope = go.Figure()
    
    for i, row in salary_projection.iterrows():
        color = COLORS['categorical'][i % len(COLORS['categorical'])]
        
        # Line connecting current to projected
        fig_slope.add_trace(go.Scatter(
            x=['Current', '2030 Projection'],
            y=[row['annual_salary_usd'], row['projected_salary_2030_usd']],
            mode='lines+markers+text',
            name=row['job_category'],
            line=dict(color=color, width=2),
            marker=dict(size=10),
            text=[f"${row['annual_salary_usd']/1000:.0f}K", f"${row['projected_salary_2030_usd']/1000:.0f}K"],
            textposition=['middle left', 'middle right'],
            hovertemplate=f"<b>{row['job_category']}</b><br>%{{x}}: $%{{y:,.0f}}<extra></extra>"
        ))
    
    fig_slope.update_layout(
        title=dict(
            text='Salary Growth Trajectory by Job Category<br><sup>Current Average vs Projected 2030 Salary</sup>',
            font=dict(size=14)
        ),
        xaxis_title='',
        yaxis_title='Annual Salary (USD)',
        height=500,
        legend=dict(orientation='v', yanchor='top', y=0.99, xanchor='left', x=1.02, font=dict(size=9)),
        margin=dict(l=20, r=150, t=80, b=20),
        hovermode='closest'
    )
    
    st.plotly_chart(fig_slope, use_container_width=True, config=PLOTLY_CONFIG)
    
    avg_growth = ((salary_projection['projected_salary_2030_usd'].mean() / 
                   salary_projection['annual_salary_usd'].mean()) - 1) * 100
    
    display_insight(
        f"Average projected salary growth by 2030: {avg_growth:.1f}%. The slope of each line indicates the expected growth rate for each job category.",
        "Steeper positive slopes indicate faster salary growth projections. Workers in categories with flatter or negative slopes should consider career transitions or aggressive upskilling."
    )
    
    st.markdown("---")
    
    # ========== 4.5 QUADRANT SCATTER - Security vs Displacement ==========
    
    st.subheader("4.5 Job Security vs Displacement Risk Analysis")
    
    fig_quadrant = px.scatter(
        filtered_df.sample(min(1000, len(filtered_df))),
        x='job_displacement_probability',
        y='job_security_index',
        color='job_category',
        color_discrete_sequence=COLORS['categorical_extended'],
        opacity=0.6,
        hover_data=['job_title', 'industry']
    )
    
    fig_quadrant.update_traces(
        marker=dict(size=8),
        hovertemplate='<b>%{customdata[0]}</b><br>Industry: %{customdata[1]}<br>Displacement Prob: %{x:.1f}%<br>Security Index: %{y:.1f}<extra></extra>'
    )
    
    # Add quadrant lines at medians
    median_disp = filtered_df['job_displacement_probability'].median()
    median_sec = filtered_df['job_security_index'].median()
    
    fig_quadrant.add_hline(y=median_sec, line_dash="dash", line_color="gray", opacity=0.5)
    fig_quadrant.add_vline(x=median_disp, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Quadrant labels
    fig_quadrant.add_annotation(x=20, y=90, text="✅ SECURE<br>(Low Disp, High Sec)", 
                                showarrow=False, font=dict(size=10, color='green'))
    fig_quadrant.add_annotation(x=80, y=90, text="⚠️ PARADOX<br>(High Disp, High Sec)", 
                                showarrow=False, font=dict(size=10, color='orange'))
    fig_quadrant.add_annotation(x=20, y=20, text="🔄 TRANSITION<br>(Low Disp, Low Sec)", 
                                showarrow=False, font=dict(size=10, color='blue'))
    fig_quadrant.add_annotation(x=80, y=20, text="🚨 AT RISK<br>(High Disp, Low Sec)", 
                                showarrow=False, font=dict(size=10, color='red'))
    
    fig_quadrant.update_layout(
        title=dict(
            text='Job Security Quadrant Analysis<br><sup>Four segments based on displacement probability and security index</sup>',
            font=dict(size=14)
        ),
        xaxis_title='Job Displacement Probability (%)',
        yaxis_title='Job Security Index',
        height=550,
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5, font=dict(size=9)),
        margin=dict(l=20, r=20, t=80, b=120)
    )
    
    st.plotly_chart(fig_quadrant, use_container_width=True, config=PLOTLY_CONFIG)
    
    at_risk = len(filtered_df[(filtered_df['job_displacement_probability'] > median_disp) & 
                               (filtered_df['job_security_index'] < median_sec)])
    secure = len(filtered_df[(filtered_df['job_displacement_probability'] < median_disp) & 
                              (filtered_df['job_security_index'] > median_sec)])
    
    display_insight(
        f"Quadrant distribution: {secure:,} workers ({secure/len(filtered_df)*100:.1f}%) in 'Secure' zone, {at_risk:,} workers ({at_risk/len(filtered_df)*100:.1f}%) in 'At Risk' zone.",
        "The 'At Risk' quadrant (high displacement, low security) requires immediate intervention. The 'Paradox' zone indicates roles that may face displacement despite current perceived security."
    )

    # ============================================================
# PAGE 5: WORKFORCE SENTIMENT ANALYSIS
# ============================================================

elif page == "🧠 Workforce Sentiment":
    
    st.title("🧠 Workforce Sentiment Analysis")
    st.markdown("### Worker Attitudes Toward AI and Career Transformation")
    st.markdown("---")
    
    # ========== 5.1 BAR CHART - AI Anxiety by Age ==========
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("5.1 AI Anxiety Level by Age Group")
        
        anxiety_by_age = filtered_df.groupby('age_group')['ai_anxiety_level'].mean().reset_index()
        
        # Order age groups properly
        age_order = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        anxiety_by_age['age_group'] = pd.Categorical(anxiety_by_age['age_group'], categories=age_order, ordered=True)
        anxiety_by_age = anxiety_by_age.sort_values('age_group')
        
        fig_anxiety = px.bar(
            anxiety_by_age,
            x='age_group',
            y='ai_anxiety_level',
            color='ai_anxiety_level',
            color_continuous_scale='RdYlGn_r',
            text_auto='.2f'
        )
        
        fig_anxiety.update_traces(
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Anxiety Level: %{y:.2f}/5<extra></extra>'
        )
        
        fig_anxiety.update_layout(
            title=dict(text='AI Anxiety by Age (1-5 Scale)', font=dict(size=13)),
            xaxis_title='Age Group',
            yaxis_title='Average Anxiety Level',
            height=400,
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20),
            yaxis=dict(range=[0, 5]),
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig_anxiety, use_container_width=True, config=PLOTLY_CONFIG)
        
        oldest_anxiety = anxiety_by_age[anxiety_by_age['age_group'] == '65+']['ai_anxiety_level'].values
        youngest_anxiety = anxiety_by_age[anxiety_by_age['age_group'] == '18-24']['ai_anxiety_level'].values
        
        oldest_val = oldest_anxiety[0] if len(oldest_anxiety) > 0 else 0
        youngest_val = youngest_anxiety[0] if len(youngest_anxiety) > 0 else 0
        
        display_insight(
            f"AI anxiety increases with age: 18-24 ({youngest_val:.2f}) vs 65+ ({oldest_val:.2f}), a difference of {oldest_val - youngest_val:.2f} points on a 5-point scale.",
            "Older workers experience significantly higher AI anxiety. Age-sensitive change management and targeted support programs can help address these concerns."
        )
    
    # ========== 5.2 DONUT CHART - AI Benefit Perception ==========
    
    with col2:
        st.subheader("5.2 AI Benefit Perception")
        
        benefit_counts = filtered_df['ai_benefit_perception'].value_counts()
        
        # Define order and colors
        perception_order = ['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive']
        perception_colors = ['#d73027', '#f46d43', '#fee08b', '#a6d96a', '#1a9850']
        
        # Reorder
        benefit_counts = benefit_counts.reindex([p for p in perception_order if p in benefit_counts.index])
        colors_ordered = [perception_colors[perception_order.index(p)] for p in benefit_counts.index]
        
        fig_benefit = px.pie(
            values=benefit_counts.values,
            names=benefit_counts.index,
            color_discrete_sequence=colors_ordered,
            hole=0.5
        )
        
        fig_benefit.update_traces(
            textposition='outside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>'
        )
        
        positive_pct = (benefit_counts.get('Positive', 0) + benefit_counts.get('Very Positive', 0)) / len(filtered_df) * 100
        
        fig_benefit.update_layout(
            title=dict(text='How Workers Perceive AI Benefits', font=dict(size=13)),
            height=400,
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20),
            annotations=[dict(text=f'{positive_pct:.0f}%<br>Positive', x=0.5, y=0.5, font_size=14, showarrow=False)]
        )
        
        st.plotly_chart(fig_benefit, use_container_width=True, config=PLOTLY_CONFIG)
        
        negative_pct = (benefit_counts.get('Negative', 0) + benefit_counts.get('Very Negative', 0)) / len(filtered_df) * 100
        
        display_insight(
            f"{positive_pct:.1f}% of workers view AI positively (Positive + Very Positive), while {negative_pct:.1f}% hold negative views.",
            "The overall positive sentiment suggests workforce receptiveness to AI adoption. Address concerns of the negative segment through transparent communication and demonstrated benefits."
        )
    
    st.markdown("---")
    
    # ========== 5.3 STACKED BAR - Reskilling Willingness ==========
    
    st.subheader("5.3 Reskilling Willingness by Age Group")
    
    # Bin reskilling willingness
    filtered_df['reskill_group'] = filtered_df['reskilling_willingness'].map({
        1: 'Very Low', 2: 'Low', 3: 'Moderate', 4: 'High', 5: 'Very High'
    })
    
    reskill_cross = pd.crosstab(
        filtered_df['age_group'],
        filtered_df['reskill_group'],
        normalize='index'
    ) * 100
    
    # Reorder columns and index
    reskill_order = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
    reskill_cross = reskill_cross[[c for c in reskill_order if c in reskill_cross.columns]]
    age_order = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    reskill_cross = reskill_cross.reindex([a for a in age_order if a in reskill_cross.index])
    
    fig_reskill = go.Figure()
    
    reskill_colors = ['#d73027', '#f46d43', '#fee08b', '#a6d96a', '#1a9850']
    
    for i, col in enumerate(reskill_cross.columns):
        fig_reskill.add_trace(go.Bar(
            name=col,
            x=reskill_cross.index,
            y=reskill_cross[col],
            marker_color=reskill_colors[i],
            text=[f'{v:.0f}%' if v > 5 else '' for v in reskill_cross[col]],
            textposition='inside',
            hovertemplate=f'<b>{col}</b><br>Age: %{{x}}<br>Percentage: %{{y:.1f}}%<extra></extra>'
        ))
    
    fig_reskill.update_layout(
        title=dict(text='Willingness to Reskill Across Age Groups', font=dict(size=14)),
        xaxis_title='Age Group',
        yaxis_title='Percentage of Workers',
        barmode='stack',
        height=450,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        margin=dict(l=20, r=20, t=80, b=20),
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig_reskill, use_container_width=True, config=PLOTLY_CONFIG)
    
    young_high = reskill_cross.loc['18-24', ['High', 'Very High']].sum() if '18-24' in reskill_cross.index else 0
    old_high = reskill_cross.loc['65+', ['High', 'Very High']].sum() if '65+' in reskill_cross.index else 0
    
    display_insight(
        f"High/Very High reskilling willingness: 18-24 age group ({young_high:.1f}%) vs 65+ ({old_high:.1f}%). Younger workers show {young_high - old_high:.1f}% higher enthusiasm.",
        "Despite lower anxiety, younger workers also show higher reskilling willingness. Design learning programs that leverage this enthusiasm while making programs accessible for older workers."
    )
    
    st.markdown("---")
    
    # ========== 5.4 HEATMAP - Satisfaction by Industry & Level ==========
    
    st.subheader("5.4 Job Satisfaction Heatmap")
    
    satisfaction_heat = filtered_df.pivot_table(
        values='job_satisfaction_score',
        index='industry',
        columns='job_level',
        aggfunc='mean'
    )
    
    # Reorder columns
    level_order = ['Entry', 'Junior', 'Mid', 'Senior', 'Lead', 'Manager', 'Director', 'Executive']
    satisfaction_heat = satisfaction_heat[[col for col in level_order if col in satisfaction_heat.columns]]
    
    fig_sat_heat = px.imshow(
        satisfaction_heat,
        color_continuous_scale='RdYlGn',
        aspect='auto',
        text_auto='.0f'
    )
    
    fig_sat_heat.update_traces(
        hovertemplate='Industry: %{y}<br>Level: %{x}<br>Satisfaction: %{z:.1f}<extra></extra>'
    )
    
    fig_sat_heat.update_layout(
        title=dict(
            text='Job Satisfaction Score by Industry & Job Level<br><sup>Green = High Satisfaction | Red = Low Satisfaction</sup>',
            font=dict(size=14)
        ),
        xaxis_title='Job Level',
        yaxis_title='Industry',
        height=500,
        margin=dict(l=20, r=20, t=80, b=20),
        coloraxis_colorbar=dict(title='Satisfaction<br>Score')
    )
    
    st.plotly_chart(fig_sat_heat, use_container_width=True, config=PLOTLY_CONFIG)
    
    max_sat = satisfaction_heat.max().max()
    max_sat_loc = satisfaction_heat.stack().idxmax()
    min_sat = satisfaction_heat.min().min()
    min_sat_loc = satisfaction_heat.stack().idxmin()
    
    display_insight(
        f"Highest satisfaction: {max_sat_loc[0]} - {max_sat_loc[1]} ({max_sat:.1f}). Lowest: {min_sat_loc[0]} - {min_sat_loc[1]} ({min_sat:.1f}). Range of {max_sat - min_sat:.1f} points.",
        "Satisfaction patterns reveal industry-level cultural differences. Organizations with low satisfaction scores should investigate root causes—often related to AI anxiety, workload, or career uncertainty."
    )
    
    st.markdown("---")
    
    # ========== 5.5 PARALLEL COORDINATES - Sentiment Dimensions ==========
    
    st.subheader("5.5 Multi-Dimensional Sentiment Analysis")
    
    # Sample for performance and select relevant columns
    sentiment_cols = ['ai_anxiety_level', 'ai_optimism_level', 'reskilling_willingness', 
                      'technology_acceptance_score', 'job_satisfaction_score', 'work_life_balance_score']
    
    # Normalize to 0-100 for parallel coordinates
    parallel_data = filtered_df[sentiment_cols + ['country']].copy()
    parallel_data['ai_anxiety_level'] = parallel_data['ai_anxiety_level'] * 20  # 1-5 to 0-100
    parallel_data['ai_optimism_level'] = parallel_data['ai_optimism_level'] * 20
    parallel_data['reskilling_willingness'] = parallel_data['reskilling_willingness'] * 20
    
    # Sample for visualization
    parallel_sample = parallel_data.sample(min(500, len(parallel_data)))
    
    fig_parallel = px.parallel_coordinates(
        parallel_sample,
        dimensions=['ai_anxiety_level', 'ai_optimism_level', 'reskilling_willingness',
                   'technology_acceptance_score', 'job_satisfaction_score', 'work_life_balance_score'],
        color='ai_anxiety_level',
        color_continuous_scale='RdYlGn_r',
        labels={
            'ai_anxiety_level': 'AI Anxiety',
            'ai_optimism_level': 'AI Optimism',
            'reskilling_willingness': 'Reskill Willing',
            'technology_acceptance_score': 'Tech Accept',
            'job_satisfaction_score': 'Job Satisf',
            'work_life_balance_score': 'Work-Life Bal'
        }
    )
    
    fig_parallel.update_layout(
        title=dict(
            text='Parallel Coordinates: Worker Sentiment Profile<br><sup>Each line represents a worker | Color = AI Anxiety Level</sup>',
            font=dict(size=14)
        ),
        height=500,
        margin=dict(l=100, r=100, t=80, b=20),
        coloraxis_colorbar=dict(title='AI Anxiety')
    )
    
    st.plotly_chart(fig_parallel, use_container_width=True, config=PLOTLY_CONFIG)
    
    display_insight(
        "Parallel coordinates reveal sentiment patterns across six dimensions simultaneously. Lines crossing in similar patterns indicate worker segments with common characteristics.",
        "Use this visualization to identify worker personas: high-anxiety/low-optimism workers need different support than low-anxiety/high-reskilling workers. Tailor change management approaches accordingly."
    )

    # ============================================================
# PAGE 6: GEOGRAPHIC ANALYSIS
# ============================================================

elif page == "🌍 Geographic Analysis":
    
    st.title("🌍 Geographic Analysis")
    st.markdown("### Regional Workforce Patterns Across India & UAE")
    st.markdown("---")
    
    # ========== 6.1 CHOROPLETH MAP - India ==========
    
    st.subheader("6.1 India: State-wise Analysis")
    
    # Metric selector
    map_metric = st.selectbox(
        "Select Metric to Display:",
        ['ai_literacy_score', 'automation_risk_score', 'annual_salary_usd', 
         'skill_gap_index', 'job_satisfaction_score'],
        format_func=lambda x: x.replace('_', ' ').title()
    )
    
    india_data = filtered_df[filtered_df['country'] == 'India'].groupby('state_emirate').agg({
        map_metric: 'mean',
        'record_id': 'count'
    }).reset_index()
    india_data.columns = ['State', 'Metric Value', 'Worker Count']
    
    # Add coordinates
    india_data['lat'] = india_data['State'].map(lambda x: INDIA_STATE_COORDS.get(x, [20, 78])[0])
    india_data['lon'] = india_data['State'].map(lambda x: INDIA_STATE_COORDS.get(x, [20, 78])[1])
    
    # Determine color scale based on metric
    if 'risk' in map_metric or 'gap' in map_metric:
        color_scale = 'RdYlGn_r'  # Red = bad
    else:
        color_scale = 'RdYlGn'  # Green = good
    
    fig_india_map = px.scatter_mapbox(
        india_data,
        lat='lat',
        lon='lon',
        size='Worker Count',
        color='Metric Value',
        color_continuous_scale=color_scale,
        size_max=40,
        zoom=3.5,
        center={'lat': 22, 'lon': 82},
        mapbox_style='carto-positron',
        hover_name='State',
        hover_data={'lat': False, 'lon': False, 'Metric Value': ':.1f', 'Worker Count': ':,'}
    )
    
    fig_india_map.update_layout(
        title=dict(
            text=f'India: {map_metric.replace("_", " ").title()} by State<br><sup>Bubble size = Worker count | Color = Metric value</sup>',
            font=dict(size=14)
        ),
        height=500,
        margin=dict(l=0, r=0, t=80, b=0),
        coloraxis_colorbar=dict(title=map_metric.replace('_', ' ').title()[:15])
    )
    
    st.plotly_chart(fig_india_map, use_container_width=True, config=PLOTLY_CONFIG)
    
    top_state = india_data.loc[india_data['Metric Value'].idxmax()]
    bottom_state = india_data.loc[india_data['Metric Value'].idxmin()]
    
    display_insight(
        f"Highest {map_metric.replace('_', ' ')}: {top_state['State']} ({top_state['Metric Value']:.1f}). Lowest: {bottom_state['State']} ({bottom_state['Metric Value']:.1f}). Range: {top_state['Metric Value'] - bottom_state['Metric Value']:.1f} points.",
        "Geographic variation highlights regional disparities in AI readiness and workforce characteristics. Policy interventions should be tailored to state-specific needs."
    )
    
    st.markdown("---")
    
    # ========== 6.2 BAR CHART - UAE Emirates ==========
    
    st.subheader("6.2 UAE: Emirates Comparison")
    
    uae_data = filtered_df[filtered_df['country'] == 'UAE'].groupby('state_emirate').agg({
        'annual_salary_usd': 'mean',
        'automation_risk_score': 'mean',
        'ai_literacy_score': 'mean',
        'record_id': 'count'
    }).reset_index()
    uae_data.columns = ['Emirate', 'Avg Salary', 'Risk Score', 'AI Literacy', 'Worker Count']
    uae_data = uae_data.sort_values('Avg Salary', ascending=True)
    
    fig_uae = make_subplots(rows=1, cols=3, subplot_titles=['Avg Salary (USD)', 'Automation Risk', 'AI Literacy'])
    
    # Salary
    fig_uae.add_trace(go.Bar(
        y=uae_data['Emirate'],
        x=uae_data['Avg Salary'],
        orientation='h',
        marker_color=COLORS['primary'],
        text=[f'${v/1000:.0f}K' for v in uae_data['Avg Salary']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Salary: $%{x:,.0f}<extra></extra>',
        showlegend=False
    ), row=1, col=1)
    
    # Risk
    fig_uae.add_trace(go.Bar(
        y=uae_data['Emirate'],
        x=uae_data['Risk Score'],
        orientation='h',
        marker_color=COLORS['secondary'],
        text=[f'{v:.1f}' for v in uae_data['Risk Score']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Risk: %{x:.1f}<extra></extra>',
        showlegend=False
    ), row=1, col=2)
    
    # AI Literacy
    fig_uae.add_trace(go.Bar(
        y=uae_data['Emirate'],
        x=uae_data['AI Literacy'],
        orientation='h',
        marker_color=COLORS['categorical'][4],
        text=[f'{v:.1f}' for v in uae_data['AI Literacy']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>AI Literacy: %{x:.1f}<extra></extra>',
        showlegend=False
    ), row=1, col=3)
    
    fig_uae.update_layout(
        title=dict(text='UAE Emirates: Key Workforce Metrics', font=dict(size=14)),
        height=400,
        margin=dict(l=20, r=80, t=80, b=20)
    )
    
    st.plotly_chart(fig_uae, use_container_width=True, config=PLOTLY_CONFIG)
    
    top_emirate = uae_data.loc[uae_data['Avg Salary'].idxmax()]
    
    display_insight(
        f"{top_emirate['Emirate']} leads in average salary (${top_emirate['Avg Salary']:,.0f}) with {top_emirate['Worker Count']:,} workers. Abu Dhabi and Dubai dominate the UAE workforce.",
        "The UAE's concentration in Dubai and Abu Dhabi creates a two-tier economy. Other emirates may offer cost advantages but have smaller talent pools."
    )
    
    st.markdown("---")
    
    # ========== 6.3 GROUPED BAR - City Tier Analysis ==========
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("6.3 Analysis by City Tier")
        
        tier_data = filtered_df.groupby('city_tier').agg({
            'annual_salary_usd': 'mean',
            'automation_risk_score': 'mean',
            'ai_literacy_score': 'mean',
            'skill_gap_index': 'mean'
        }).reset_index()
        
        fig_tier = go.Figure()
        
        metrics = ['annual_salary_usd', 'automation_risk_score', 'ai_literacy_score', 'skill_gap_index']
        labels = ['Salary (÷1000)', 'Risk Score', 'AI Literacy', 'Skill Gap']
        
        # Normalize salary for comparison
        tier_data['salary_norm'] = tier_data['annual_salary_usd'] / 1000
        
        for i, (metric, label) in enumerate(zip(['salary_norm', 'automation_risk_score', 'ai_literacy_score', 'skill_gap_index'], labels)):
            fig_tier.add_trace(go.Bar(
                name=label,
                x=tier_data['city_tier'],
                y=tier_data[metric],
                marker_color=COLORS['categorical'][i],
                hovertemplate=f'<b>{label}</b><br>City Tier: %{{x}}<br>Value: %{{y:.1f}}<extra></extra>'
            ))
        
        fig_tier.update_layout(
            title=dict(text='Workforce Metrics by City Tier', font=dict(size=13)),
            xaxis_title='City Tier',
            yaxis_title='Score / Value',
            barmode='group',
            height=400,
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5, font=dict(size=9)),
            margin=dict(l=20, r=20, t=80, b=20)
        )
        
        st.plotly_chart(fig_tier, use_container_width=True, config=PLOTLY_CONFIG)
        
        display_insight(
            "Metro and Tier 1 cities show higher salaries and AI literacy but also attract workers with higher automation risk profiles due to industry concentration.",
            "Tier 2 and Tier 3 cities may represent emerging opportunities with lower costs and growing tech presence. Consider geographic diversification in talent strategies."
        )
    
    # ========== 6.4 RADAR CHART - Economic Zone ==========
    
    with col2:
        st.subheader("6.4 Economic Zone Profiles")
        
        zone_data = filtered_df.groupby('economic_zone').agg({
            'ai_literacy_score': 'mean',
            'automation_risk_score': 'mean',
            'annual_salary_usd': 'mean',
            'skill_gap_index': 'mean',
            'job_satisfaction_score': 'mean'
        }).reset_index()
        
        # Normalize all to 0-100
        zone_data['salary_norm'] = (zone_data['annual_salary_usd'] / zone_data['annual_salary_usd'].max()) * 100
        
        categories = ['AI Literacy', 'Risk Score', 'Salary', 'Skill Gap', 'Satisfaction']
        
        fig_radar = go.Figure()
        
        for i, row in zone_data.iterrows():
            values = [
                row['ai_literacy_score'],
                row['automation_risk_score'],
                row['salary_norm'],
                row['skill_gap_index'],
                row['job_satisfaction_score']
            ]
            values.append(values[0])  # Close the polygon
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=row['economic_zone'],
                line=dict(color=COLORS['categorical'][i % len(COLORS['categorical'])]),
                opacity=0.6,
                hovertemplate='%{theta}: %{r:.1f}<extra></extra>'
            ))
        
        fig_radar.update_layout(
            title=dict(text='Economic Zone Comparison', font=dict(size=13)),
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            height=400,
            legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5, font=dict(size=9)),
            margin=dict(l=60, r=60, t=60, b=80)
        )
        
        st.plotly_chart(fig_radar, use_container_width=True, config=PLOTLY_CONFIG)
        
        display_insight(
            "Each economic zone shows a distinct profile. Tech Hubs excel in AI literacy but show higher salary costs. Industrial zones face higher automation risk.",
            "The radar chart enables quick comparison of zone characteristics. Choose locations based on the specific metric priorities for your workforce strategy."
        )
    
    st.markdown("---")
    
    # ========== 6.5 CALENDAR HEATMAP - Data by Year ==========
    
    st.subheader("6.5 Data Distribution by Year and Country")
    
    yearly_country = pd.crosstab(filtered_df['observation_year'], filtered_df['country'])
    
    fig_calendar = px.imshow(
        yearly_country.T,
        color_continuous_scale='Blues',
        aspect='auto',
        text_auto=True
    )
    
    fig_calendar.update_traces(
        hovertemplate='Year: %{x}<br>Country: %{y}<br>Records: %{z:,}<extra></extra>'
    )
    
    fig_calendar.update_layout(
        title=dict(
            text='Data Records by Observation Year and Country<br><sup>Darker = More records</sup>',
            font=dict(size=14)
        ),
        xaxis_title='Observation Year',
        yaxis_title='Country',
        height=250,
        margin=dict(l=20, r=20, t=80, b=20),
        coloraxis_colorbar=dict(title='Records')
    )
    
    st.plotly_chart(fig_calendar, use_container_width=True, config=PLOTLY_CONFIG)
    
    peak_year = yearly_country.sum(axis=1).idxmax()
    peak_count = yearly_country.sum(axis=1).max()
    
    display_insight(
        f"Data collection peaked in {peak_year} with {peak_count:,} records. The distribution shows consistent data availability across the observation period.",
        "Temporal coverage ensures trend analysis validity. More recent years may show emerging patterns not visible in historical data."
    )

    # ============================================================
# PAGE 7: AI/ML ANALYTICS
# ============================================================

elif page == "🤖 AI/ML Analytics":
    
    st.title("🤖 AI/ML Analytics")
    st.markdown("### Advanced Analytics: Machine Learning Perspectives on Workforce Data")
    st.markdown("---")
    
    # ========== 7.1 CONFUSION MATRIX - Job Transformation ==========
    
    st.subheader("7.1 Job Transformation Matrix")
    st.markdown("*Showing how jobs distribute across transformation stages and demand forecasts*")
    
    # Create a cross-tabulation as a "confusion matrix" style visualization
    transform_matrix = pd.crosstab(
        filtered_df['job_transformation_stage'],
        filtered_df['demand_forecast_2030'],
        normalize='all'
    ) * 100
    
    # Reorder
    stage_order = ['Pre-AI', 'Early Adoption', 'Scaling', 'Optimized', 'AI-Native']
    demand_order = ['Declining', 'Stable', 'Growing', 'High Growth']
    
    transform_matrix = transform_matrix.reindex([s for s in stage_order if s in transform_matrix.index])
    transform_matrix = transform_matrix[[d for d in demand_order if d in transform_matrix.columns]]
    
    fig_conf = px.imshow(
        transform_matrix,
        color_continuous_scale='RdYlGn',
        text_auto='.1f',
        aspect='auto'
    )
    
    fig_conf.update_traces(
        hovertemplate='Stage: %{y}<br>Demand 2030: %{x}<br>Percentage: %{z:.1f}%<extra></extra>'
    )
    
    fig_conf.update_layout(
        title=dict(
            text='Job Transformation Stage vs 2030 Demand Forecast<br><sup>Values show percentage of total workforce in each cell</sup>',
            font=dict(size=14)
        ),
        xaxis_title='Demand Forecast 2030',
        yaxis_title='Current Transformation Stage',
        height=400,
        margin=dict(l=20, r=20, t=80, b=20),
        coloraxis_colorbar=dict(title='% of<br>Workforce')
    )
    
    st.plotly_chart(fig_conf, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Calculate key insights
    ai_native_growth = transform_matrix.loc['AI-Native', ['Growing', 'High Growth']].sum() if 'AI-Native' in transform_matrix.index else 0
    pre_ai_decline = transform_matrix.loc['Pre-AI', 'Declining'] if 'Pre-AI' in transform_matrix.index and 'Declining' in transform_matrix.columns else 0
    
    display_insight(
        f"AI-Native jobs show {ai_native_growth:.1f}% in growth categories, while Pre-AI stage shows {pre_ai_decline:.1f}% in declining demand. The diagonal pattern indicates transformation stage correlates with demand outlook.",
        "This matrix helps identify workforce segments requiring transition support. Workers in Pre-AI/Declining cells face urgent transformation needs, while AI-Native/Growth cells represent target destinations."
    )
    
    st.markdown("---")
    
    # ========== 7.2 ROC-STYLE CURVE - Risk-Benefit Tradeoff ==========
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("7.2 Risk-Benefit Tradeoff Curve")
        
        # Create threshold-based analysis
        thresholds = np.arange(0, 101, 5)
        tradeoff_data = []
        
        for thresh in thresholds:
            high_risk_pct = (filtered_df['automation_risk_score'] >= thresh).mean() * 100
            high_augment_pct = (filtered_df[filtered_df['automation_risk_score'] >= thresh]['ai_augmentation_potential'].mean()) if high_risk_pct > 0 else 0
            tradeoff_data.append({
                'threshold': thresh,
                'pct_above_threshold': high_risk_pct,
                'avg_augmentation': high_augment_pct
            })
        
        tradeoff_df = pd.DataFrame(tradeoff_data)
        
        fig_roc = go.Figure()
        
        fig_roc.add_trace(go.Scatter(
            x=tradeoff_df['pct_above_threshold'],
            y=tradeoff_df['avg_augmentation'],
            mode='lines+markers',
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(size=8),
            text=tradeoff_df['threshold'],
            hovertemplate='Risk Threshold: %{text}<br>% Above Threshold: %{x:.1f}%<br>Avg Augmentation: %{y:.1f}<extra></extra>'
        ))
        
        # Add diagonal reference line
        fig_roc.add_trace(go.Scatter(
            x=[0, 100],
            y=[100, 0],
            mode='lines',
            line=dict(color='gray', dash='dash'),
            name='Random',
            hoverinfo='skip'
        ))
        
        fig_roc.update_layout(
            title=dict(text='Automation Risk vs AI Augmentation Tradeoff', font=dict(size=13)),
            xaxis_title='% Workforce Above Risk Threshold',
            yaxis_title='Avg AI Augmentation Potential',
            height=400,
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig_roc, use_container_width=True, config=PLOTLY_CONFIG)
        
        display_insight(
            "This curve shows the tradeoff between automation risk threshold and augmentation potential. As risk threshold increases, fewer workers qualify but their augmentation potential changes.",
            "Use this to set optimal intervention thresholds. The curve helps balance between capturing enough at-risk workers while maintaining meaningful augmentation potential for reskilling."
        )
    
    # ========== 7.3 LEARNING CURVES - Training Impact ==========
    
    with col2:
        st.subheader("7.3 Training Impact Analysis")
        
        # Bin training hours
        filtered_df['training_bin'] = pd.cut(
            filtered_df['annual_training_hours'],
            bins=[0, 20, 40, 60, 80, 100, 500],
            labels=['0-20', '21-40', '41-60', '61-80', '81-100', '100+']
        )
        
        training_impact = filtered_df.groupby('training_bin').agg({
            'ai_literacy_score': 'mean',
            'skill_gap_index': 'mean',
            'automation_risk_score': 'mean'
        }).reset_index()
        
        fig_learning = go.Figure()
        
        fig_learning.add_trace(go.Scatter(
            x=training_impact['training_bin'].astype(str),
            y=training_impact['ai_literacy_score'],
            name='AI Literacy',
            mode='lines+markers',
            line=dict(color=COLORS['categorical'][0], width=3),
            marker=dict(size=10),
            hovertemplate='Training: %{x} hrs<br>AI Literacy: %{y:.1f}<extra></extra>'
        ))
        
        fig_learning.add_trace(go.Scatter(
            x=training_impact['training_bin'].astype(str),
            y=training_impact['skill_gap_index'],
            name='Skill Gap',
            mode='lines+markers',
            line=dict(color=COLORS['categorical'][2], width=3),
            marker=dict(size=10),
            hovertemplate='Training: %{x} hrs<br>Skill Gap: %{y:.1f}<extra></extra>'
        ))
        
        fig_learning.update_layout(
            title=dict(text='Skill Metrics vs Training Hours', font=dict(size=13)),
            xaxis_title='Annual Training Hours',
            yaxis_title='Score',
            height=400,
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            margin=dict(l=20, r=20, t=80, b=20)
        )
        
        st.plotly_chart(fig_learning, use_container_width=True, config=PLOTLY_CONFIG)
        
        display_insight(
            "AI literacy increases with training hours while skill gap decreases, demonstrating clear returns on training investment.",
            "This 'learning curve' validates training ROI. The inflection points help determine optimal training durations for maximum impact."
        )
    
    st.markdown("---")
    
    # ========== 7.4 FEATURE IMPORTANCE - Risk Drivers ==========
    
    st.subheader("7.4 Factors Influencing Automation Risk")
    st.markdown("*Correlation-based importance analysis of variables affecting automation risk*")
    
    # Calculate correlations with automation risk
    numeric_cols = ['ai_literacy_score', 'technical_skill_score', 'digital_literacy_score',
                    'soft_skill_score', 'years_of_experience', 'annual_training_hours',
                    'company_ai_adoption_level', 'skill_gap_index', 'certifications_held',
                    'annual_salary_usd', 'remote_work_percentage']
    
    correlations = []
    for col in numeric_cols:
        corr = filtered_df['automation_risk_score'].corr(filtered_df[col])
        correlations.append({'Feature': col.replace('_', ' ').title(), 'Correlation': corr})
    
    corr_df = pd.DataFrame(correlations)
    corr_df['Abs_Correlation'] = abs(corr_df['Correlation'])
    corr_df = corr_df.sort_values('Abs_Correlation', ascending=True)
    
    # Create colors based on positive/negative
    colors = [COLORS['pos_neg'][0] if c > 0 else COLORS['pos_neg'][1] for c in corr_df['Correlation']]
    
    fig_importance = go.Figure()
    
    fig_importance.add_trace(go.Bar(
        x=corr_df['Correlation'],
        y=corr_df['Feature'],
        orientation='h',
        marker_color=colors,
        text=[f'{c:.3f}' for c in corr_df['Correlation']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Correlation with Risk: %{x:.3f}<extra></extra>'
    ))
    
    fig_importance.add_vline(x=0, line_color='black', line_width=1)
    
    fig_importance.update_layout(
        title=dict(
            text='Feature Correlation with Automation Risk<br><sup>Green = Positive (increases risk) | Red = Negative (decreases risk)</sup>',
            font=dict(size=14)
        ),
        xaxis_title='Correlation Coefficient',
        yaxis_title='',
        height=500,
        margin=dict(l=20, r=80, t=80, b=20),
        xaxis=dict(range=[-0.6, 0.6])
    )
    
    st.plotly_chart(fig_importance, use_container_width=True, config=PLOTLY_CONFIG)
    
    strongest = corr_df.loc[corr_df['Abs_Correlation'].idxmax()]
    
    display_insight(
        f"Strongest predictor of automation risk: '{strongest['Feature']}' (correlation: {strongest['Correlation']:.3f}). Skill gap shows strong positive correlation while AI literacy shows protective effect.",
        "This feature importance chart guides intervention priorities. Focus on variables with strong negative correlations (red bars) to reduce automation risk most effectively."
    )
    
    st.markdown("---")
    
    # ========== 7.5 DIMENSIONALITY REDUCTION - PCA/Clustering ==========
    
    st.subheader("7.5 Workforce Segmentation (PCA Visualization)")
    
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    
    # Select features for PCA
    pca_features = ['automation_risk_score', 'ai_literacy_score', 'skill_gap_index',
                    'annual_salary_usd', 'years_of_experience', 'technical_skill_score',
                    'ai_augmentation_potential', 'job_satisfaction_score']
    
    # Prepare data
    pca_data = filtered_df[pca_features].dropna()
    
    # Standardize
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(pca_data)
    
    # Apply PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_data)
    
    # Create DataFrame with results
    pca_df = pd.DataFrame({
        'PC1': pca_result[:, 0],
        'PC2': pca_result[:, 1],
        'Job Category': filtered_df.loc[pca_data.index, 'job_category'],
        'Risk Score': filtered_df.loc[pca_data.index, 'automation_risk_score'],
        'Country': filtered_df.loc[pca_data.index, 'country']
    })
    
    # Sample for visualization
    pca_sample = pca_df.sample(min(1000, len(pca_df)))
    
    fig_pca = px.scatter(
        pca_sample,
        x='PC1',
        y='PC2',
        color='Job Category',
        color_discrete_sequence=COLORS['categorical_extended'],
        opacity=0.7,
        hover_data=['Risk Score', 'Country']
    )
    
    fig_pca.update_traces(
        marker=dict(size=7),
        hovertemplate='<b>%{customdata[0]}</b><br>PC1: %{x:.2f}<br>PC2: %{y:.2f}<br>Risk: %{customdata[1]:.1f}<extra></extra>'
    )
    
    fig_pca.update_layout(
        title=dict(
            text=f'PCA: Workforce Clusters by Job Category<br><sup>Variance Explained: PC1={pca.explained_variance_ratio_[0]*100:.1f}%, PC2={pca.explained_variance_ratio_[1]*100:.1f}%</sup>',
            font=dict(size=14)
        ),
        xaxis_title=f'Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)',
        yaxis_title=f'Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)',
        height=550,
        legend=dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5, font=dict(size=9)),
        margin=dict(l=20, r=20, t=80, b=100)
    )
    
    st.plotly_chart(fig_pca, use_container_width=True, config=PLOTLY_CONFIG)
    
    total_variance = (pca.explained_variance_ratio_[0] + pca.explained_variance_ratio_[1]) * 100
    
    display_insight(
        f"PCA reduces {len(pca_features)} workforce variables to 2 dimensions, capturing {total_variance:.1f}% of variance. Clusters represent natural groupings of similar worker profiles.",
        "This dimensionality reduction reveals hidden structure in the data. Job categories form distinct clusters, validating that workforce segments have genuinely different characteristics beyond their labels."
    )
    
    st.markdown("---")
    
    # Summary Statistics
    st.subheader("📋 Page Summary: Advanced Analytics Takeaways")
    
    st.markdown("""
    | Analysis Type | Key Finding | Business Application |
    |---------------|-------------|---------------------|
    | **Transformation Matrix** | AI-Native jobs correlate with growth outlook | Target transformation toward AI-Native roles |
    | **Risk-Benefit Curve** | Optimal risk threshold exists for intervention | Use data-driven thresholds for reskilling programs |
    | **Learning Curves** | Training hours directly improve AI literacy | Justify L&D investment with quantified returns |
    | **Feature Importance** | Skill gap is strongest risk predictor | Prioritize skill gap reduction in interventions |
    | **PCA Clustering** | Job categories form distinct clusters | Design category-specific transformation pathways |
    """)

# ============================================================
# FOOTER
# ============================================================

st.sidebar.markdown("---")
st.sidebar.markdown("""
**📊 Dashboard Info**
- 7 Pages | 39 Visualizations
- Data: India & UAE Workforce
- Framework: Streamlit + Plotly

*Built for AI in Business Course*
""")

