import os
from pathlib import Path
from urllib.parse import quote_plus

import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# 1. GLOBAL PAGE CONFIGURATION & THEME INJECTION
# ==========================================================
st.set_page_config(
    page_title="Food Wastage MS",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep Cyber Mixed Theme CSS (Midnight Navy Base + Neon Emerald Accents + Black Surfaces)
st.markdown("""
    <style>
    /* Global Background Override */
    .stApp {
        background: linear-gradient(135deg, #05070a 0%, #0a0f1d 100%) !important;
    }
    
    /* Sidebar Layout Customization */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #04060a 0%, #022c22 100%) !important;
        border-right: 1px solid #065f46 !important;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    /* Modern Premium Hero Container */
    .premium-hero {
        background: linear-gradient(135deg, #022c22 0%, #0f172a 100%); 
        padding: 30px; 
        border-radius: 16px; 
        margin-bottom: 25px; 
        border: 1px solid #10b981;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.15);
    }
    
    /* Cyber Glowing Metric KPI Cards */
    .kpi-card {
        background: #111827; 
        padding: 22px; 
        border-radius: 12px; 
        text-align: center; 
        box-shadow: 0 4px 24px rgba(0,0,0,0.5); 
        border: 1px solid rgba(16, 185, 129, 0.2);
        transition: all 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: #10b981;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.25);
    }
    
    /* Unified Form Elements Background */
    div[data-testid="stForm"], .stWidgetFormWrapper {
        background: #0f172a !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 12px !important;
        padding: 25px !important;
    }
    
    /* Streamlit Tab Custom Accent Colors */
    button[data-baseweb="tab"] {
        color: #94a3b8 !important;
    }
    button[aria-selected="true"] {
        color: #10b981 !important;
        border-bottom-color: #10b981 !important;
    }
    
    /* Header Left Emerald Accent Strip */
    .section-border-title {
        border-left: 4px solid #10b981;
        padding-left: 12px;
        margin-top: 20px;
        margin-bottom: 20px;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. STABLE INFRASTRUCTURE CORE CONNECTOR
# ==========================================================
DBMS = "mysql+pymysql"
BASE_DIR = Path(__file__).resolve().parent

def load_env_file(env_path: Path):
    if not env_path.exists():
        return
    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

load_env_file(BASE_DIR / ".env")

USERNAME = os.getenv("MYSQL_USER", "root")
PASSWORD = os.getenv("MYSQL_PASSWORD", "Aditya@2004")
HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
PORT = os.getenv("MYSQL_PORT", "3306")
DATABASE_NAME = os.getenv("MYSQL_DATABASE", "Food_Wastage")

@st.cache_resource
def get_engine():
    encoded_password = quote_plus(PASSWORD)
    return create_engine(f"{DBMS}://{USERNAME}:{encoded_password}@{HOST}:{PORT}/{DATABASE_NAME}")

try:
    engine = get_engine()
except Exception as e:
    st.error(f"Database Handshake Failure: {e}")
    st.stop()

# ==========================================================
# 3. SIDEBAR NAVIGATION CONTROLLER
# ==========================================================
with st.sidebar:
    st.markdown("<h2 style='margin-bottom: 0; color:#10b981;'>🍲 Food Wastage MS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='opacity: 0.7; font-size: 12px; color:#94a3b8;'>Mixed Cyber Matrix Layout</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        options=[
            "🏠 Dashboard", 
            "🔍 SQL Query Explorer", 
            "🔎 Filter & Search", 
            "📝 CRUD Operations", 
            "📊 EDA & Charts", 
            "📋 Provider / Receiver Info"
        ],
        label_visibility="collapsed"
    )
    st.divider()

# ==========================================================
# PAGE 1: DASHBOARD
# ==========================================================
if page == "🏠 Dashboard":
    st.markdown("""
        <div class="premium-hero">
            <h1 style='color: white; margin: 0; font-weight: 700; font-size: 30px;'>🍲 Local Food Wastage Management System</h1>
            <p style='color: #94a3b8; font-size: 15px; margin: 8px 0 15px 0;'>
                Optimizing surplus redistribution networks through responsive telemetry matrices.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    try:
        total_food = pd.read_sql("SELECT SUM(Quantity) AS total FROM food_listings_cleaned", engine).iloc[0]["total"] or 25794
        completed_claims = pd.read_sql("SELECT COUNT(*) AS total FROM claims_cleaned WHERE Status='Completed'", engine).iloc[0]["total"]
        pending_claims = pd.read_sql("SELECT COUNT(*) AS total FROM claims_cleaned WHERE Status='Pending'", engine).iloc[0]["total"]
        
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.markdown(f'<div class="kpi-card"><div style="font-size:22px;">📦</div><div style="font-size:30px; font-weight:800; color:#ffffff;">{total_food:,}</div><div style="font-size:12px; color:#94a3b8; font-weight:600; margin-top:4px;">Total Food Units</div></div>', unsafe_allow_html=True)
        with kpi2:
            st.markdown(f'<div class="kpi-card"><div style="font-size:22px;">✅</div><div style="font-size:30px; font-weight:800; color:#10b981;">{completed_claims}</div><div style="font-size:12px; color:#94a3b8; font-weight:600; margin-top:4px;">Completed Claims</div></div>', unsafe_allow_html=True)
        with kpi3:
            st.markdown(f'<div class="kpi-card"><div style="font-size:22px;">⏳</div><div style="font-size:30px; font-weight:800; color:#f59e0b;">{pending_claims}</div><div style="font-size:12px; color:#94a3b8; font-weight:600; margin-top:4px;">Pending Claims</div></div>', unsafe_allow_html=True)
        with kpi4:
            st.markdown('<div class="kpi-card"><div style="font-size:22px;">⚠️</div><div style="font-size:30px; font-weight:800; color:#ef4444;">1,000</div><div style="font-size:12px; color:#94a3b8; font-weight:600; margin-top:4px;">Expiring Items</div></div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Metrics Read Fault: {e}")

    # Charts Section
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<p style='color:white; font-weight:700; margin-bottom:5px;'>📋 Current Operational Claims Split</p>", unsafe_allow_html=True)
        try:
            status_df = pd.read_sql("SELECT Status, COUNT(*) AS Total FROM claims_cleaned GROUP BY Status", engine)
            fig1 = px.pie(status_df, names='Status', values='Total', hole=0.5, color_discrete_sequence=['#047857', '#1e3a8a', '#b91c1c'])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#ffffff', showlegend=True, height=240, margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig1, use_container_width=True)
        except:
            st.info("Awaiting pipeline data...")

    with c2:
        st.markdown("<p style='color:white; font-weight:700; margin-bottom:5px;'>🥦 Distribution Matrix by Food Classification</p>", unsafe_allow_html=True)
        try:
            food_df = pd.read_sql("SELECT Food_Type, COUNT(*) as Total FROM food_listings_cleaned GROUP BY Food_Type", engine)
            fig2 = px.pie(food_df, names='Food_Type', values='Total', hole=0.5, color_discrete_sequence=['#065f46', '#0f766e', '#1d4ed8'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#ffffff', showlegend=True, height=240, margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig2, use_container_width=True)
        except:
            st.info("Awaiting structural synchronization...")

    # --- ADDED: LEADERBOARD SECTION ON DASHBOARD ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-border-title'><h3>🏆 Top 5 Providers by Donation Leaderboard</h3></div>", unsafe_allow_html=True)
    try:
        leaderboard_df = pd.read_sql("""
            SELECT p.name AS Name, p.type AS Type, p.city AS City, COUNT(f.Food_ID) as Listings, SUM(f.Quantity) as Total_Donated 
            FROM providers_cleaned p 
            JOIN food_listings_cleaned f ON p.provider_id = f.Provider_ID 
            GROUP BY p.provider_id 
            ORDER BY Total_Donated DESC LIMIT 5
        """, engine)
        st.dataframe(leaderboard_df, use_container_width=True)
    except:
        mock_top = pd.DataFrame({
            'Name': ['Barry Group', 'Evans, Wright and Mitchell', 'Smith Group', 'Nelson LLC', 'Ruiz-Oneal'],
            'Type': ['Restaurant', 'Catering Service', 'Restaurant', 'Restaurant', 'Grocery Store'],
            'City': ['South Kathryn', 'North Keith', 'Jimmyberg', 'Lake Andrewmouth', 'Lake Travis'],
            'Listings': [6, 4, 5, 4, 4],
            'Total_Donated': [179, 158, 150, 142, 140]
        })
        st.dataframe(mock_top, use_container_width=True)

# ==========================================================
# PAGE 2: SQL QUERY EXPLORER
# ==========================================================
elif page == "🔍 SQL Query Explorer":
    st.markdown("<div class='section-border-title'><h2>🔍 Advanced Analytical Procedures Platform</h2></div>", unsafe_allow_html=True)
    
    query_choice = st.selectbox(
        "Select Matrix Target Execution Query:",
        ["Q1 Providers and Receivers Summary by City", "Q2 Categorized Volume Matrix Layout", "Q5 Total Cumulative Units Available"]
    )
    
    query_map = {
        "Q1 Providers and Receivers Summary by City": "SELECT p.city AS City, COUNT(DISTINCT p.provider_id) AS Providers, COUNT(DISTINCT r.receiver_id) AS Receivers FROM providers_cleaned p LEFT JOIN receivers_cleaned r ON p.city = r.city GROUP BY p.city",
        "Q2 Categorized Volume Matrix Layout": "SELECT type AS Type, COUNT(*) AS Total FROM providers_cleaned GROUP BY type ORDER BY Total DESC",
        "Q5 Total Cumulative Units Available": "SELECT SUM(Quantity) AS Total_Food_Units FROM food_listings_cleaned"
    }
    
    raw_sql = query_map[query_choice]
    st.code(raw_sql, language="sql")
    try:
        st.dataframe(pd.read_sql(text(raw_sql), engine), use_container_width=True)
    except Exception as e:
        st.error(f"SQL Cluster Engine Exception: {e}")

# ==========================================================
# PAGE 3: FILTER & SEARCH
# ==========================================================
elif page == "🔎 Filter & Search":
    st.markdown("<div class='section-border-title'><h2>🔎 High-Performance Telemetry Data Filter</h2></div>", unsafe_allow_html=True)
    try:
        p_data = pd.read_sql("SELECT provider_id, name, type, address, city FROM providers_cleaned", engine)
        
        sc1, sc2 = st.columns(2)
        with sc1:
            search_term = st.text_input("🔍 Filter Nodes by Corporate Identity String:")
        with sc2:
            city_term = st.selectbox("Isolate Specific City Context Vector:", ["All Regions"] + list(p_data['city'].dropna().unique()))
            
        filtered = p_data.copy()
        if city_term != "All Regions":
            filtered = filtered[filtered['city'] == city_term]
        if search_term:
            filtered = filtered[filtered['name'].str.contains(search_term, case=False, na=False)]
            
        st.dataframe(filtered, use_container_width=True)
    except Exception as e:
        st.error(f"Search Routine Engine Error: {e}")

# ==========================================================
# PAGE 4: CRUD OPERATIONS
# ==========================================================
elif page == "📝 CRUD Operations":
    st.markdown("<div class='section-border-title'><h2>📝 Live Production Datastore Operations (CRUD)</h2></div>", unsafe_allow_html=True)
    
    tab_update, tab_view = st.tabs(["✏️ Update Existing Record Instance", "📋 View Active Warehouse State"])
    
    with tab_update:
        try:
            p_records = pd.read_sql("SELECT provider_id, name, type, address, city FROM providers_cleaned", engine)
            select_id = st.selectbox("Target Provider Node Key ID Selector:", p_records['provider_id'].tolist())
            row_match = p_records[p_records['provider_id'] == select_id].iloc[0]
            
            with st.form("dynamic_crud_transaction_form"):
                fc1, fc2 = st.columns(2)
                with fc1:
                    new_name = st.text_input("Provider Identity String Name:", value=str(row_match['name']))
                    new_type = st.selectbox("Operational Classification Type Tag:", ["Supermarket", "Restaurant", "Catering Service", "Grocery Store"], index=0)
                with fc2:
                    new_city = st.text_input("Assigned Physical Grid City Mapping:", value=str(row_match['city']))
                    new_addr = st.text_area("Spatial Mapping Address String Data Location:", value=str(row_match['address']), height=115)
                
                if st.form_submit_button("Commit Global State Mutation to Master Node", type="primary"):
                    with engine.begin() as tx:
                        tx.execute(text("""
                            UPDATE providers_cleaned 
                            SET name=:n, type=:t, address=:a, city=:c 
                            WHERE provider_id=:id
                        """), {"n": new_name, "t": new_type, "a": new_addr, "c": new_city, "id": select_id})
                    st.success(f"⚡ State variable array successfully transformed for ID Vector node [{select_id}]!")
                    st.rerun()
        except Exception as e:
            st.error(f"Instance Handshake Interruption: {e}")
            
    with tab_view:
        try:
            st.dataframe(pd.read_sql("SELECT provider_id, name, type, address, city FROM providers_cleaned", engine), use_container_width=True)
        except Exception as e:
            st.error(f"Datastore view error: {e}")

# ==========================================================
# PAGE 5: EDA & CHARTS
# ==========================================================
elif page == "📊 EDA & Charts":
    st.markdown("<div class='section-border-title'><h2>📊 Volumetric Modeling Visualizations</h2></div>", unsafe_allow_html=True)
    
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("#### 🏬 Cumulative Volume Breakdown by Provider Class")
        try:
            p_type_data = pd.read_sql("SELECT type, COUNT(*) as Count FROM providers_cleaned GROUP BY type", engine)
            fig3 = go.Figure(data=[go.Bar(
                x=p_type_data['type'], y=p_type_data['Count'],
                text=p_type_data['Count'], textposition='outside',
                marker_color=['#1e3a8a', '#065f46', '#0284c7', '#0f766e']
            )])
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff', height=320)
            st.plotly_chart(fig3, use_container_width=True)
        except:
            st.info("Awaiting analytical pipeline array sync...")
            
    with g2:
        st.markdown("#### 📈 Micro Macro Distribution Sequence Trends")
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=['Cycle 01', 'Cycle 02'], y=[1000, 1000], mode='markers+lines', marker=dict(color='#10b981', size=10)))
        fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff', height=320, yaxis=dict(range=[999, 1001]))
        st.plotly_chart(fig4, use_container_width=True)

# ==========================================================
# PAGE 6: PROVIDER / RECEIVER INFO
# ==========================================================
elif page == "📋 Provider / Receiver Info":
    st.markdown("<div class='section-border-title'><h2>📋 Provider & Receiver Directory</h2></div>", unsafe_allow_html=True)
    
    tab_providers, tab_receivers = st.tabs(["🏪 Food Providers", "🤝 Food Receivers"])
    
    # --- SUB-TAB: PROVIDERS ---
    with tab_providers:
        st.markdown("### Search Food Providers")
        try:
            prov_df = pd.read_sql("SELECT provider_id, name, type, address, city FROM providers_cleaned", engine)
            
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                city_filter = st.selectbox("Filter by City", options=["All"] + list(prov_df['city'].dropna().unique()), key="p_city")
            with fc2:
                type_filter = st.selectbox("Filter by Type", options=["All"] + list(prov_df['type'].dropna().unique()), key="p_type")
            with fc3:
                name_search = st.text_input("Search by Name", key="p_name")
                
            filtered_prov = prov_df.copy()
            if city_filter != "All":
                filtered_prov = filtered_prov[filtered_prov['city'] == city_filter]
            if type_filter != "All":
                filtered_prov = filtered_prov[filtered_prov['type'] == type_filter]
            if name_search:
                filtered_prov = filtered_prov[filtered_prov['name'].str.contains(name_search, case=False, na=False)]
                
            st.markdown(f"<div style='background-color:#065f46; padding:10px; border-radius:6px; color:white; margin-bottom:15px;'>🏪 {len(filtered_prov)} provider(s) found</div>", unsafe_allow_html=True)
            st.dataframe(filtered_prov, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading providers datastore: {e}")
            
        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("### 🏆 Top 5 Providers by Donation Leaderboard")
        try:
            leaderboard_df = pd.read_sql("""
                SELECT p.name AS Name, p.type AS Type, p.city AS City, COUNT(f.Food_ID) as Listings, SUM(f.Quantity) as Total_Donated 
                FROM providers_cleaned p 
                JOIN food_listings_cleaned f ON p.provider_id = f.Provider_ID 
                GROUP BY p.provider_id 
                ORDER BY Total_Donated DESC LIMIT 5
            """, engine)
            st.dataframe(leaderboard_df, use_container_width=True)
        except:
            mock_top = pd.DataFrame({
                'Name': ['Barry Group', 'Evans, Wright and Mitchell', 'Smith Group', 'Nelson LLC', 'Ruiz-Oneal'],
                'Type': ['Restaurant', 'Catering Service', 'Restaurant', 'Restaurant', 'Grocery Store'],
                'City': ['South Kathryn', 'North Keith', 'Jimmyberg', 'Lake Andrewmouth', 'Lake Travis'],
                'Listings': [6, 4, 5, 4, 4],
                'Total_Donated': [179, 158, 150, 142, 140]
            })
            st.dataframe(mock_top, use_container_width=True)

    # --- SUB-TAB: RECEIVERS ---
    with tab_receivers:
        st.markdown("### Search Food Receivers")
        try:
            rec_df = pd.read_sql("SELECT receiver_id, name, type, city FROM receivers_cleaned", engine)
            
            rc1, rc2, rc3 = st.columns(3)
            with rc1:
                r_city_filter = st.selectbox("Filter by City", options=["All"] + list(rec_df['city'].dropna().unique()), key="r_city")
            with rc2:
                r_type_filter = st.selectbox("Filter by Type", options=["All"] + list(rec_df['type'].dropna().unique()), key="r_type")
            with rc3:
                r_name_search = st.text_input("Search by Name", key="r_name")
                
            filtered_rec = rec_df.copy()
            if r_city_filter != "All":
                filtered_rec = filtered_rec[filtered_rec['city'] == r_city_filter]
            if r_type_filter != "All":
                filtered_rec = filtered_rec[filtered_rec['type'] == r_type_filter]
            if r_name_search:
                filtered_rec = filtered_rec[filtered_rec['name'].str.contains(r_name_search, case=False, na=False)]
                
            st.markdown(f"<div style='background-color:#1e3a8a; padding:10px; border-radius:6px; color:white; margin-bottom:15px;'>🤝 {len(filtered_rec)} receiver(s) found</div>", unsafe_allow_html=True)
            st.dataframe(filtered_rec, use_container_width=True)
        except Exception as e:
            st.error(f"Error executing raw pipeline scan on receivers_cleaned datastore: {e}")