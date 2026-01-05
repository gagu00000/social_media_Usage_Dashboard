# 🤖 AI in the Future of Work - Interactive Dashboard

[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.18.0-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> A comprehensive data visualization dashboard analyzing the impact of Artificial Intelligence on the workforce in India and UAE. Built as part of the **Masters of AI in Business** program for the **Data Visualization and Analytics** course.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Dashboard Pages](#-dashboard-pages)
- [Chart Types Implemented](#-chart-types-implemented)
- [Dataset Information](#-dataset-information)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Technologies Used](#-technologies-used)
- [Design Principles](#-design-principles)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

This interactive dashboard provides a multi-dimensional analysis of how Artificial Intelligence is reshaping the workforce across India and the UAE. The project visualizes synthetic data representing 5,000 worker profiles across 12 industries, examining automation risks, skill gaps, economic impacts, and workforce sentiment.

### Key Questions Addressed

- 📊 Which industries and job roles face the highest automation risk?
- 💼 What skills are most critical for workforce resilience?
- 💰 How does AI adoption impact salaries and career growth?
- 🧠 What are workers' attitudes toward AI and reskilling?
- 🌍 How do regional factors influence AI readiness?
- 🔮 What does the future workforce landscape look like?

---

## ✨ Features

### Core Functionality

| Feature | Description |
|---------|-------------|
| **7 Interactive Pages** | Comprehensive coverage of workforce AI impact |
| **39 Visualizations** | Diverse chart types for multi-faceted analysis |
| **Dynamic Filtering** | Real-time data filtering by country, industry, job level, etc. |
| **Key Insights** | Auto-generated insights after every visualization |
| **Data Export** | Download filtered data as CSV |
| **Responsive Design** | Works on desktop and tablet devices |

### Accessibility

- ✅ **Colorblind-Safe Palettes** - IBM Design Library compliant colors
- ✅ **High Contrast** - WCAG AA compliant contrast ratios
- ✅ **Clear Labels** - All charts are self-explanatory
- ✅ **Interactive Tooltips** - Detailed information on hover

---

## 📑 Dashboard Pages

### Page 1: 📌 Executive Summary
High-level KPIs and overview metrics with sparklines, providing a quick snapshot of the entire dataset.

**Visualizations:**
- KPI Cards with Sparklines
- Pie Chart (Country Distribution)
- Donut Chart (Employment Type)
- Bar Chart (Industry Distribution)
- Line Chart (Trend Analysis)
- Histogram (Risk Distribution)

---

### Page 2: 📊 Automation Risk Analysis
Deep dive into automation vulnerability across industries, job categories, and roles.

**Visualizations:**
- Horizontal Bar Chart (Risk by Industry)
- Bubble Chart (Risk vs Salary vs Count)
- Violin Plot (Risk Distribution by Country)
- Box Plot (Years to Automation)
- Treemap (Job Titles by Risk)
- Sunburst Chart (Industry → Category → Level Hierarchy)
- Scatter Plot (Risk vs AI Augmentation)

---

### Page 3: 💼 Skills & Training Analysis
Assessment of workforce capabilities, skill gaps, and training investments.

**Visualizations:**
- Grouped Bar Chart (Skill Scores by Country)
- Heatmap (Skill Gap by Industry & Level)
- Area Chart (Training Investment Trend)
- Scatter Plot (AI Literacy vs Risk)
- Correlation Matrix (Skill Variables)
- Stacked Bar Chart (Certifications by Level)

---

### Page 4: 💰 Economic Impact Analysis
Financial implications of AI on salaries, job security, and career prospects.

**Visualizations:**
- Grouped Bar Chart (Salary by Country & Level)
- Box Plot (Salary Distribution)
- Bar Chart (Wage Premium for AI Skills)
- Slope Chart (Current vs 2030 Salary Projection)
- Quadrant Scatter (Job Security vs Displacement)

---

### Page 5: 🧠 Workforce Sentiment
Worker attitudes toward AI, reskilling willingness, and job satisfaction.

**Visualizations:**
- Bar Chart (AI Anxiety by Age)
- Donut Chart (AI Benefit Perception)
- Stacked Bar Chart (Reskilling Willingness)
- Heatmap (Job Satisfaction by Industry & Level)
- Parallel Coordinates (Multi-dimensional Sentiment)

---

### Page 6: 🌍 Geographic Analysis
Regional patterns across Indian states and UAE emirates.

**Visualizations:**
- Choropleth/Point Map (India State-wise Metrics)
- Grouped Bar Chart (UAE Emirates Comparison)
- Grouped Bar Chart (City Tier Analysis)
- Radar Chart (Economic Zone Profiles)
- Calendar Heatmap (Data by Year)

---

### Page 7: 🤖 AI/ML Analytics
Advanced analytics using machine learning techniques.

**Visualizations:**
- Confusion Matrix (Job Transformation Matrix)
- ROC-style Curve (Risk-Benefit Tradeoff)
- Learning Curves (Training Impact)
- Feature Importance Chart (Risk Drivers)
- PCA Scatter Plot (Workforce Clustering)

---

## 📈 Chart Types Implemented

This dashboard implements **28 unique chart types** as required by the course curriculum:

### Comparison Charts
- [x] Bar Chart
- [x] Grouped Bar Chart
- [x] Stacked Bar Chart
- [x] Dot Plot / Lollipop Chart

### Temporal Charts
- [x] Line Chart
- [x] Area Chart
- [x] Sparklines
- [x] Slope Chart

### Distribution Charts
- [x] Histogram
- [x] Box Plot
- [x] Violin Plot

### Relationship Charts
- [x] Scatter Plot
- [x] Bubble Chart
- [x] Heatmap
- [x] Correlation Matrix

### Part-to-Whole Charts
- [x] Pie Chart
- [x] Donut Chart
- [x] Treemap
- [x] Sunburst Chart

### Geospatial Charts
- [x] Choropleth Map
- [x] Point/Symbol Map

### Specialized Charts
- [x] Radar Chart
- [x] Parallel Coordinates
- [x] Calendar Heatmap

### AI/ML Charts
- [x] Confusion Matrix
- [x] ROC Curve
- [x] Learning Curves
- [x] Feature Importance Chart
- [x] Dimensionality Reduction (PCA)

---

## 📊 Dataset Information

### Overview

| Attribute | Value |
|-----------|-------|
| **Total Records** | 5,000 |
| **Total Features** | 63 |
| **Countries** | India (70%), UAE (30%) |
| **Industries** | 12 |
| **Job Categories** | 10 |
| **Time Period** | 2020-2030 |

### Feature Categories
├── Identification & Classification (10 columns)
│   └── record_id, country, state_emirate, city_tier, economic_zone, etc.
│
├── Worker Demographics (6 columns)
│   └── age_group, gender, education_level, years_of_experience, etc.
│
├── AI & Automation Metrics (10 columns)
│   └── automation_risk_score, ai_augmentation_potential, ai_exposure_index, etc.
│
├── Skills & Training (10 columns)
│   └── technical_skill_score, ai_literacy_score, skill_gap_index, etc.
│
├── Economic & Employment (10 columns)
│   └── annual_salary_usd, job_security_index, career_growth_potential, etc.
│
├── Temporal & Projection (6 columns)
│   └── observation_year, demand_forecast_2030, projected_salary_2030_usd, etc.
│
├── Sentiment & Perception (8 columns)
│   └── ai_anxiety_level, ai_optimism_level, reskilling_willingness, etc.
│
└── Organizational Context (5 columns)
└── company_ai_investment_millions, team_size, ai_tools_available_count, etc.
### Geographic Coverage

**India (36 States/UTs):**
Maharashtra, Karnataka, Tamil Nadu, Telangana, Delhi NCT, Gujarat, Haryana, West Bengal, Uttar Pradesh, Kerala, Rajasthan, Madhya Pradesh, Punjab, Andhra Pradesh, Bihar, Odisha, Jharkhand, Chhattisgarh, Assam, Uttarakhand, Himachal Pradesh, Goa, Chandigarh, Puducherry, Jammu and Kashmir, Tripura, Meghalaya, Manipur, Nagaland, Arunachal Pradesh, Mizoram, Sikkim, Ladakh, Andaman and Nicobar Islands, Lakshadweep, Dadra and Nagar Haveli and Daman and Diu

**UAE (7 Emirates):**
Dubai, Abu Dhabi, Sharjah, Ajman, Ras Al Khaimah, Fujairah, Umm Al Quwain

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Git (optional)

### Step 1: Clone or Download the Repository

```bash
# Option A: Clone via Git
git clone https://github.com/yourusername/ai-future-of-work-dashboard.git
cd ai-future-of-work-dashboard

# Option B: Or simply create a folder and add the files manually
mkdir ai-future-of-work-dashboard
cd ai-future-of-work-dashboard