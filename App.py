import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ─── Config page ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FraudShield · Détection de Fraude",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS personnalisé ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg: #0a0d14;
    --surface: #111520;
    --surface2: #161c2e;
    --border: #1e2a42;
    --accent: #00e5ff;
    --accent2: #ff4757;
    --accent3: #ffd32a;
    --text: #e8edf5;
    --muted: #6b7a99;
    --green: #2ed573;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif;
}

[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * { color: var(--text) !important; }

h1, h2, h3 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }

.stSelectbox > div > div,
.stSlider > div,
.stNumberInput > div {
    background-color: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.metric-card.accent::before { background: var(--accent); }
.metric-card.danger::before { background: var(--accent2); }
.metric-card.warn::before   { background: var(--accent3); }
.metric-card.ok::before     { background: var(--green); }

.metric-label {
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.1;
    margin-top: 0.3rem;
}
.metric-value.cyan  { color: var(--accent); }
.metric-value.red   { color: var(--accent2); }
.metric-value.yellow{ color: var(--accent3); }
.metric-value.green { color: var(--green); }

.section-title {
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

.fraud-badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
}
.badge-fraud { background: rgba(255,71,87,0.15); color: var(--accent2); border: 1px solid rgba(255,71,87,0.3); }
.badge-ok    { background: rgba(46,213,115,0.12); color: var(--green); border: 1px solid rgba(46,213,115,0.25); }

.predict-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
}
.predict-result-fraud {
    background: rgba(255,71,87,0.08);
    border: 2px solid var(--accent2);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
}
.predict-result-ok {
    background: rgba(46,213,115,0.06);
    border: 2px solid var(--green);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
}

/* Benefit cards */
.benefit-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem;
    height: 100%;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.benefit-card:hover { border-color: #00e5ff44; }
.benefit-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--green));
}
.benefit-icon { font-size: 1.8rem; margin-bottom: 0.6rem; }
.benefit-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.5rem;
}
.benefit-desc {
    font-size: 0.8rem;
    color: var(--muted);
    line-height: 1.6;
}
.benefit-stat {
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    margin-top: 0.6rem;
}

.free-card {
    background: linear-gradient(135deg, #0a0d14 0%, #0d1a2e 100%);
    border: 1px solid #00e5ff33;
    border-radius: 14px;
    padding: 1.4rem;
}
.free-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #ff4757, #ffd32a, #00e5ff);
}

.stat-highlight {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.stat-highlight .val {
    font-size: 1.8rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
}
.stat-highlight .lbl {
    font-size: 0.72rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.3rem;
}

.quote-box {
    background: var(--surface2);
    border-left: 3px solid var(--accent);
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    font-style: italic;
    color: var(--muted);
    font-size: 0.85rem;
    line-height: 1.7;
    margin: 1rem 0;
}

.timeline-item {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.2rem;
    align-items: flex-start;
}
.timeline-dot {
    min-width: 10px; height: 10px;
    border-radius: 50%;
    margin-top: 5px;
}
.timeline-content { flex: 1; }
.timeline-title { font-size: 0.88rem; font-weight: 700; color: var(--text); }
.timeline-desc  { font-size: 0.78rem; color: var(--muted); margin-top: 0.2rem; line-height: 1.5; }

/* Plotly transparent backgrounds */
.js-plotly-plot .plotly { background: transparent !important; }

[data-testid="stMetric"] { background: var(--surface); border-radius: 12px; padding: 1rem; border: 1px solid var(--border); }
div[data-testid="stDataFrame"] { background: var(--surface); }
.stButton > button {
    background: var(--accent) !important;
    color: #000 !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.8rem !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stTabs [data-baseweb="tab-list"] { background: var(--surface) !important; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { color: var(--muted) !important; font-family: 'Syne', sans-serif !important; font-weight: 600 !important; }
.stTabs [aria-selected="true"] { background: var(--surface2) !important; color: var(--accent) !important; border-radius: 8px !important; }

[data-testid="stMarkdownContainer"] p { color: var(--text); }
.stAlert { border-radius: 10px !important; }
div[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Syne, sans-serif', color='#e8edf5'),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor='#1e2a42', linecolor='#1e2a42'),
    yaxis=dict(gridcolor='#1e2a42', linecolor='#1e2a42'),
)

COLOR_FRAUD  = '#ff4757'
COLOR_OK     = '#2ed573'
COLOR_ACCENT = '#00e5ff'
COLOR_WARN   = '#ffd32a'

FRAUD_TYPE_LABELS = {
    'normal':         'Normal',
    'phishing':       'Phishing',
    'sim_swap':       'SIM Swap',
    'bypass_cash_in': 'Bypass Cash-In',
    'compte_interne': 'Intrusion Compte',
    'fermes_sim':     'Fermes SIM',
    'agent_complice': 'Agent Complice',
}

# ─── Chargement données ──────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('data/transactions.csv', parse_dates=['date'])
    df['day_of_week'] = df['date'].dt.dayofweek
    df['is_weekend']  = (df['day_of_week'] >= 5).astype(int)
    df['month']       = df['date'].dt.month
    df['day']         = df['date'].dt.day
    df['month_name']  = df['date'].dt.strftime('%b %Y')
    df['week']        = df['date'].dt.isocalendar().week.astype(int)

    def period(h):
        if h < 6:    return 'Nuit (0-6h)'
        elif h < 12: return 'Matin (6-12h)'
        elif h < 18: return 'Après-midi (12-18h)'
        else:        return 'Soir (18-24h)'

    df['period_of_day'] = df['hour'].apply(period)
    df['amount_log']    = np.log1p(df['amount'])
    avg = df['nb_transactions_24h'].mean()
    df['activity_ratio'] = df['nb_transactions_24h'] / avg
    df['risk_score'] = (
        df['changement_localisation'] * 2 +
        df['appareil_different'] * 1.5 +
        (df['hour'] < 6).astype(int) * 1.5 +
        (df['hour'] >= 23).astype(int) * 1
    )
    df['fraud_label'] = df['fraud_type'].map(FRAUD_TYPE_LABELS).fillna(df['fraud_type'])
    return df

@st.cache_resource
def train_model(df):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
    from imblearn.over_sampling import SMOTE

    cat_cols = ['transaction_type', 'city', 'operator', 'period_of_day']
    df_enc = pd.get_dummies(df, columns=cat_cols)

    exclude = ['transaction_id', 'date', 'user_id', 'is_fraud', 'fraud_type', 'fraud_label', 'month_name']
    feature_cols = [c for c in df_enc.columns if c not in exclude]

    X = df_enc[feature_cols].fillna(0)
    y = df_enc['is_fraud']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    scaler = StandardScaler()
    num_cols = ['amount', 'nb_transactions_24h', 'amount_log', 'activity_ratio', 'risk_score', 'hour', 'day', 'day_of_week', 'month']
    num_cols = [c for c in num_cols if c in X_train.columns]
    X_train_s = X_train.copy()
    X_test_s  = X_test.copy()
    X_train_s[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test_s[num_cols]  = scaler.transform(X_test[num_cols])

    smote = SMOTE(random_state=42)
    X_bal, y_bal = smote.fit_resample(X_train_s, y_train)

    rf = RandomForestClassifier(n_estimators=100, max_depth=15, min_samples_split=10,
                                min_samples_leaf=5, random_state=42, n_jobs=-1)
    rf.fit(X_bal, y_bal)

    y_pred      = rf.predict(X_test_s)
    y_pred_prob = rf.predict_proba(X_test_s)[:, 1]

    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
    metrics = {
        'accuracy':  accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall':    recall_score(y_test, y_pred),
        'f1':        f1_score(y_test, y_pred),
        'auc':       roc_auc_score(y_test, y_pred_prob),
        'cm':        confusion_matrix(y_test, y_pred),
        'y_test':    y_test,
        'y_pred_prob': y_pred_prob,
    }

    importances = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)

    return rf, scaler, feature_cols, num_cols, metrics, importances

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1.5rem 0;">
        <div style="font-size:1.6rem; font-weight:800; color:#00e5ff; letter-spacing:-0.02em;">FraudShield</div>
        <div style="font-size:0.7rem; color:#6b7a99; letter-spacing:0.15em; text-transform:uppercase; font-family:'JetBrains Mono',monospace;">Détection IA · Mobile Money</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Navigation</div>', unsafe_allow_html=True)
    page = st.radio("", ["Vue d'ensemble", "Analyse exploratoire", "Modèle IA", "Simulateur", "Bénéfices & Impact"],
                    label_visibility="collapsed")

    st.markdown('<div class="section-title" style="margin-top:2rem;">Filtres globaux</div>', unsafe_allow_html=True)

    df_raw = load_data()

    selected_ops    = st.multiselect("Opérateur", df_raw['operator'].unique(), default=list(df_raw['operator'].unique()))
    selected_cities = st.multiselect("Ville",     df_raw['city'].unique(),     default=list(df_raw['city'].unique()))
    amount_range    = st.slider("Montant (FCFA)", int(df_raw['amount'].min()),
                                int(df_raw['amount'].max()),
                                (int(df_raw['amount'].min()), int(df_raw['amount'].max())))

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:0.7rem; color:#6b7a99; font-family:'JetBrains Mono',monospace; line-height:1.8;">
    Dataset · 100 000 transactions<br>
    Période · Juil–Déc 2024<br>
    Contexte · Sénégal / UEMOA<br>
    Modèle · Random Forest
    </div>
    """, unsafe_allow_html=True)

# ─── Données filtrées ────────────────────────────────────────────────────────
@st.cache_data
def filter_data(ops, cities, amt_min, amt_max):
    df = load_data()
    mask = (df['operator'].isin(ops) &
            df['city'].isin(cities) &
            df['amount'].between(amt_min, amt_max))
    return df[mask]

df = filter_data(tuple(selected_ops), tuple(selected_cities), amount_range[0], amount_range[1])

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — VUE D'ENSEMBLE
# ═══════════════════════════════════════════════════════════════════════════════
if page == "Vue d'ensemble":
    st.markdown('<h1 style="color:#00e5ff; margin-bottom:0.2rem;">Vue d\'ensemble</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6b7a99; margin-bottom:2rem; font-family:\'JetBrains Mono\',monospace; font-size:0.8rem;">Tableau de bord · Transactions Mobile Money · Sénégal</p>', unsafe_allow_html=True)

    total     = len(df)
    frauds    = df['is_fraud'].sum()
    fraud_rate= frauds / total * 100 if total > 0 else 0
    vol_total = df['amount'].sum()
    vol_fraud = df[df['is_fraud']==1]['amount'].sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card accent">
            <div class="metric-label">Transactions</div>
            <div class="metric-value cyan">{total:,}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card danger">
            <div class="metric-label">Fraudes détectées</div>
            <div class="metric-value red">{frauds:,}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card warn">
            <div class="metric-label">Taux de fraude</div>
            <div class="metric-value yellow">{fraud_rate:.2f}%</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card ok">
            <div class="metric-label">Volume frauduleux</div>
            <div class="metric-value green">{vol_fraud/1e6:.1f}M FCFA</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="section-title">Évolution des fraudes dans le temps</div>', unsafe_allow_html=True)
        daily = df.groupby(['date', 'is_fraud']).size().reset_index(name='count')
        daily_fraud = daily[daily['is_fraud']==1].set_index('date')['count'].resample('W').sum().reset_index()
        daily_total = daily.groupby('date')['count'].sum().resample('W').sum().reset_index()
        daily_total.columns = ['date', 'total']
        merged = daily_fraud.merge(daily_total, on='date', how='left')
        merged['taux'] = merged['count'] / merged['total'] * 100

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=merged['date'], y=merged['count'], name='Fraudes',
                             marker_color=COLOR_FRAUD, opacity=0.8), secondary_y=False)
        fig.add_trace(go.Scatter(x=merged['date'], y=merged['taux'], name='Taux (%)',
                                 line=dict(color=COLOR_ACCENT, width=2), mode='lines+markers',
                                 marker=dict(size=5)), secondary_y=True)
        fig.update_layout(**PLOTLY_LAYOUT, height=280, showlegend=True,
                          legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
        fig.update_yaxes(title_text="Fraudes / semaine", secondary_y=False, gridcolor='#1e2a42')
        fig.update_yaxes(title_text="Taux (%)", secondary_y=True, gridcolor='#1e2a42')
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-title">Types de fraudes</div>', unsafe_allow_html=True)
        fraud_types = df[df['is_fraud']==1]['fraud_label'].value_counts()
        colors = [COLOR_FRAUD, '#ff6b81', '#ff9f43', COLOR_WARN, COLOR_ACCENT, '#7bed9f', COLOR_OK]
        fig2 = go.Figure(go.Pie(
            labels=fraud_types.index, values=fraud_types.values, hole=0.55,
            marker=dict(colors=colors[:len(fraud_types)], line=dict(color='#0a0d14', width=2)),
            textfont=dict(family='JetBrains Mono', size=11),
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, height=280, showlegend=True,
                           legend=dict(orientation='v', font=dict(size=10), bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig2, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-title">Fraudes par opérateur</div>', unsafe_allow_html=True)
        op_stats = df.groupby('operator').agg(total=('is_fraud','count'), fraudes=('is_fraud','sum')).reset_index()
        op_stats['taux'] = op_stats['fraudes'] / op_stats['total'] * 100
        op_stats = op_stats.sort_values('taux', ascending=True)
        fig3 = go.Figure(go.Bar(
            y=op_stats['operator'], x=op_stats['taux'], orientation='h',
            marker=dict(color=op_stats['taux'], colorscale=[[0, COLOR_OK],[0.5, COLOR_WARN],[1, COLOR_FRAUD]],
                        line=dict(color='rgba(0,0,0,0)')),
            text=[f"{t:.1f}%" for t in op_stats['taux']], textposition='outside',
            textfont=dict(family='JetBrains Mono', size=11)
        ))
        fig3.update_layout(**PLOTLY_LAYOUT, height=220)
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">Fraudes par ville</div>', unsafe_allow_html=True)
        city_stats = df.groupby('city').agg(total=('is_fraud','count'), fraudes=('is_fraud','sum')).reset_index()
        city_stats['taux'] = city_stats['fraudes'] / city_stats['total'] * 100
        city_stats = city_stats.sort_values('taux', ascending=True)
        fig4 = go.Figure(go.Bar(
            y=city_stats['city'], x=city_stats['taux'], orientation='h',
            marker=dict(color=city_stats['taux'], colorscale=[[0, COLOR_OK],[0.5, COLOR_WARN],[1, COLOR_FRAUD]],
                        line=dict(color='rgba(0,0,0,0)')),
            text=[f"{t:.1f}%" for t in city_stats['taux']], textposition='outside',
            textfont=dict(family='JetBrains Mono', size=11)
        ))
        fig4.update_layout(**PLOTLY_LAYOUT, height=220)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-title">Dernières transactions suspectes</div>', unsafe_allow_html=True)
    suspect = df[df['is_fraud']==1].sort_values('date', ascending=False).head(10)[
        ['transaction_id','date','hour','amount','transaction_type','city','operator','fraud_label','risk_score']
    ].copy()
    suspect['amount']     = suspect['amount'].apply(lambda x: f"{x:,.0f} FCFA")
    suspect['risk_score'] = suspect['risk_score'].apply(lambda x: f"{x:.1f}")
    st.dataframe(suspect.rename(columns={
        'transaction_id':'ID','date':'Date','hour':'Heure','amount':'Montant',
        'transaction_type':'Type','city':'Ville','operator':'Opérateur',
        'fraud_label':'Type de fraude','risk_score':'Score risque'
    }), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — ANALYSE EXPLORATOIRE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Analyse exploratoire":
    st.markdown('<h1 style="color:#00e5ff; margin-bottom:0.2rem;">Analyse exploratoire</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6b7a99; margin-bottom:2rem; font-family:\'JetBrains Mono\',monospace; font-size:0.8rem;">Patterns · Distributions · Corrélations</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Temporel", "Montants", "Comportement", "Corrélations"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">Fraudes par heure de la journée</div>', unsafe_allow_html=True)
            hourly = df.groupby(['hour','is_fraud']).size().reset_index(name='count')
            h_fraud  = hourly[hourly['is_fraud']==1]
            h_normal = hourly[hourly['is_fraud']==0]
            fig = go.Figure()
            fig.add_trace(go.Bar(x=h_normal['hour'], y=h_normal['count'], name='Normal',
                                 marker_color=COLOR_OK, opacity=0.5))
            fig.add_trace(go.Bar(x=h_fraud['hour'], y=h_fraud['count'], name='Fraude',
                                 marker_color=COLOR_FRAUD))
            fig.update_layout(**PLOTLY_LAYOUT, barmode='overlay', height=300,
                              legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
            fig.update_xaxes(dtick=1, title='Heure')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-title">Fraudes par jour de la semaine</div>', unsafe_allow_html=True)
            days = ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim']
            dow = df.groupby(['day_of_week','is_fraud']).size().reset_index(name='count')
            d_fraud = dow[dow['is_fraud']==1].set_index('day_of_week')['count']
            d_total = dow.groupby('day_of_week')['count'].sum()
            taux_dow = (d_fraud / d_total * 100).reindex(range(7)).fillna(0)
            fig2 = go.Figure(go.Bar(
                x=days, y=taux_dow.values,
                marker=dict(color=[COLOR_FRAUD if v > taux_dow.mean() else COLOR_OK for v in taux_dow.values]),
                text=[f"{v:.1f}%" for v in taux_dow.values], textposition='outside',
                textfont=dict(family='JetBrains Mono', size=11)
            ))
            fig2.update_layout(**PLOTLY_LAYOUT, height=300)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="section-title">Fraudes par période de la journée</div>', unsafe_allow_html=True)
        period_order = ['Nuit (0-6h)', 'Matin (6-12h)', 'Après-midi (12-18h)', 'Soir (18-24h)']
        period_stats = df.groupby('period_of_day').agg(
            total=('is_fraud','count'), fraudes=('is_fraud','sum')).reindex(period_order).reset_index()
        period_stats['taux']    = period_stats['fraudes'] / period_stats['total'] * 100
        period_stats['normaux'] = period_stats['total'] - period_stats['fraudes']
        fig3 = make_subplots(rows=1, cols=2, subplot_titles=('Volume de transactions', 'Taux de fraude (%)'))
        fig3.add_trace(go.Bar(x=period_stats['period_of_day'], y=period_stats['normaux'],
                              name='Normal', marker_color=COLOR_OK, opacity=0.7), row=1, col=1)
        fig3.add_trace(go.Bar(x=period_stats['period_of_day'], y=period_stats['fraudes'],
                              name='Fraude', marker_color=COLOR_FRAUD), row=1, col=1)
        fig3.add_trace(go.Bar(x=period_stats['period_of_day'], y=period_stats['taux'],
                              name='Taux', marker_color=COLOR_WARN,
                              text=[f"{t:.1f}%" for t in period_stats['taux']], textposition='outside'), row=1, col=2)
        fig3.update_layout(**PLOTLY_LAYOUT, height=320, barmode='stack',
                           legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">Distribution des montants</div>', unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=df[df['is_fraud']==0]['amount_log'], name='Normal',
                                       marker_color=COLOR_OK, opacity=0.6, nbinsx=50))
            fig.add_trace(go.Histogram(x=df[df['is_fraud']==1]['amount_log'], name='Fraude',
                                       marker_color=COLOR_FRAUD, opacity=0.8, nbinsx=50))
            fig.update_layout(**PLOTLY_LAYOUT, barmode='overlay', height=300, xaxis_title='log(Montant)',
                              legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-title">Montant moyen par type de transaction</div>', unsafe_allow_html=True)
            type_amt = df.groupby(['transaction_type','is_fraud'])['amount'].mean().reset_index()
            fig2 = px.bar(type_amt, x='transaction_type', y='amount', color='is_fraud', barmode='group',
                          color_discrete_map={0: COLOR_OK, 1: COLOR_FRAUD},
                          labels={'amount':'Montant moyen (FCFA)','transaction_type':'Type','is_fraud':'Fraude'})
            fig2.update_layout(**PLOTLY_LAYOUT, height=300,
                               legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="section-title">Statistiques des montants</div>', unsafe_allow_html=True)
        stats = df.groupby('is_fraud')['amount'].describe().round(0)
        stats.index = ['Normal', 'Fraude']
        st.dataframe(stats.style.format("{:,.0f}"), use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">Changement de localisation</div>', unsafe_allow_html=True)
            loc = df.groupby(['changement_localisation','is_fraud']).size().reset_index(name='count')
            loc['label'] = loc['changement_localisation'].map({0:'Même localisation', 1:'Changement rapide'})
            fig = px.bar(loc, x='label', y='count', color='is_fraud', barmode='group',
                         color_discrete_map={0: COLOR_OK, 1: COLOR_FRAUD},
                         labels={'count':'Transactions','label':'Localisation','is_fraud':'Fraude'})
            fig.update_layout(**PLOTLY_LAYOUT, height=280,
                              legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-title">Appareil différent</div>', unsafe_allow_html=True)
            app = df.groupby(['appareil_different','is_fraud']).size().reset_index(name='count')
            app['label'] = app['appareil_different'].map({0:'Même appareil', 1:'Appareil différent'})
            fig2 = px.bar(app, x='label', y='count', color='is_fraud', barmode='group',
                          color_discrete_map={0: COLOR_OK, 1: COLOR_FRAUD},
                          labels={'count':'Transactions','label':'Appareil','is_fraud':'Fraude'})
            fig2.update_layout(**PLOTLY_LAYOUT, height=280,
                               legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="section-title">Score de risque vs Fraude</div>', unsafe_allow_html=True)
        risk_fraud = df.groupby(['risk_score','is_fraud']).size().reset_index(name='count')
        rf_fraud   = risk_fraud[risk_fraud['is_fraud']==1]
        rf_total   = risk_fraud.groupby('risk_score')['count'].sum().reset_index()
        merged_risk = rf_total.merge(rf_fraud[['risk_score','count']], on='risk_score', how='left', suffixes=('_total','_fraud'))
        merged_risk['taux'] = merged_risk['count_fraud'] / merged_risk['count_total'] * 100
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=merged_risk['risk_score'], y=merged_risk['count_total'],
                              name='Total', marker_color=COLOR_OK, opacity=0.5))
        fig3.add_trace(go.Scatter(x=merged_risk['risk_score'], y=merged_risk['taux'],
                                  name='Taux fraude (%)', mode='lines+markers',
                                  line=dict(color=COLOR_FRAUD, width=2), yaxis='y2'))
        fig3.update_layout(**PLOTLY_LAYOUT, height=320,
                           yaxis2=dict(overlaying='y', side='right', gridcolor='#1e2a42', title='Taux de fraude (%)'),
                           legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
        fig3.update_xaxes(title='Score de risque')
        st.plotly_chart(fig3, use_container_width=True)

    with tab4:
        st.markdown('<div class="section-title">Matrice de corrélation</div>', unsafe_allow_html=True)
        num_cols_corr = ['amount','hour','nb_transactions_24h','changement_localisation',
                         'appareil_different','is_fraud','risk_score','activity_ratio','amount_log']
        corr = df[num_cols_corr].corr()
        fig = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.columns,
            colorscale=[[0, COLOR_FRAUD],[0.5, '#111520'],[1, COLOR_ACCENT]], zmid=0,
            text=corr.round(2).values, texttemplate='%{text}',
            textfont=dict(size=10, family='JetBrains Mono'), hoverongaps=False
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=450)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="section-title">Top corrélations avec is_fraud</div>', unsafe_allow_html=True)
        top_corr = corr['is_fraud'].drop('is_fraud').sort_values(key=abs, ascending=False)
        fig2 = go.Figure(go.Bar(
            x=top_corr.values, y=top_corr.index, orientation='h',
            marker=dict(color=[COLOR_FRAUD if v > 0 else COLOR_OK for v in top_corr.values]),
            text=[f"{v:.3f}" for v in top_corr.values], textposition='outside',
            textfont=dict(family='JetBrains Mono', size=11)
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, height=300)
        st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — MODÈLE IA
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Modèle IA":
    st.markdown('<h1 style="color:#00e5ff; margin-bottom:0.2rem;">Modèle IA</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6b7a99; margin-bottom:2rem; font-family:\'JetBrains Mono\',monospace; font-size:0.8rem;">Random Forest · Entraînement & Évaluation</p>', unsafe_allow_html=True)

    with st.spinner("Entraînement du modèle Random Forest en cours..."):
        df_full = load_data()
        rf_model, scaler_obj, feat_cols, num_c, metrics, importances = train_model(df_full)

    m1, m2, m3, m4, m5 = st.columns(5)
    cards = [
        (m1, "Accuracy",  f"{metrics['accuracy']*100:.1f}%",  "accent", "cyan"),
        (m2, "Precision", f"{metrics['precision']*100:.1f}%", "ok",     "green"),
        (m3, "Recall",    f"{metrics['recall']*100:.1f}%",    "warn",   "yellow"),
        (m4, "F1-Score",  f"{metrics['f1']:.3f}",             "danger", "red"),
        (m5, "AUC-ROC",   f"{metrics['auc']:.3f}",            "accent", "cyan"),
    ]
    for col, label, value, card_cls, val_cls in cards:
        with col:
            st.markdown(f"""<div class="metric-card {card_cls}">
                <div class="metric-label">{label}</div>
                <div class="metric-value {val_cls}">{value}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Matrice de confusion</div>', unsafe_allow_html=True)
        cm = metrics['cm']
        labels = [['TN\nNormaux corrects','FP\nFausses alertes'],['FN\nFraudes manquées','TP\nFraudes détectées']]
        fig = go.Figure(go.Heatmap(
            z=cm, x=['Prédit Normal','Prédit Fraude'], y=['Réel Normal','Réel Fraude'],
            colorscale=[[0,'#111520'],[1, COLOR_ACCENT]],
            text=[[f"{cm[i][j]:,}" for j in range(2)] for i in range(2)],
            texttemplate='%{text}',
            textfont=dict(size=16, family='JetBrains Mono, monospace', color='#e8edf5'),
            showscale=False
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=320)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Courbe ROC</div>', unsafe_allow_html=True)
        from sklearn.metrics import roc_curve
        fpr_arr, tpr_arr, _ = roc_curve(metrics['y_test'], metrics['y_pred_prob'])
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=[0,1], y=[0,1], mode='lines',
                                  line=dict(color=COLOR_FRAUD, dash='dash', width=1),
                                  name='Aléatoire', showlegend=True))
        fig2.add_trace(go.Scatter(x=fpr_arr, y=tpr_arr, mode='lines',
                                  line=dict(color=COLOR_ACCENT, width=2.5),
                                  fill='tozeroy', fillcolor='rgba(0,229,255,0.08)',
                                  name=f"Random Forest (AUC={metrics['auc']:.3f})"))
        fig2.update_layout(**PLOTLY_LAYOUT, height=320,
                           xaxis_title='Taux de Faux Positifs',
                           yaxis_title='Taux de Vrais Positifs',
                           legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-title">Importance des variables (Top 15)</div>', unsafe_allow_html=True)
    top15 = importances.head(15).sort_values(ascending=True)
    fig3 = go.Figure(go.Bar(
        x=top15.values, y=top15.index, orientation='h',
        marker=dict(color=top15.values, colorscale=[[0, COLOR_OK],[0.5, COLOR_WARN],[1, COLOR_ACCENT]]),
        text=[f"{v:.3f}" for v in top15.values], textposition='outside',
        textfont=dict(family='JetBrains Mono', size=11)
    ))
    fig3.update_layout(**PLOTLY_LAYOUT, height=400)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-title">Distribution des probabilités de fraude</div>', unsafe_allow_html=True)
    fig4 = go.Figure()
    y_test_arr = metrics['y_test'].values
    prob_arr   = metrics['y_pred_prob']
    fig4.add_trace(go.Histogram(x=prob_arr[y_test_arr==0], name='Normal',
                                marker_color=COLOR_OK, opacity=0.7, nbinsx=50))
    fig4.add_trace(go.Histogram(x=prob_arr[y_test_arr==1], name='Fraude',
                                marker_color=COLOR_FRAUD, opacity=0.8, nbinsx=50))
    fig4.add_vline(x=0.5, line_dash='dash', line_color=COLOR_WARN, line_width=2,
                   annotation_text='Seuil 0.5', annotation_font_color=COLOR_WARN)
    fig4.update_layout(**PLOTLY_LAYOUT, barmode='overlay', height=300,
                       xaxis_title='Probabilité de fraude',
                       legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
    st.plotly_chart(fig4, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — SIMULATEUR
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Simulateur":
    st.markdown('<h1 style="color:#00e5ff; margin-bottom:0.2rem;">Simulateur de transaction</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6b7a99; margin-bottom:2rem; font-family:\'JetBrains Mono\',monospace; font-size:0.8rem;">Testez une transaction et obtenez un score de risque en temps réel</p>', unsafe_allow_html=True)

    with st.spinner("Chargement du modèle..."):
        df_full = load_data()
        rf_model, scaler_obj, feat_cols, num_c, metrics, importances = train_model(df_full)

    col_form, col_result = st.columns([1, 1])

    with col_form:
        st.markdown('<div class="section-title">Paramètres de la transaction</div>', unsafe_allow_html=True)
        amount           = st.number_input("Montant (FCFA)", min_value=500, max_value=700000, value=25000, step=500)
        hour             = st.slider("Heure de la transaction", 0, 23, 14)
        transaction_type = st.selectbox("Type de transaction", ['transfer','payment','withdrawal','deposit'])
        city             = st.selectbox("Ville", ['Dakar','Thiès','Kaolack','Saint-Louis','Ziguinchor','Touba'])
        operator         = st.selectbox("Opérateur", ['Wave','Orange Money','Free Money','Wizall'])
        nb_trans_24h     = st.slider("Transactions dans les 24 dernières heures", 0, 20, 1)
        changement_loc   = st.toggle("Changement rapide de localisation", value=False)
        appareil_diff    = st.toggle("Appareil différent utilisé", value=False)
        predict_btn      = st.button("Analyser la transaction")

    with col_result:
        if predict_btn:
            def period(h):
                if h < 6:    return 'Nuit (0-6h)'
                elif h < 12: return 'Matin (6-12h)'
                elif h < 18: return 'Après-midi (12-18h)'
                else:         return 'Soir (18-24h)'

            amount_log     = np.log1p(amount)
            activity_ratio = nb_trans_24h / df_full['nb_transactions_24h'].mean()
            risk_score     = (int(changement_loc)*2 + int(appareil_diff)*1.5 +
                              (1.5 if hour < 6 else 0) + (1 if hour >= 23 else 0))
            period_val = period(hour)

            row = {
                'amount': amount, 'hour': hour, 'nb_transactions_24h': nb_trans_24h,
                'changement_localisation': int(changement_loc), 'appareil_different': int(appareil_diff),
                'day_of_week': 2, 'is_weekend': 0, 'month': 10, 'day': 15,
                'amount_log': amount_log, 'activity_ratio': activity_ratio, 'risk_score': risk_score,
            }
            for tt in ['transfer','payment','withdrawal','deposit']:
                row[f'transaction_type_{tt}'] = 1 if transaction_type == tt else 0
            for c in ['Dakar','Thiès','Kaolack','Saint-Louis','Ziguinchor','Touba']:
                row[f'city_{c}'] = 1 if city == c else 0
            for op in ['Wave','Orange Money','Free Money','Wizall']:
                row[f'operator_{op}'] = 1 if operator == op else 0
            for p in ['Nuit (0-6h)','Matin (6-12h)','Après-midi (12-18h)','Soir (18-24h)']:
                row[f'period_of_day_{p}'] = 1 if period_val == p else 0

            X_sim   = pd.DataFrame([row]).reindex(columns=feat_cols, fill_value=0)
            X_sim_s = X_sim.copy()
            num_present = [c for c in num_c if c in X_sim_s.columns]
            X_sim_s[num_present] = scaler_obj.transform(X_sim_s[num_present].values.reshape(1,-1))[0].reshape(1,-1)

            prob = rf_model.predict_proba(X_sim_s)[0][1]
            pred = int(prob >= 0.5)

            if pred == 1:
                st.markdown(f"""<div class="predict-result-fraud">
                    <div style="font-size:3rem;">⚠️</div>
                    <div style="font-size:1.4rem; font-weight:800; color:#ff4757; margin:0.5rem 0;">TRANSACTION SUSPECTE</div>
                    <div style="font-family:'JetBrains Mono',monospace; color:#6b7a99; margin-bottom:1rem;">Probabilité de fraude</div>
                    <div style="font-size:3.5rem; font-weight:800; color:#ff4757; font-family:'JetBrains Mono',monospace;">{prob*100:.1f}%</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="predict-result-ok">
                    <div style="font-size:3rem;">✅</div>
                    <div style="font-size:1.4rem; font-weight:800; color:#2ed573; margin:0.5rem 0;">TRANSACTION NORMALE</div>
                    <div style="font-family:'JetBrains Mono',monospace; color:#6b7a99; margin-bottom:1rem;">Probabilité de fraude</div>
                    <div style="font-size:3.5rem; font-weight:800; color:#2ed573; font-family:'JetBrains Mono',monospace;">{prob*100:.1f}%</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=prob*100,
                number={'suffix': '%', 'font': {'family': 'JetBrains Mono', 'size': 30, 'color': '#e8edf5'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#6b7a99', 'tickfont': {'family': 'JetBrains Mono', 'size': 10}},
                    'bar': {'color': COLOR_FRAUD if pred==1 else COLOR_OK, 'thickness': 0.25},
                    'bgcolor': '#111520',
                    'steps': [
                        {'range': [0, 30],  'color': 'rgba(46,213,115,0.15)'},
                        {'range': [30, 60], 'color': 'rgba(255,211,42,0.12)'},
                        {'range': [60, 100],'color': 'rgba(255,71,87,0.12)'},
                    ],
                    'threshold': {'line': {'color': COLOR_WARN, 'width': 3}, 'value': 50}
                }
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e8edf5'),
                              height=230, margin=dict(l=30, r=30, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('<div class="section-title">Facteurs de risque détectés</div>', unsafe_allow_html=True)
            factors = []
            if changement_loc:    factors.append(("Changement de localisation rapide", "élevé", COLOR_FRAUD))
            if appareil_diff:     factors.append(("Appareil différent utilisé", "moyen", COLOR_WARN))
            if hour < 6:          factors.append(("Transaction de nuit (0-6h)", "élevé", COLOR_FRAUD))
            if nb_trans_24h > 5:  factors.append((f"{nb_trans_24h} transactions en 24h", "moyen", COLOR_WARN))
            if amount > 200000:   factors.append(("Montant très élevé", "moyen", COLOR_WARN))

            if factors:
                for label, level, color in factors:
                    st.markdown(f"""<div style="display:flex; justify-content:space-between; align-items:center;
                        background:#111520; border:1px solid #1e2a42; border-radius:8px;
                        padding:0.6rem 1rem; margin-bottom:0.4rem;">
                        <span style="font-family:'JetBrains Mono',monospace; font-size:0.82rem;">{label}</span>
                        <span style="color:{color}; font-family:'JetBrains Mono',monospace;
                              font-size:0.72rem; font-weight:700; text-transform:uppercase;">{level}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="background:#111520; border:1px solid #1e2a42;
                    border-radius:8px; padding:0.8rem 1rem; color:#6b7a99;
                    font-family:'JetBrains Mono',monospace; font-size:0.82rem;">
                    Aucun facteur de risque majeur détecté
                </div>""", unsafe_allow_html=True)

        else:
            st.markdown("""<div class="predict-box" style="margin-top:2rem;">
                <div style="font-size:3rem; margin-bottom:1rem;">🛡</div>
                <div style="color:#6b7a99; font-family:'JetBrains Mono',monospace; font-size:0.85rem;">
                    Configurez les paramètres de la transaction<br>et cliquez sur <strong style="color:#00e5ff;">Analyser</strong>
                </div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — BÉNÉFICES & IMPACT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Bénéfices & Impact":

    st.markdown('<h1 style="color:#00e5ff; margin-bottom:0.2rem;">Bénéfices & Impact</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6b7a99; margin-bottom:2rem; font-family:\'JetBrains Mono\',monospace; font-size:0.8rem;">Valeur business · Contexte Sénégal · Cas d\'usage Free Money</p>', unsafe_allow_html=True)

    tab_gen, tab_free, tab_roi = st.tabs([
        "Bénéfices généraux",
        "Cas Free Money · Sénégal",
        "Estimation ROI"
    ])

    # ══════════════════════════════════════════════════════
    # TAB 1 — BÉNÉFICES GÉNÉRAUX
    # ══════════════════════════════════════════════════════
    with tab_gen:

        # Contexte marché
        st.markdown('<div class="section-title">Contexte · Mobile Money au Sénégal</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#111520; border:1px solid #1e2a42; border-radius:12px; padding:1.2rem 1.6rem; margin-bottom:1.5rem; line-height:1.8; font-size:0.88rem; color:#c5cde0;">
        Le Sénégal est devenu en 2024 le <strong style="color:#00e5ff;">leader du mobile money dans l'UEMOA</strong> avec 24,1% du volume
        des transactions de la zone. Le taux d'utilisation des services financiers numériques a bondi de 40,9% en 2012 à
        <strong style="color:#00e5ff;">93,5% en 2022</strong>, mais cette croissance s'est accompagnée d'une explosion des tentatives de fraude :
        les plaintes reçues par la Division de lutte contre la cybercriminalité sont passées de <strong style="color:#ff4757;">212 à 5 600 entre 2017 et 2024</strong>.
        <strong style="color:#ffd32a;">43% des utilisateurs</strong> ont fait face à au moins une tentative de fraude dans les 12 derniers mois,
        et seuls <strong>10% des opérateurs</strong> utilisent des technologies avancées (IA/ML) pour les combattre.
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        stats_marche = [
            (c1, "93,5%",  "Taux d'adoption des SFN au Sénégal (2022)", COLOR_ACCENT),
            (c2, "43%",    "Utilisateurs exposés à une tentative de fraude", COLOR_FRAUD),
            (c3, "+2 540%","Hausse des plaintes cybercriminalité (2017–2024)", COLOR_WARN),
            (c4, "10%",    "Opérateurs utilisant l'IA anti-fraude", COLOR_OK),
        ]
        for col, val, lbl, color in stats_marche:
            with col:
                st.markdown(f"""<div class="stat-highlight">
                    <div class="val" style="color:{color};">{val}</div>
                    <div class="lbl">{lbl}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Les 6 bénéfices clés
        st.markdown('<div class="section-title">Les 6 bénéfices clés d\'un système de détection automatisée</div>', unsafe_allow_html=True)

        benefits = [
            ("Réduction des pertes financières",
             "Un opérateur de mobile money perd en moyenne 1,06 million USD par an à cause de la fraude. Un système IA capable de détecter 90%+ des fraudes avant exécution réduit directement ces pertes et protège les marges dans un marché où la guerre des prix est déjà intense.",
             "−70% de pertes"),
            ("Détection en temps réel",
             "Contrairement aux contrôles manuels post-transaction, le modèle analyse chaque transaction en quelques millisecondes. Les fraudes par SIM Swap, phishing ou fermes SIM — souvent exécutées en rafale — sont bloquées avant tout dommage.",
             "< 50 ms / transaction"),
            ("Confiance et fidélisation client",
             "32% des utilisateurs sénégalais ont déjà perdu de l'argent suite à une fraude ou arnaque. Un opérateur qui garantit la sécurité des fonds se différencie fortement et réduit le churn. La confiance est le 1er facteur de rétention dans le mobile money.",
             "+25% de rétention"),
            ("Réduction des faux positifs",
             "Un blocage injustifié d'une transaction légitime frustre l'utilisateur et nuit à l'image. Le modèle Random Forest, avec sa précision élevée, minimise ces erreurs coûteuses tout en maintenant un recall fort sur les vraies fraudes.",
             "Précision > 90%"),
            ("Conformité réglementaire BCEAO",
             "La BCEAO et l'UEMOA exigent des dispositifs de lutte contre le blanchiment et la fraude. Ce système génère des logs détaillés, des scores de risque par transaction et des alertes auditables, facilitant la conformité et les rapports réglementaires.",
             "Conformité BCEAO"),
            ("Scalabilité et automatisation",
             "Le traitement manuel de 100 000 transactions par jour est impossible. L'IA analyse l'intégralité du flux sans surcoût marginal, libérant les équipes fraude pour les cas complexes et les investigations à haute valeur ajoutée.",
             "100K tx/jour"),
        ]

        icons = ["💰", "⚡", "🤝", "🎯", "📋", "📈"]
        colors_b = [COLOR_FRAUD, COLOR_ACCENT, COLOR_OK, COLOR_WARN, "#ab47bc", COLOR_OK]

        for i in range(0, 6, 2):
            col_a, col_b = st.columns(2)
            for col, idx in [(col_a, i), (col_b, i+1)]:
                if idx < len(benefits):
                    title, desc, stat = benefits[idx]
                    with col:
                        st.markdown(f"""
                        <div class="benefit-card" style="margin-bottom:1rem;">
                            <div class="benefit-icon">{icons[idx]}</div>
                            <div class="benefit-title">{title}</div>
                            <div class="benefit-desc">{desc}</div>
                            <div class="benefit-stat" style="color:{colors_b[idx]};">{stat}</div>
                        </div>
                        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Comparaison manuel vs IA
        st.markdown('<div class="section-title">Comparaison · Contrôle manuel vs Détection IA</div>', unsafe_allow_html=True)
        compare_data = {
            "Critère":            ["Vitesse de détection", "Couverture des transactions", "Taux de détection fraude",
                                   "Faux positifs", "Coût par transaction analysée", "Disponibilité", "Scalabilité"],
            "Contrôle manuel":    ["Heures / jours", "< 5% (échantillon)", "~30–50%", "Élevé (subjectif)",
                                   "Très élevé", "Heures ouvrables", "Limitée"],
            "Détection IA (FraudShield)": ["< 50 ms", "100%", "> 90%", "Faible (optimisé)",
                                            "Quasi nul", "24h/24 7j/7", "Illimitée"],
        }
        df_compare = pd.DataFrame(compare_data)
        st.dataframe(df_compare, use_container_width=True, hide_index=True)

        # Graphique types de fraudes et leur dangerosité
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Dangerosité des types de fraude mobile money au Sénégal</div>', unsafe_allow_html=True)

        fraud_danger = pd.DataFrame({
            "Type de fraude":   ["SIM Swap", "Fermes SIM", "Agent Complice", "Phishing", "Bypass Cash-In", "Intrusion Compte"],
            "Fréquence (%)":    [22, 18, 15, 28, 10, 7],
            "Montant moyen (K FCFA)": [185, 95, 230, 45, 120, 160],
            "Difficulté détection": [8, 9, 7, 5, 6, 8],
        })
        fig = px.scatter(fraud_danger,
                         x="Fréquence (%)", y="Montant moyen (K FCFA)",
                         size="Difficulté détection", color="Type de fraude",
                         color_discrete_sequence=[COLOR_FRAUD,'#ff6b81','#ff9f43',COLOR_WARN,COLOR_ACCENT,'#ab47bc'],
                         hover_name="Type de fraude", size_max=50,
                         labels={"Fréquence (%)":"Fréquence relative (%)","Montant moyen (K FCFA)":"Montant moyen (FCFA × 1000)"})
        fig.update_layout(**PLOTLY_LAYOUT, height=380,
                          xaxis=dict(gridcolor='#1e2a42'), yaxis=dict(gridcolor='#1e2a42'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""<div style="font-size:0.75rem; color:#6b7a99; font-family:'JetBrains Mono',monospace; margin-top:-0.5rem;">
        La taille des bulles représente la difficulté de détection (1=facile, 10=très difficile). Source : données simulées inspirées du contexte UEMOA / CGAP 2022-2024.
        </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # TAB 2 — CAS FREE MONEY
    # ══════════════════════════════════════════════════════
    with tab_free:

        # En-tête Free
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0a0d14,#0d1a2e); border:1px solid #00e5ff22;
             border-radius:14px; padding:1.5rem 2rem; margin-bottom:1.5rem; position:relative; overflow:hidden;">
            <div style="position:absolute; top:0; left:0; right:0; height:3px;
                 background:linear-gradient(90deg,#ff4757,#ffd32a,#00e5ff);"></div>
            <div style="font-size:1.4rem; font-weight:800; color:#00e5ff; margin-bottom:0.4rem;">
                Free Money · Mixx by Yas
            </div>
            <div style="font-size:0.82rem; color:#6b7a99; line-height:1.7;">
                Anciennement Free Sénégal · Filiale d'Axian Telecom · Lancé en octobre 2019<br>
                Challenger du marché face à Wave (~60% de parts) et Orange Money (~28%)<br>
                Positionnement : <strong style="color:#ffd32a;">gratuité totale des services</strong> (transferts, retraits, paiements)
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Positionnement marché
        st.markdown('<div class="section-title">Positionnement de Free Money sur le marché sénégalais</div>', unsafe_allow_html=True)

        col_pie, col_context = st.columns([1, 1])
        with col_pie:
            market_data = pd.DataFrame({
                "Opérateur": ["Wave", "Orange Money", "Free Money (Mixx by Yas)", "Autres (Wizall, etc.)"],
                "Part de marché (%)": [58, 28, 8, 6],
            })
            fig = go.Figure(go.Pie(
                labels=market_data["Opérateur"],
                values=market_data["Part de marché (%)"],
                hole=0.5,
                marker=dict(colors=[COLOR_ACCENT, COLOR_WARN, COLOR_FRAUD, '#6b7a99'],
                            line=dict(color='#0a0d14', width=2)),
                textfont=dict(family='JetBrains Mono', size=11),
            ))
            fig.update_layout(**PLOTLY_LAYOUT, height=300, showlegend=True,
                              legend=dict(orientation='v', font=dict(size=10), bgcolor='rgba(0,0,0,0)'),
                              annotations=[dict(text='Marché<br>Sénégal', x=0.5, y=0.5,
                                               font=dict(size=11, color='#6b7a99'), showarrow=False)])
            st.plotly_chart(fig, use_container_width=True)

        with col_context:
            st.markdown("""
            <div style="padding-top:0.5rem;">
            <div class="timeline-item">
                <div class="timeline-dot" style="background:#ffd32a;"></div>
                <div class="timeline-content">
                    <div class="timeline-title">Octobre 2019 — Lancement Free Money</div>
                    <div class="timeline-desc">Passage de Tigo à Free Sénégal. Lancement du service mobile money face à Orange Money (4,2M comptes actifs à l'époque).</div>
                </div>
            </div>
            <div class="timeline-item">
                <div class="timeline-dot" style="background:#00e5ff;"></div>
                <div class="timeline-content">
                    <div class="timeline-title">2020 — Migration vers Comviva</div>
                    <div class="timeline-desc">Adoption de la plateforme mobiquity® Money pour scaler face à la demande Covid-19 et accélérer la croissance des transactions.</div>
                </div>
            </div>
            <div class="timeline-item">
                <div class="timeline-dot" style="background:#2ed573;"></div>
                <div class="timeline-content">
                    <div class="timeline-title">2024 — Offre "Tout à 0 FCFA"</div>
                    <div class="timeline-desc">Tous les services (transferts, retraits, paiements marchands) deviennent gratuits. Stratégie agressive pour gagner des parts sur Wave.</div>
                </div>
            </div>
            <div class="timeline-item">
                <div class="timeline-dot" style="background:#ab47bc;"></div>
                <div class="timeline-content">
                    <div class="timeline-title">2025 — Rebrand Mixx by Yas</div>
                    <div class="timeline-desc">Free Sénégal devient Yas Sénégal, filiale d'Axian Telecom. Le service Free Money devient Mixx by Yas avec de nouvelles ambitions.</div>
                </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Pourquoi Free Money a particulièrement besoin de FraudShield
        st.markdown('<div class="section-title">Pourquoi Free Money a particulièrement besoin d\'un système anti-fraude IA</div>', unsafe_allow_html=True)

        challenges = [
            ("Stratégie 0 FCFA = risque amplifié",
             "En rendant tous les services gratuits, Free Money devient une cible attractive pour les fraudeurs. L'absence de frais de transaction élimine un frein naturel à la fraude en volume (fermes SIM, transactions répétitives). Un système de détection IA est la barrière indispensable.",
             COLOR_FRAUD),
            ("Déficit de notoriété à combler",
             "Avec ~8% de parts de marché face à Wave (58%) et Orange Money (28%), la confiance des utilisateurs est le levier de croissance n°1. Un seul incident de fraude médiatisé peut freiner l'acquisition. FraudShield protège la réputation autant que les fonds.",
             COLOR_WARN),
            ("Croissance rapide = surface d'attaque croissante",
             "Une base d'utilisateurs en croissance accélérée signifie davantage de nouveaux comptes, souvent sans historique de transactions. Ces profils 'froids' sont les plus vulnérables au SIM Swap et à l'usurpation d'identité. Le modèle IA apprend leurs patterns comportementaux.",
             COLOR_ACCENT),
            ("Marges compressées par la gratuité",
             "Sans revenus de commissions, Free Money doit absolument minimiser les pertes liées à la fraude. Chaque FCFA frauduleux est une perte nette. À l'échelle de millions de transactions, même un taux de fraude de 1% représente des dizaines de millions de FCFA de pertes annuelles.",
             COLOR_OK),
        ]

        for i in range(0, 4, 2):
            col_a, col_b = st.columns(2)
            for col, idx in [(col_a, i), (col_b, i+1)]:
                if idx < len(challenges):
                    title, desc, color = challenges[idx]
                    with col:
                        st.markdown(f"""
                        <div style="background:#111520; border:1px solid {color}33; border-left:3px solid {color};
                             border-radius:10px; padding:1.2rem; margin-bottom:1rem; min-height:160px;">
                            <div style="font-size:0.9rem; font-weight:700; color:{color}; margin-bottom:0.5rem;">{title}</div>
                            <div style="font-size:0.8rem; color:#8891b2; line-height:1.65;">{desc}</div>
                        </div>
                        """, unsafe_allow_html=True)

        # Scénario concret
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Scénario concret · Attaque par fermes SIM sur Free Money</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#111520; border:1px solid #1e2a42; border-radius:12px; padding:1.4rem; font-size:0.84rem; color:#c5cde0; line-height:1.8;">
        <strong style="color:#ff4757;">Scénario :</strong> Un réseau de fraudeurs crée 200 comptes Free Money avec de faux numéros SIM. Grâce à la gratuité des transferts,
        ils effectuent 50 transactions de 15 000 FCFA chacun en moins de 2 heures vers des comptes complices, soit <strong style="color:#ff4757;">150 millions de FCFA</strong> déplacés.<br><br>
        <strong style="color:#00e5ff;">Sans FraudShield :</strong> L'activité anormale est détectée manuellement après plusieurs heures. Les fonds sont irrécupérables.<br><br>
        <strong style="color:#2ed573;">Avec FraudShield :</strong> Dès la 3ème transaction, le score de risque (activité_ratio élevé, même device, heure nocturne)
        dépasse le seuil. Les comptes sont flagués et les transactions suspendues automatiquement. <strong style="color:#2ed573;">Perte évitée : 147M FCFA.</strong>
        </div>
        """, unsafe_allow_html=True)

        # Recommandations stratégiques
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Recommandations stratégiques pour Free Money / Mixx by Yas</div>', unsafe_allow_html=True)

        recs = [
            ("Intégration API temps réel", "Connecter FraudShield directement au moteur de traitement des transactions pour un blocage avant validation, pas après."),
            ("Règles métier personnalisées", "Paramétrer des seuils spécifiques au contexte Free Money : plafonds de transactions gratuites, ratio d'activité par compte, géolocalisation des agents."),
            ("Dashboard fraude dédié", "Donner à l'équipe Risk de Free Money accès à ce dashboard pour monitorer en continu les patterns et ajuster le modèle."),
            ("Boucle de rétroaction continue", "Alimenter le modèle avec les retours des équipes fraude (cas confirmés, faux positifs) pour améliorer la précision au fil du temps."),
            ("Communication client", "Valoriser le système de protection dans la communication marketing : 'Vos fonds sont protégés par une IA de détection de fraude en temps réel'."),
        ]
        for i, (title, desc) in enumerate(recs):
            st.markdown(f"""
            <div style="display:flex; gap:1rem; margin-bottom:0.8rem; align-items:flex-start;
                 background:#111520; border:1px solid #1e2a42; border-radius:8px; padding:0.9rem 1.1rem;">
                <div style="min-width:24px; height:24px; border-radius:50%; background:#00e5ff22;
                     border:1px solid #00e5ff44; display:flex; align-items:center; justify-content:center;
                     font-size:0.75rem; font-weight:800; color:#00e5ff; font-family:'JetBrains Mono',monospace;">{i+1}</div>
                <div>
                    <div style="font-size:0.88rem; font-weight:700; color:#e8edf5; margin-bottom:0.2rem;">{title}</div>
                    <div style="font-size:0.78rem; color:#6b7a99; line-height:1.6;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # TAB 3 — ESTIMATION ROI
    # ══════════════════════════════════════════════════════
    with tab_roi:
        st.markdown('<div class="section-title">Simulateur d\'impact financier</div>', unsafe_allow_html=True)
        st.markdown("""<div style="background:#111520; border:1px solid #1e2a42; border-radius:10px;
            padding:1rem 1.2rem; margin-bottom:1.5rem; font-size:0.82rem; color:#6b7a99; line-height:1.7;">
            Ajustez les paramètres ci-dessous pour estimer l'impact financier d'un système de détection automatisée
            adapté à votre opérateur. Les valeurs par défaut sont calées sur le profil Free Money / Mixx by Yas.
        </div>""", unsafe_allow_html=True)

        col_params, col_results = st.columns([1, 1])

        with col_params:
            nb_tx_jour    = st.number_input("Transactions par jour", min_value=1000, max_value=5000000,
                                             value=50000, step=5000)
            montant_moyen = st.number_input("Montant moyen par transaction (FCFA)",
                                             min_value=1000, max_value=500000, value=15000, step=1000)
            taux_fraude   = st.slider("Taux de fraude estimé (%)", 0.1, 10.0, 2.0, 0.1)
            taux_detection= st.slider("Taux de détection du modèle IA (%)", 50, 99, 90)
            taux_fp       = st.slider("Taux de faux positifs (%)", 0.1, 10.0, 2.0, 0.1)
            cout_fp       = st.number_input("Coût d'un faux positif (FCFA, service client)",
                                             min_value=0, max_value=50000, value=2000, step=500)
            cout_solution = st.number_input("Coût annuel de la solution IA (FCFA)",
                                             min_value=0, max_value=500000000, value=15000000, step=1000000)

        with col_results:
            # Calculs
            tx_an          = nb_tx_jour * 365
            vol_an         = tx_an * montant_moyen
            fraudes_an     = tx_an * taux_fraude / 100
            montant_fraude = fraudes_an * montant_moyen
            fraudes_detectees   = fraudes_an * taux_detection / 100
            fraudes_manquees    = fraudes_an - fraudes_detectees
            perte_residuelle    = fraudes_manquees * montant_moyen
            economies           = montant_fraude - perte_residuelle
            faux_pos_an         = tx_an * taux_fp / 100
            cout_faux_pos_total = faux_pos_an * cout_fp
            roi_net             = economies - cout_faux_pos_total - cout_solution
            roi_pct             = (roi_net / cout_solution * 100) if cout_solution > 0 else 0

            st.markdown(f"""
            <div style="background:#111520; border:1px solid #1e2a42; border-radius:12px; padding:1.4rem; margin-bottom:1rem;">
                <div style="font-size:0.7rem; letter-spacing:0.15em; text-transform:uppercase; color:#6b7a99;
                     font-family:'JetBrains Mono',monospace; margin-bottom:1.2rem; border-bottom:1px solid #1e2a42; padding-bottom:0.6rem;">
                    Résultats de la simulation
                </div>

                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.8rem; margin-bottom:1rem;">
                    <div class="stat-highlight">
                        <div class="val" style="color:#00e5ff; font-size:1.3rem;">{vol_an/1e9:.1f} Md</div>
                        <div class="lbl">Volume annuel (FCFA)</div>
                    </div>
                    <div class="stat-highlight">
                        <div class="val" style="color:#ff4757; font-size:1.3rem;">{montant_fraude/1e6:.1f}M</div>
                        <div class="lbl">Fraude totale estimée (FCFA)</div>
                    </div>
                    <div class="stat-highlight">
                        <div class="val" style="color:#2ed573; font-size:1.3rem;">{economies/1e6:.1f}M</div>
                        <div class="lbl">Économies brutes (FCFA)</div>
                    </div>
                    <div class="stat-highlight">
                        <div class="val" style="color:#ffd32a; font-size:1.3rem;">{cout_faux_pos_total/1e6:.1f}M</div>
                        <div class="lbl">Coût faux positifs (FCFA)</div>
                    </div>
                </div>

                <div style="background:{'rgba(46,213,115,0.08)' if roi_net > 0 else 'rgba(255,71,87,0.08)'};
                     border:2px solid {'#2ed573' if roi_net > 0 else '#ff4757'};
                     border-radius:10px; padding:1.2rem; text-align:center;">
                    <div style="font-size:0.72rem; color:#6b7a99; font-family:'JetBrains Mono',monospace;
                         text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.3rem;">ROI Net annuel</div>
                    <div style="font-size:2.2rem; font-weight:800; font-family:'JetBrains Mono',monospace;
                         color:{'#2ed573' if roi_net > 0 else '#ff4757'};">
                        {roi_net/1e6:.1f}M FCFA
                    </div>
                    <div style="font-size:1rem; color:{'#2ed573' if roi_net > 0 else '#ff4757'};
                         font-family:'JetBrains Mono',monospace; margin-top:0.3rem;">
                        {'+' if roi_pct > 0 else ''}{roi_pct:.0f}% de retour sur investissement
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Graphique waterfall ROI
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Décomposition du ROI</div>', unsafe_allow_html=True)

        waterfall_x = ["Fraude totale\névitée", "Coût faux\npositifs", "Coût solution\nIA", "ROI Net"]
        waterfall_y = [economies/1e6, -cout_faux_pos_total/1e6, -cout_solution/1e6, roi_net/1e6]
        colors_wf   = [COLOR_OK, COLOR_WARN, COLOR_FRAUD, COLOR_ACCENT if roi_net > 0 else COLOR_FRAUD]

        fig = go.Figure(go.Bar(
            x=waterfall_x, y=waterfall_y,
            marker_color=colors_wf,
            text=[f"{v:+.1f}M FCFA" for v in waterfall_y],
            textposition='outside',
            textfont=dict(family='JetBrains Mono', size=12, color='#e8edf5')
        ))
        fig.add_hline(y=0, line_color='#1e2a42', line_width=1)
        fig.update_layout(**PLOTLY_LAYOUT, height=360,
                          yaxis_title="Millions FCFA",
                          xaxis=dict(gridcolor='rgba(0,0,0,0)'),
                          yaxis=dict(gridcolor='#1e2a42'))
        st.plotly_chart(fig, use_container_width=True)

        # Source note
        st.markdown("""
        <div style="font-size:0.72rem; color:#6b7a99; font-family:'JetBrains Mono',monospace; margin-top:1rem; line-height:1.8;
             background:#111520; border:1px solid #1e2a42; border-radius:8px; padding:0.8rem 1rem;">
        <strong style="color:#e8edf5;">Sources :</strong> CGAP — Enquête nationale sur les risques SFN au Sénégal (2022) ·
        BCEAO — Rapport annuel SFN UEMOA 2024 · GSMA — State of the Industry Report Mobile Money 2025 ·
        Le360 Afrique — Pertes mobile money en Afrique (2024) · Ciberobs — Cybercriminalité mobile money Sénégal (2024) ·
        HUB2 — Senegal payment market analysis (2025)
        </div>
        """, unsafe_allow_html=True)
