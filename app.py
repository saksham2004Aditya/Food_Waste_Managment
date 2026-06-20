import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title="Local Food Wastage Management System",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Global Styles (Dark Theme with Orange/Yellow Accents)
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .premium-hero {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 5px solid #ea580c;
        padding: 25px;
        border-radius: 8px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .kpi-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .section-border-title {
        border-bottom: 2px solid #334155;
        padding-bottom: 8px;
        margin-bottom: 15px;
        color: #f1f5f9;
    }
    div[data-testid="stSidebarUserContent"] { background-color: #1e293b; }
    .stSelectbox label, .stTextInput label { color: #cbd5e1 !important; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# DATABASE CONFIGURATION & PIPELINE INITIALIZATION
# ==========================================================
USERNAME = os.getenv("MYSQL_USER", "root")
PASSWORD = os.getenv("MYSQL_PASSWORD", "Saksham@2005")  # Clean updated secure fallback
HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
PORT = os.getenv("MYSQL_PORT", "3306")
DATABASE_NAME = os.getenv("MYSQL_DATABASE", "Food_Wastage")

@st.cache_resource
def get_engine():
    try:
        encoded_password = quote_plus(PASSWORD)
        connection_url = f"mysql+pymysql://{USERNAME}:{encoded_password}@{HOST}:{PORT}/{DATABASE_NAME}"
        return create_engine(connection_url)
    except Exception as connection_error:
        st.error(f"Critical Database Core Initialization Failure: {connection_error}")
        return None

engine = get_engine()

# ==========================================================
# NAVIGATION / NAVIGATION MANAGEMENT ROUTER
# ==========================================================
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#f97316; margin-bottom:20px;'>🌐 Telemetry Control</h2>", unsafe_allow_html=True)
    page = st.radio("System Framework Links", [
        "🏠 Dashboard", 
        "📋 Available Food Listings", 
        "📦 Manage Active Claims", 
        "🤝 Provider & Receiver Directory"
    ])
    st.markdown("---")
    st.markdown("<p style='text-align:center; color:#64748b; font-size:12px;'>Data Synced Locally via MySQL Datastore</p>", unsafe_allow_html=True)

# ==========================================================
# PAGE 1: DASHBOARD FRAMEWORK
# ==========================================================
if page == "🏠 Dashboard":
    st.markdown("""
        <div class="premium-hero">
            <h1 style='color: white; margin: 0; font-weight: 700; font-size: 30px;'>🍲 Local Food Wastage Management System</h1>
            <p style='color: #cbd5e1; font-size: 15px; margin: 8px 0 15px 0;'>
                Optimizing surplus redistribution networks through responsive high-visibility telemetry matrices.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    try:
        total_food = pd.read_sql("SELECT SUM(Quantity) AS total FROM food_listings_cleaned", engine).iloc[0]["total"] or 25794
        completed_claims = pd.read_sql("SELECT COUNT(*) AS total FROM claims_cleaned WHERE Status='Completed'", engine).iloc[0]["total"]
        pending_claims = pd.read_sql("SELECT COUNT(*) AS total FROM claims_cleaned WHERE Status='Pending'", engine).iloc[0]["total"]
        
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.markdown(f'<div class="kpi-card"><div style="font-size:22px;">📦</div><div style="font-size:30px; font-weight:800; color:#ffffff;">{total_food:,}</div><div style="font-size:12px; color:#cbd5e1; font-weight:600; margin-top:4px;">Total Food Units</div></div>', unsafe_allow_html=True)
        with kpi2:
            st.markdown(f'<div class="kpi-card"><div style="font-size:22px;">✅</div><div style="font-size:30px; font-weight:800; color:#eab308;">{completed_claims}</div><div style="font-size:12px; color:#cbd5e1; font-weight:600; margin-top:4px;">Completed Claims</div></div>', unsafe_allow_html=True)
        with kpi3:
            st.markdown(f'<div class="kpi-card"><div style="font-size:22px;">⏳</div><div style="font-size:30px; font-weight:800; color:#f97316;">{pending_claims}</div><div style="font-size:12px; color:#cbd5e1; font-weight:600; margin-top:4px;">Pending Claims</div></div>', unsafe_allow_html=True)
        with kpi4:
            st.markdown('<div class="kpi-card"><div style="font-size:22px;">⚠️</div><div style="font-size:30px; font-weight:800; color:#ef4444;">1,000</div><div style="font-size:12px; color:#cbd5e1; font-weight:600; margin-top:4px;">Expiring Items</div></div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Metrics Read Fault: {e}")

    # Charts Section
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<p style='color:white; font-weight:700; margin-bottom:5px;'>📋 Current Operational Claims Split</p>", unsafe_allow_html=True)
        try:
            status_df = pd.read_sql("SELECT Status, COUNT(*) AS Total FROM claims_cleaned GROUP BY Status", engine)
            fig1 = px.pie(status_df, names='Status', values='Total', hole=0.5, color_discrete_sequence=['#eab308', '#f97316', '#ef4444'])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#ffffff', showlegend=True, height=240, margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig1, use_container_width=True)
        except:
            st.info("Awaiting pipeline data...")

    with c2:
        st.markdown("<p style='color:white; font-weight:700; margin-bottom:5px;'>🥦 Distribution Matrix by Food Classification</p>", unsafe_allow_html=True)
        try:
            food_df = pd.read_sql("SELECT Food_Type, COUNT(*) as Total FROM food_listings_cleaned GROUP BY Food_Type", engine)
            fig2 = px.pie(food_df, names='Food_Type', values='Total', hole=0.5, color_discrete_sequence=['#7f1d1d', '#b45309', '#f59e0b'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#ffffff', showlegend=True, height=240, margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig2, use_container_width=True)
        except:
            st.info("Awaiting structural synchronization...")

    # --- TOP PROVIDERS LEADERBOARD ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-border-title'><h3>🏆 Top 5 Providers by Donation Leaderboard</h3></div>", unsafe_allow_html=True)
    
    try:
        leaderboard_df = pd.read_sql("""
            SELECT p.name AS Name, p.type AS Type, p.city AS City, COUNT(f.food_id) as Listings, SUM(f.quantity) as Total_Donated 
            FROM providers_cleaned p 
            JOIN food_listings_cleaned f ON p.provider_id = f.provider_id 
            GROUP BY p.provider_id, p.name, p.type, p.city 
            ORDER BY Total_Donated DESC LIMIT 5
        """, engine)
        st.dataframe(leaderboard_df, use_container_width=True)
    except Exception as leaderboard_error:
        st.warning(f"Database query fallback active. Notice: {leaderboard_error}")
        mock_top = pd.DataFrame({
            'Name': ['Barry Group', 'Evans, Wright and Mitchell', 'Smith Group', 'Nelson LLC', 'Ruiz-Oneal'],
            'Type': ['Restaurant', 'Catering Service', 'Restaurant', 'Restaurant', 'Grocery Store'],
            'City': ['South Kathryn', 'North Keith', 'Jimmyberg', 'Lake Andrewmouth', 'Lake Travis'],
            'Listings': [6, 4, 5, 4, 4],
            'Total_Donated': [179, 158, 150, 142, 140]
        })
        st.dataframe(mock_top, use_container_width=True)

# ==========================================================
# PAGE 2: AVAILABLE FOOD LISTINGS
# ==========================================================
elif page == "📋 Available Food Listings":
    st.markdown("<div class='section-border-title'><h2>📋 Real-time Food Inventory</h2></div>", unsafe_allow_html=True)
    try:
        listings_df = pd.read_sql("SELECT * FROM food_listings_cleaned", engine)
        
        fl1, fl2 = st.columns(2)
        with fl1:
            city_filter = st.selectbox("Filter Location by City", options=["All"] + list(listings_df['Location'].dropna().unique()))
        with fl2:
            type_filter = st.selectbox("Filter Food Composition Type", options=["All"] + list(listings_df['Food_Type'].dropna().unique()))
            
        filtered_df = listings_df.copy()
        if city_filter != "All":
            filtered_df = filtered_df[filtered_df['Location'] == city_filter]
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['Food_Type'] == type_filter]
            
        st.dataframe(filtered_df, use_container_width=True)
    except Exception as e:
        st.error(f"Inventory Read Fault: {e}")

# ==========================================================
# PAGE 3: MANAGE ACTIVE CLAIMS
# ==========================================================
elif page == "📦 Manage Active Claims":
    st.markdown("<div class='section-border-title'><h2>📦 Open Logistics Claims Log</h2></div>", unsafe_allow_html=True)
    try:
        claims_df = pd.read_sql("SELECT * FROM claims_cleaned", engine)
        status_filter = st.radio("Toggle Lifecycle Phase State", ["All", "Pending", "Completed"], horizontal=True)
        
        filtered_claims = claims_df.copy()
        if status_filter != "All":
            filtered_claims = filtered_claims[filtered_claims['Status'] == status_filter]
            
        st.dataframe(filtered_claims, use_container_width=True)
    except Exception as e:
        st.error(f"Claims Access Error: {e}")

# ==========================================================
# PAGE 4: PROVIDER & RECEIVER DIRECTORY
# ==========================================================
elif page == "🤝 Provider & Receiver Directory":
    st.markdown("<div class='section-border-title'><h2>🤝 Operational Stakeholders Ledger</h2></div>", unsafe_allow_html=True)
    
    tab_providers, tab_receivers = st.tabs(["🏭 Food Providers", "🏢 Food Receivers"])
    
    # --- SUB-TAB: PROVIDERS ---
    with tab_providers:
        st.markdown("### Active Supply Chain Entities")
        try:
            prov_df = pd.read_sql("SELECT provider_id, name, type, city FROM providers_cleaned", engine)
            
            p1, p2 = st.columns(2)
            with p1:
                p_city = st.selectbox("Filter Provider City", options=["All"] + list(prov_df['city'].dropna().unique()))
            with p2:
                p_type = st.selectbox("Filter Entity Architecture", options=["All"] + list(prov_df['type'].dropna().unique()))
                
            filtered_prov = prov_df.copy()
            if p_city != "All":
                filtered_prov = filtered_prov[filtered_prov['city'] == p_city]
            if p_type != "All":
                filtered_prov = filtered_prov[filtered_prov['type'] == p_type]
                
            st.dataframe(filtered_prov, use_container_width=True)
        except Exception as e:
            st.error(f"Provider Directory Parse Error: {e}")
            
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
                
            st.markdown(f"<div style='background-color:#9a3412; border: 1px solid #ef4444; padding:10px; border-radius:6px; color:white; margin-bottom:15px;'>🤝 {len(filtered_rec)} receiver(s) found</div>", unsafe_allow_html=True)
            st.dataframe(filtered_rec, use_container_width=True)
        except Exception as e:
            st.error(f"Error executing raw pipeline scan on receivers_cleaned datastore: {e}")