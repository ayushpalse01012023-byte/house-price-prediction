import streamlit as st
import joblib
import pandas as pd

st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    background: #f1f5f9 !important;
    color: #1e293b !important;
}
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1300px !important; }

/* Top banner */
.top-banner {
    background: linear-gradient(120deg, #1e3a5f 0%, #2563eb 100%);
    border-radius: 14px;
    padding: 1.6rem 2rem;
    margin-bottom: 2rem;
    display: flex; align-items: center; gap: 1rem;
}
.top-banner h1 { font-size: 1.65rem; font-weight: 700; color: #fff; margin: 0 0 0.2rem; }
.top-banner p  { font-size: 0.85rem; color: #bfdbfe; margin: 0; }

/* Section card */
.sec-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.4rem 1.6rem 0.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.sec-title {
    font-size: 0.73rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #f1f5f9;
}

/* Number inputs */
[data-testid="stNumberInput"] input {
    border-radius: 8px !important;
    border: 1.5px solid #e2e8f0 !important;
    background: #f8fafc !important;
    font-size: 0.93rem !important;
    color: #1e293b !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
    background: #fff !important;
}
label[data-testid="stWidgetLabel"] p {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #475569 !important;
}

/* Predict button */
.stButton > button {
    background: linear-gradient(135deg, #1e3a5f, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.8rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.3) !important;
}
.stButton > button:hover { opacity: 0.92 !important; }

/* Result */
.result-box {
    background: linear-gradient(135deg, #1e3a5f 0%, #1d4ed8 100%);
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 8px 28px rgba(37,99,235,0.25);
}
.result-box .rl  { font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase; color: #93c5fd; margin-bottom: 0.5rem; }
.result-box .rp  { font-size: 3rem; font-weight: 700; color: #fff; line-height: 1; margin-bottom: 0.4rem; }
.result-box .rr  { font-size: 0.82rem; color: #93c5fd; }

/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model        = joblib.load("house_price_prediction.pkl")
    model_columns = joblib.load("model_columns.pkl")
    return model, model_columns

try:
    model, model_columns = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    load_error   = str(e)

# ── Banner ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-banner">
  <span style="font-size:2rem;">🏠</span>
  <div>
    <h1>House Price Predictor</h1>
    <p>Enter values for every feature below, then click Predict</p>
  </div>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.error(f"Could not load model files: {load_error}\n\n"
             "Place `house_price_prediction.pkl` and `model_columns.pkl` next to this script.")
    st.stop()

# ── Human-friendly labels for known columns ────────────────────────────────────
LABELS = {
    "GrLivArea":     "Above-Ground Living Area (sq ft)",
    "LotArea":       "Lot Area (sq ft)",
    "TotalBsmtSF":   "Total Basement SF",
    "1stFlrSF":      "1st Floor SF",
    "2ndFlrSF":      "2nd Floor SF",
    "GarageArea":    "Garage Area (sq ft)",
    "OverallQual":   "Overall Quality (1-10)",
    "OverallCond":   "Overall Condition (1-10)",
    "YearBuilt":     "Year Built",
    "YearRemodAdd":  "Year Remodelled",
    "BedroomAbvGr":  "Bedrooms Above Ground",
    "FullBath":      "Full Bathrooms",
    "HalfBath":      "Half Bathrooms",
    "TotRmsAbvGrd":  "Total Rooms Above Ground",
    "Fireplaces":    "Fireplaces",
    "GarageCars":    "Garage Cars",
    "LotFrontage":   "Lot Frontage (ft)",
    "MasVnrArea":    "Masonry Veneer Area (sq ft)",
    "BsmtFinSF1":    "Basement Finished SF 1",
    "BsmtFinSF2":    "Basement Finished SF 2",
    "BsmtUnfSF":     "Basement Unfinished SF",
    "WoodDeckSF":    "Wood Deck SF",
    "OpenPorchSF":   "Open Porch SF",
    "EnclosedPorch": "Enclosed Porch SF",
    "ScreenPorch":   "Screen Porch SF",
    "PoolArea":      "Pool Area (sq ft)",
    "MiscVal":       "Miscellaneous Value ($)",
    "BsmtFullBath":  "Basement Full Baths",
    "BsmtHalfBath":  "Basement Half Baths",
    "KitchenAbvGr":  "Kitchens Above Ground",
    "MoSold":        "Month Sold (1-12)",
    "YrSold":        "Year Sold",
    "MSSubClass":    "MS SubClass",
    "3SsnPorch":     "3-Season Porch SF",
}

DEFAULTS = {
    "GrLivArea": 1500, "LotArea": 8000, "TotalBsmtSF": 800,
    "1stFlrSF": 1000,  "2ndFlrSF": 0,   "GarageArea": 400,
    "OverallQual": 6,  "OverallCond": 5, "YearBuilt": 1990,
    "YearRemodAdd": 2000, "BedroomAbvGr": 3, "FullBath": 2,
    "HalfBath": 1, "TotRmsAbvGrd": 7, "Fireplaces": 1,
    "GarageCars": 2, "LotFrontage": 70, "MoSold": 6, "YrSold": 2023,
    "KitchenAbvGr": 1, "MSSubClass": 60,
}

# ── Group model columns into sections ─────────────────────────────────────────
SIZE_COLS   = ["GrLivArea","LotArea","TotalBsmtSF","1stFlrSF","2ndFlrSF",
               "GarageArea","LotFrontage","MasVnrArea","BsmtFinSF1",
               "BsmtFinSF2","BsmtUnfSF","WoodDeckSF","OpenPorchSF",
               "EnclosedPorch","ScreenPorch","PoolArea","3SsnPorch"]
QUAL_COLS   = ["OverallQual","OverallCond","YearBuilt","YearRemodAdd"]
ROOM_COLS   = ["BedroomAbvGr","FullBath","HalfBath","TotRmsAbvGrd",
               "KitchenAbvGr","Fireplaces","GarageCars","BsmtFullBath","BsmtHalfBath"]
SALE_COLS   = ["MSSubClass","MoSold","YrSold","MiscVal"]

# everything else goes to "Other Features"
accounted   = set(SIZE_COLS + QUAL_COLS + ROOM_COLS + SALE_COLS)
OTHER_COLS  = [c for c in model_columns if c not in accounted]

def render_section(title, cols_in_model, ncols=4):
    """Render a section card with number_input for every column."""
    cols_present = [c for c in cols_in_model if c in model_columns]
    if not cols_present:
        return {}
    vals = {}
    st.markdown(f'<div class="sec-card"><div class="sec-title">{title}</div>', unsafe_allow_html=True)
    grid = st.columns(ncols)
    for i, col in enumerate(cols_present):
        label   = LABELS.get(col, col.replace("_", " "))
        default = float(DEFAULTS.get(col, 0))
        vals[col] = grid[i % ncols].number_input(
            label, value=default, step=1.0, format="%.0f", key=f"inp_{col}"
        )
    st.markdown('</div>', unsafe_allow_html=True)
    return vals

# ── Render all sections ────────────────────────────────────────────────────────
input_values = {}
input_values.update(render_section("📐  Size & Areas",       SIZE_COLS,  4))
input_values.update(render_section("⭐  Quality & Age",      QUAL_COLS,  4))
input_values.update(render_section("🛏️  Rooms & Amenities", ROOM_COLS,  4))
input_values.update(render_section("📅  Sale Info",          SALE_COLS,  4))
if OTHER_COLS:
    input_values.update(render_section("🏷️  Other Features (0 = No, 1 = Yes)", OTHER_COLS, 4))

# ── Predict ────────────────────────────────────────────────────────────────────
def build_df():
    row = {col: 0.0 for col in model_columns}
    for col, val in input_values.items():
        if col in row:
            row[col] = float(val)
    return pd.DataFrame([row])[model_columns]

def fmt(v):
    if v >= 1e6: return f"${v/1e6:.2f}M"
    if v >= 1e3: return f"${v/1e3:.0f}K"
    return f"${v:,.0f}"

st.markdown("<br>", unsafe_allow_html=True)
col_btn, col_res = st.columns([1, 2], gap="large")

with col_btn:
    clicked = st.button("⚡  Predict House Price")
    st.markdown(f"""
    <div style="margin-top:1rem;background:#fff;border:1px solid #e2e8f0;
         border-radius:12px;padding:1rem 1.25rem;">
      <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;
           text-transform:uppercase;color:#64748b;margin-bottom:0.6rem;">Model Info</div>
      <div style="font-size:0.85rem;color:#475569;margin-bottom:0.3rem;">
        🤖 <b>{type(model).__name__}</b></div>
      <div style="font-size:0.85rem;color:#475569;">
        📊 <b>{len(model_columns)}</b> input features</div>
    </div>
    """, unsafe_allow_html=True)

with col_res:
    if clicked:
        try:
            pred = float(model.predict(build_df())[0])
            st.markdown(f"""
            <div class="result-box">
              <div class="rl">Estimated Market Value</div>
              <div class="rp">{fmt(pred)}</div>
              <div class="rr">Range &nbsp;·&nbsp; {fmt(pred*0.92)} — {fmt(pred*1.08)}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Prediction error: {e}")
    else:
        st.markdown("""
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
             padding:2.5rem;text-align:center;">
          <div style="font-size:2.5rem;margin-bottom:0.75rem;">🏠</div>
          <div style="font-size:1rem;font-weight:600;color:#1e293b;margin-bottom:0.35rem;">
            Ready to Estimate</div>
          <div style="font-size:0.85rem;color:#94a3b8;">
            Fill in the fields above and click<br><b>Predict House Price</b></div>
        </div>
        """, unsafe_allow_html=True)
