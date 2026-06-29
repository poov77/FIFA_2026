import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="FIFA 2026 AI Predictor",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional sports dashboard aesthetic
st.markdown("""
    <style>
    /* Main background and text */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    /* Metric Cards */
    [data-testid="stMetric"] {
        background-color: #1E2329;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #2D333B;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    [data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: bold;
        color: #00FF87; /* Sports Neon Green */
    }
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA LOADING & PREPROCESSING
# ==========================================
from pathlib import Path

@st.cache_data
def load_and_process_data():
    file_path = Path(__file__).resolve().parent / "FIFA World Cup Dataset.csv.xlsx"

    if not file_path.exists():
        st.error(f"Dataset not found: {file_path}. Please ensure it is in the same directory as the app.")
        return pd.DataFrame()

    try:
        df = pd.read_excel(file_path)
    except Exception as exc:
        st.error(f"Unable to read dataset: {exc}")
        return pd.DataFrame()

    if df.empty:
        st.warning("The dataset appears to be empty.")
        return pd.DataFrame()

    df = df.copy()
    df = df.fillna(0)

    numeric_cols = [
        'fifa_points_pre_tournament',
        'squad_total_market_value_eur',
        'world_cup_titles_before',
        'goals_scored_last_4y',
        'goals_received_last_4y',
        'wins_last_4y',
        'fifa_rank_pre_tournament',
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    scaler = MinMaxScaler()

    win_features = ['fifa_points_pre_tournament', 'squad_total_market_value_eur', 'world_cup_titles_before']
    scaled_win = scaler.fit_transform(df[win_features])
    df['win_score'] = (scaled_win * [0.5, 0.4, 0.1]).sum(axis=1)
    df['Winning Probability (%)'] = (df['win_score'] / df['win_score'].sum()) * 100

    attack_features = ['goals_scored_last_4y', 'squad_total_market_value_eur']
    scaled_attack = scaler.fit_transform(df[attack_features])
    df['Attack Score'] = (scaled_attack * [0.6, 0.4]).sum(axis=1) * 100

    df['inverse_goals_received'] = df['goals_received_last_4y'].max() - df['goals_received_last_4y']
    def_features = ['inverse_goals_received', 'wins_last_4y']
    scaled_def = scaler.fit_transform(df[def_features])
    df['Defense Score'] = (scaled_def * [0.6, 0.4]).sum(axis=1) * 100

    return df

df = load_and_process_data()

if df.empty:
    st.error("The dashboard could not load because the dataset was unavailable.")
    st.stop()

# ==========================================
# 3. SIDEBAR NAVIGATION & FILTERS
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5328/5328087.png", width=80)
    st.title("FIFA '26 Analytics")
    st.markdown("*Advanced Heuristic Prediction Engine*")
    st.markdown("---")
    
    st.markdown("### 🎛️ Dashboard Controls")
    continents = ["All"] + list(df['continent'].unique()) if not df.empty else ["All"]
    selected_continent = st.selectbox("Filter by Continent", continents)
    
    st.markdown("---")
    st.markdown("""
    **Validation & Tech Stack:**
    * ✅ Python & Pandas
    * ✅ Scikit-Learn (MinMax)
    * ✅ Streamlit UI/UX
    * 📍 *Designed for Indian Football Club Analytics*
    """)

# Filter dataframe based on sidebar
if selected_continent != "All":
    display_df = df[df['continent'] == selected_continent]
else:
    display_df = df

# ==========================================
# 4. MAIN DASHBOARD UI
# ==========================================
st.title("🏆 2026 FIFA World Cup: Predictive Analytics Dashboard")
st.markdown("Utilizing market value, historical performance, and FIFA coefficients to forecast tournament outcomes.")

if not display_df.empty:
    # --- Top Level KPIs ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    best_overall = df.sort_values('Winning Probability (%)', ascending=False).iloc[0]
    best_attack = df.sort_values('Attack Score', ascending=False).iloc[0]
    best_defense = df.sort_values('Defense Score', ascending=False).iloc[0]
    
    kpi1.metric("Tournament Favorite", best_overall['team'], f"{best_overall['Winning Probability (%)']:.2f}% Win Chance")
    kpi2.metric("Most Expensive Squad", "England", "€1.30 Billion")
    kpi3.metric("Deadliest Attack", best_attack['team'], f"{int(best_attack['goals_scored_last_4y'])} Goals (4y)")
    kpi4.metric("Strongest Defense", best_defense['team'], f"Only {int(best_defense['goals_received_last_4y'])} Conceded")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Analytics Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Tournament Winner", "⚔️ Predicted Final Four", "🚀 Attacking Powerhouses", "🐴 Dark Horses"])

    # TAB 1: Tournament Winner
    with tab1:
        st.subheader("Win Probability Rankings")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Interactive Bar Chart
            top_15 = display_df.sort_values('Winning Probability (%)', ascending=False).head(15)
            fig = px.bar(top_15, x='team', y='Winning Probability (%)', 
                         text=top_15['Winning Probability (%)'].apply(lambda x: f'{x:.2f}%'),
                         color='Winning Probability (%)', color_continuous_scale='viridis',
                         labels={'team': 'National Team'}, title="Top 15 Favorites to Win")
            fig.update_layout(xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("**Probability Table**")
            table_df = top_15[['team', 'continent', 'Winning Probability (%)']].copy()
            table_df['Winning Probability (%)'] = table_df['Winning Probability (%)'].round(2).astype(str) + "%"
            st.dataframe(table_df, use_container_width=True, hide_index=True)

    # TAB 2: Final Four
    with tab2:
        st.subheader("Predicted Semi-Finalists")
        st.markdown("The 4 teams mathematically most likely to survive the knockout stages based on combined squad depth and tournament pedigree.")
        
        final_four = df.sort_values('Winning Probability (%)', ascending=False).head(4)
        ff_cols = st.columns(4)
        
        for idx, col in enumerate(ff_cols):
            team_data = final_four.iloc[idx]
            with col:
                st.markdown(f"<h2 style='text-align: center; color: #00FF87;'>{team_data['team']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'>{team_data['continent']}</p>", unsafe_allow_html=True)
                st.metric("FIFA Rank", int(team_data['fifa_rank_pre_tournament']))
                st.metric("Squad Value", f"€{team_data['squad_total_market_value_eur']/1000000:.0f}M")

    # TAB 3: Attacking Power
    with tab3:
        st.subheader("Goals Scored vs. Market Value")
        st.markdown("Visualizing which teams have the highest attacking output relative to their squad cost.")
        
        fig2 = px.scatter(display_df, x='squad_total_market_value_eur', y='goals_scored_last_4y',
                          size='Attack Score', color='continent', hover_name='team',
                          labels={'squad_total_market_value_eur': 'Total Market Value (€)', 
                                  'goals_scored_last_4y': 'Goals Scored (Last 4 Years)'},
                          title="Attacking Efficiency Matrix")
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig2, use_container_width=True)

    # TAB 4: Dark Horses
    with tab4:
        st.subheader("Dangerous Underdogs (Dark Horses)")
        st.markdown("Teams ranked **outside the FIFA Top 10**, but boasting high win rates and solid fundamentals in the last 4 years.")
        
        # Filter for teams ranked > 10, then sort by Defense and Attack scores
        underdogs = df[df['fifa_rank_pre_tournament'] > 10].copy()
        underdogs['Dark Horse Score'] = underdogs['Attack Score'] + underdogs['Defense Score']
        top_underdogs = underdogs.sort_values('Dark Horse Score', ascending=False).head(5)
        
        for _, row in top_underdogs.iterrows():
            with st.expander(f"🐴 {row['team']} (Rank: {int(row['fifa_rank_pre_tournament'])})"):
                st.write(f"**Why they are dangerous:** {row['team']} has won {int(row['wins_last_4y'])} games in the last 4 years and scored {int(row['goals_scored_last_4y'])} goals. Their squad is valued at €{row['squad_total_market_value_eur']/1000000:.1f} Million.")
                st.progress(int(row['Dark Horse Score'] / 2)) # Visual progress bar for their threat level