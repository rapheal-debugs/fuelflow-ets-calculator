"""
================================================================================
  FUELFLOW — COMPLIANCE SUITE
  CII Calculator + EU ETS Liability Calculator

  Regulatory Basis:
    CII  → MEPC.337(76), MEPC.338(76), MEPC.339(76)
    ETS  → EU MRV Regulation 2015/757 | EU ETS Directive 2003/87/EC
    Fuel → IMO MEPC.1/Circ.795/Rev.6 | EU MRV Annex I

  Developed by: FuelFlow | Transition Holdings
================================================================================
"""

import math
import streamlit as st

st.set_page_config(
    page_title="FuelFlow | Compliance Suite",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── App background ── */
.stApp { background-color: #FFFFFF; color: #1a1a2e; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #F8F9FA;
    border-right: 1px solid #E2E8F0;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stRadio label {
    color: #64748b !important;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── Logo / Header ── */
.ff-logo {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.15rem;
    font-weight: 700;
    color: #1a1a2e;
    letter-spacing: 0.04em;
    padding: 0.5rem 0 1.5rem 0;
    border-bottom: 1px solid #E2E8F0;
    margin-bottom: 1.5rem;
}
.ff-logo span { color: #94a3b8; font-weight: 400; }

/* ── Page title ── */
.ff-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #1a1a2e;
    letter-spacing: -0.02em;
    margin-bottom: 0.2rem;
}
.ff-subtitle {
    font-size: 0.85rem;
    color: #64748b;
    margin-bottom: 2rem;
    font-weight: 400;
}

/* ── Section headers ── */
.ff-section {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #FF4B4B;
    margin: 1.8rem 0 0.8rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #E2E8F0;
}

/* ── Metric cards ── */
.metric-card {
    background: #F8F9FA;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.8rem;
}
.metric-card .label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 0.3rem;
}
.metric-card .value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.55rem;
    font-weight: 600;
    color: #1a1a2e;
    line-height: 1.1;
}
.metric-card .unit {
    font-size: 0.78rem;
    color: #94a3b8;
    margin-top: 0.2rem;
    font-family: 'Inter', sans-serif;
}

/* ── Rating badge ── */
.rating-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 3.5rem;
    font-weight: 700;
    width: 90px;
    height: 90px;
    line-height: 90px;
    text-align: center;
    border-radius: 12px;
    margin-bottom: 0.5rem;
}
.rating-A { background: #dcfce7; color: #16a34a; border: 2px solid #86efac; }
.rating-B { background: #f0fdf4; color: #22c55e; border: 2px solid #bbf7d0; }
.rating-C { background: #fefce8; color: #ca8a04; border: 2px solid #fde68a; }
.rating-D { background: #fff7ed; color: #ea580c; border: 2px solid #fdba74; }
.rating-E { background: #fef2f2; color: #dc2626; border: 2px solid #fca5a5; }

/* ── Rating boundary bar ── */
.boundary-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.45rem;
    font-size: 0.82rem;
}
.boundary-letter {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 0.85rem;
    width: 20px;
    text-align: center;
}
.boundary-range {
    font-family: 'JetBrains Mono', monospace;
    color: #64748b;
    font-size: 0.78rem;
    flex: 1;
}
.boundary-active {
    background: #fff1f1;
    border-radius: 4px;
    padding: 0.15rem 0.5rem;
    color: #FF4B4B !important;
    font-weight: 600;
}
.boundary-dot { width: 7px; height: 7px; border-radius: 50%; background: #E2E8F0; }
.boundary-dot-active { background: #FF4B4B; }

/* ── Info / warning / zero boxes ── */
.info-box {
    background: #F8F9FA;
    border-left: 3px solid #94a3b8;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    font-size: 0.82rem;
    color: #64748b;
    margin: 0.8rem 0;
    line-height: 1.6;
}
.warn-box {
    background: #fffbeb;
    border-left: 3px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    font-size: 0.82rem;
    color: #92400e;
    margin: 0.8rem 0;
    line-height: 1.6;
}
.zero-box {
    background: #f0fdf4;
    border-left: 3px solid #22c55e;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    font-size: 0.82rem;
    color: #166534;
    margin: 0.8rem 0;
    line-height: 1.6;
}

/* ── ETS liability card ── */
.ets-card {
    background: linear-gradient(135deg, #fff1f1 0%, #fef2f2 100%);
    border: 1px solid #fecaca;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
}
.ets-card .ets-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.6rem;
}
.ets-card .ets-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    color: #FF4B4B;
    line-height: 1.1;
}
.ets-card .ets-sub {
    font-size: 0.78rem;
    color: #94a3b8;
    margin-top: 0.4rem;
}

/* ── Divider ── */
.ff-divider { border: none; border-top: 1px solid #E2E8F0; margin: 1.5rem 0; }

/* ── Streamlit overrides ── */
.stNumberInput input, .stSelectbox select, div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border-color: #E2E8F0 !important;
    color: #1a1a2e !important;
}
div[data-baseweb="select"] * { color: #1a1a2e !important; }
.stTabs [data-baseweb="tab-list"] {
    background-color: #F8F9FA;
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #94a3b8;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background-color: #FFFFFF !important;
    color: #FF4B4B !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem; }

/* ── Primary button ── */
.stButton > button[kind="primary"] {
    background-color: #FF4B4B !important;
    color: white !important;
    border: none !important;
}
.stButton > button[kind="primary"]:hover {
    background-color: #cc0000 !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────

reference_params = {
    "Bulk_carrier":               {"a": 4745,      "c": 0.622,  "capacity": "DWT"},
    "Gas_carrier_large":          {"a": 14405E7,   "c": 2.071,  "capacity": "DWT"},
    "Gas_carrier_small":          {"a": 8104,      "c": 0.639,  "capacity": "DWT"},
    "Tanker":                     {"a": 5247,      "c": 0.610,  "capacity": "DWT"},
    "Container_ship":             {"a": 1984,      "c": 0.489,  "capacity": "DWT"},
    "General_cargo_large":        {"a": 31948,     "c": 0.792,  "capacity": "DWT"},
    "General_cargo_small":        {"a": 588,       "c": 0.3885, "capacity": "DWT"},
    "Refrigerated_cargo_carrier": {"a": 4600,      "c": 0.557,  "capacity": "DWT"},
    "Combination_carrier":        {"a": 40853,     "c": 0.812,  "capacity": "DWT"},
    "LNG_carrier_large":          {"a": 9.827,     "c": 0.000,  "capacity": "DWT"},
    "LNG_carrier_medium":         {"a": 14479E10,  "c": 2.673,  "capacity": "DWT"},
    "LNG_carrier_small":          {"a": 14479E10,  "c": 2.673,  "capacity": "DWT"},
    "Ro_ro_vehicle_carrier":      {"a": 5739,      "c": 0.631,  "capacity": "GT"},
    "Ro_ro_cargo_ship":           {"a": 10952,     "c": 0.637,  "capacity": "DWT"},
    "Ro_ro_passenger_ship":       {"a": 7540,      "c": 0.587,  "capacity": "GT"},
    "Cruise_passenger_ship":      {"a": 930,       "c": 0.383,  "capacity": "GT"},
}

boundary_vectors = {
    "Bulk_carrier":               {"d1": 0.86, "d2": 0.94, "d3": 1.06, "d4": 1.18},
    "Gas_carrier_large":          {"d1": 0.81, "d2": 0.91, "d3": 1.12, "d4": 1.44},
    "Gas_carrier_small":          {"d1": 0.85, "d2": 0.95, "d3": 1.06, "d4": 1.25},
    "Tanker":                     {"d1": 0.82, "d2": 0.93, "d3": 1.08, "d4": 1.28},
    "Container_ship":             {"d1": 0.83, "d2": 0.94, "d3": 1.07, "d4": 1.19},
    "General_cargo_large":        {"d1": 0.83, "d2": 0.94, "d3": 1.06, "d4": 1.19},
    "General_cargo_small":        {"d1": 0.83, "d2": 0.94, "d3": 1.06, "d4": 1.19},
    "Refrigerated_cargo_carrier": {"d1": 0.78, "d2": 0.91, "d3": 1.07, "d4": 1.20},
    "Combination_carrier":        {"d1": 0.87, "d2": 0.96, "d3": 1.06, "d4": 1.14},
    "LNG_carrier_large":          {"d1": 0.89, "d2": 0.98, "d3": 1.06, "d4": 1.13},
    "LNG_carrier_medium":         {"d1": 0.78, "d2": 0.92, "d3": 1.10, "d4": 1.37},
    "LNG_carrier_small":          {"d1": 0.78, "d2": 0.92, "d3": 1.10, "d4": 1.37},
    "Ro_ro_vehicle_carrier":      {"d1": 0.86, "d2": 0.94, "d3": 1.06, "d4": 1.16},
    "Ro_ro_cargo_ship":           {"d1": 0.66, "d2": 0.89, "d3": 1.08, "d4": 1.27},
    "Ro_ro_passenger_ship":       {"d1": 0.72, "d2": 0.90, "d3": 1.12, "d4": 1.41},
    "Cruise_passenger_ship":      {"d1": 0.87, "d2": 0.95, "d3": 1.06, "d4": 1.16},
}

reduction_factors = {2023: 0.05, 2024: 0.07, 2025: 0.09, 2026: 0.11}

TBM_ch4 = 0.00005
TBM_n2o = 0.00018

fuel_data = {
    "HFO":               {"label": "Heavy Fuel Oil",              "category": "Fossil", "efco2": 3.114, "efch4": TBM_ch4, "efn2o": TBM_n2o, "cj": 0},
    "LFO":               {"label": "Light Fuel Oil",              "category": "Fossil", "efco2": 3.151, "efch4": TBM_ch4, "efn2o": TBM_n2o, "cj": 0},
    "MGO":               {"label": "Marine Gas Oil",              "category": "Fossil", "efco2": 3.206, "efch4": TBM_ch4, "efn2o": TBM_n2o, "cj": 0},
    "LNG_Otto_medium":   {"label": "LNG (Otto Medium Speed)",     "category": "Fossil", "efco2": 2.750, "efch4": 0,       "efn2o": 0.00011, "cj": 0.031},
    "LNG_Otto_slow":     {"label": "LNG (Otto Slow Speed)",       "category": "Fossil", "efco2": 2.750, "efch4": 0,       "efn2o": 0.00011, "cj": 0.017},
    "LNG_Diesel_slow":   {"label": "LNG (Diesel Slow Speed)",     "category": "Fossil", "efco2": 2.750, "efch4": 0,       "efn2o": 0.00011, "cj": 0.002},
    "LNG_Steam_turbine": {"label": "LNG (Steam Turbine)",         "category": "Fossil", "efco2": 2.750, "efch4": 0,       "efn2o": 0.00011, "cj": 0},
    "LNG_LBSI":          {"label": "LNG (LBSI)",                  "category": "Fossil", "efco2": 2.750, "efch4": 0,       "efn2o": 0.00011, "cj": 0.026},
    "LPG_Butane":        {"label": "LPG Butane",                  "category": "Fossil", "efco2": 3.030, "efch4": TBM_ch4, "efn2o": TBM_n2o, "cj": 0},
    "LPG_Propane":       {"label": "LPG Propane",                 "category": "Fossil", "efco2": 3.000, "efch4": TBM_ch4, "efn2o": TBM_n2o, "cj": 0},
    "Methanol_fossil":   {"label": "Methanol (Fossil)",           "category": "Fossil", "efco2": 1.375, "efch4": TBM_ch4, "efn2o": TBM_n2o, "cj": 0},
    "Ethanol_fossil":    {"label": "Ethanol (Fossil)",            "category": "Fossil", "efco2": 1.913, "efch4": TBM_ch4, "efn2o": TBM_n2o, "cj": 0},
    "H2_fossil":         {"label": "Hydrogen (Fossil/Grey)",      "category": "Fossil", "efco2": 0.000, "efch4": 0,       "efn2o": TBM_n2o, "cj": 0},
    "NH3_fossil":        {"label": "Ammonia (Fossil/Grey)",       "category": "Fossil", "efco2": 0.000, "efch4": 0,       "efn2o": TBM_n2o, "cj": 0},
    "Biodiesel":         {"label": "Biodiesel (FAME)",            "category": "Bio",    "efco2": 2.834, "efch4": TBM_ch4, "efn2o": TBM_n2o, "cj": 0},
    "HVO":               {"label": "Hydrotreated Vegetable Oil",  "category": "Bio",    "efco2": 3.115, "efch4": TBM_ch4, "efn2o": TBM_n2o, "cj": 0},
    "BioLNG_Otto_medium":{"label": "Bio-LNG (Otto Medium Speed)", "category": "Bio",    "efco2": 2.750, "efch4": 0,       "efn2o": 0.00011, "cj": 0.031},
    "BioLNG_Otto_slow":  {"label": "Bio-LNG (Otto Slow Speed)",   "category": "Bio",    "efco2": 2.750, "efch4": 0,       "efn2o": 0.00011, "cj": 0.017},
    "BioLNG_Diesel_slow":{"label": "Bio-LNG (Diesel Slow Speed)", "category": "Bio",    "efco2": 2.750, "efch4": 0,       "efn2o": 0.00011, "cj": 0.002},
    "BioLNG_LBSI":       {"label": "Bio-LNG (LBSI)",             "category": "Bio",    "efco2": 2.750, "efch4": 0,       "efn2o": 0.00011, "cj": 0.026},
    "Bio_methanol":      {"label": "Bio-Methanol",               "category": "Bio",    "efco2": 1.375, "efch4": TBM_ch4, "efn2o": TBM_n2o, "cj": 0},
    "Other_bio":         {"label": "Other Biofuel",              "category": "Bio",    "efco2": 3.115, "efch4": TBM_ch4, "efn2o": TBM_n2o, "cj": 0},
    "e_diesel":          {"label": "e-Diesel (RFNBO)",           "category": "eFuel",  "efco2": 3.206, "efch4": TBM_ch4, "efn2o": TBM_n2o, "cj": 0},
    "e_methanol":        {"label": "e-Methanol (RFNBO)",         "category": "eFuel",  "efco2": 1.375, "efch4": TBM_ch4, "efn2o": TBM_n2o, "cj": 0},
    "eLNG_Otto_medium":  {"label": "e-LNG (Otto Medium Speed)",  "category": "eFuel",  "efco2": 2.750, "efch4": 0,       "efn2o": 0.00011, "cj": 0.031},
    "eLNG_Otto_slow":    {"label": "e-LNG (Otto Slow Speed)",    "category": "eFuel",  "efco2": 2.750, "efch4": 0,       "efn2o": 0.00011, "cj": 0.017},
    "eLNG_Diesel_slow":  {"label": "e-LNG (Diesel Slow Speed)",  "category": "eFuel",  "efco2": 2.750, "efch4": 0,       "efn2o": 0.00011, "cj": 0.026},
    "eLNG_LBSI":         {"label": "e-LNG (LBSI)",              "category": "eFuel",  "efco2": 2.750, "efch4": 0,       "efn2o": 0.00011, "cj": 0.026},
    "e_H2":              {"label": "Green Hydrogen (RFNBO)",     "category": "eFuel",  "efco2": 0.000, "efch4": 0,       "efn2o": 0,       "cj": 0},
    "e_NH3":             {"label": "Green Ammonia (RFNBO)",      "category": "eFuel",  "efco2": 0.000, "efch4": 0,       "efn2o": TBM_n2o, "cj": 0},
}

ZERO_EMISSION_FUELS = {k for k, v in fuel_data.items() if v["efco2"] == 0}

VESSEL_TYPE_OPTIONS = {
    "Bulk Carrier":                 "Bulk_carrier",
    "Gas Carrier":                  "Gas_carrier",
    "Tanker":                       "Tanker",
    "Container Ship":               "Container_ship",
    "General Cargo Ship":           "General_cargo_ship",
    "Refrigerated Cargo Carrier":   "Refrigerated_cargo_carrier",
    "Combination Carrier":          "Combination_carrier",
    "LNG Carrier":                  "LNG_carrier",
    "Ro-Ro Vehicle Carrier":        "Ro_ro_vehicle_carrier",
    "Ro-Ro Cargo Ship":             "Ro_ro_cargo_ship",
    "Ro-Ro Passenger Ship":         "Ro_ro_passenger_ship",
    "Cruise Passenger Ship":        "Cruise_passenger_ship",
}

VOYAGE_OPTIONS = {
    "EU → EU  (100% coverage)":     ("EU_EU",    1.0),
    "Non-EU → EU  (50% coverage)":  ("NonEU_EU", 0.5),
    "EU → Non-EU  (50% coverage)":  ("EU_NonEU", 0.5),
    "Berthed at EU Port  (100%)":   ("Berth_EU", 1.0),
}

ETS_PHASE_IN = {"2024": 0.40, "2025": 0.70, "2026+": 1.00}

RATING_DESCRIPTIONS = {
    "A": "Superior — Significantly below required CII",
    "B": "Minor Superior — Below required CII",
    "C": "Moderate — Within required range",
    "D": "Minor Inferior — Exceeds required CII",
    "E": "Inferior — Significantly exceeds required CII",
}


# ─────────────────────────────────────────────────────────────────────────────
# CALCULATION ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def get_vessel_key(vessel_type, dwt):
    if vessel_type == "LNG_carrier":
        return "LNG_carrier_large" if dwt >= 100_000 else "LNG_carrier_medium"
    elif vessel_type == "Gas_carrier":
        return "Gas_carrier_large" if dwt >= 65_000 else "Gas_carrier_small"
    elif vessel_type == "General_cargo_ship":
        return "General_cargo_large" if dwt >= 20_000 else "General_cargo_small"
    return vessel_type


def calculate_cii(vessel_type, fuel_type, DWT, GT, distance, year, mi):
    vessel_key = get_vessel_key(vessel_type, DWT)
    params     = reference_params[vessel_key]
    vectors    = boundary_vectors[vessel_key]
    fuel       = fuel_data[fuel_type]
    Cf         = fuel["efco2"]

    # ── Capacity isolation ───────────────────────────────
    # Per MEPC.337(76) Section 4.2, BOTH Reference CII and
    # Transport Work use the SAME capacity metric (C):
    #   - DWT for bulk carriers, tankers, container ships, gas
    #     carriers, LNG carriers, general cargo, refrigerated
    #     cargo, combination carriers
    #   - GT for cruise passenger ships, ro-ro cargo ships
    #     (vehicle carriers), and ro-ro passenger ships
    capacity_basis = params["capacity"]
    capacity = GT if capacity_basis == "GT" else DWT

    if vessel_key == "LNG_carrier_small":
        capacity = 65_000

    # Defensive guard: capacity must be > 0 to avoid
    # ZeroDivisionError on the negative exponent (capacity ** -c)
    if capacity <= 0:
        capacity = 1

    is_zero       = fuel_type in ZERO_EMISSION_FUELS
    CO2_tonnes    = mi * Cf
    CO2_grams     = CO2_tonnes * 1_000_000
    transport_work = capacity * distance
    attained = CO2_grams / transport_work if transport_work > 0 else 0.0

    a, c      = params["a"], params["c"]
    reference = a * (capacity ** -c)
    rf        = reduction_factors[year]
    required  = (1 - rf) * reference

    boundaries = {
        "A_B": required * vectors["d1"],
        "B_C": required * vectors["d2"],
        "C_D": required * vectors["d3"],
        "D_E": required * vectors["d4"],
    }

    if attained < boundaries["A_B"]:     rating = "A"
    elif attained < boundaries["B_C"]:   rating = "B"
    elif attained < boundaries["C_D"]:   rating = "C"
    elif attained < boundaries["D_E"]:   rating = "D"
    else:                                rating = "E"

    delta_pct = ((attained - required) / required * 100) if required > 0 else 0

    return {
        "vessel_key": vessel_key, "capacity": capacity,
        "capacity_basis": params["capacity"], "Cf": Cf,
        "CO2_tonnes": CO2_tonnes, "CO2_grams": CO2_grams,
        "transport_work": transport_work,
        "attained": attained, "reference": reference, "required": required,
        "boundaries": boundaries, "rating": rating,
        "delta_pct": delta_pct, "is_zero": is_zero, "rf": rf,
    }


def calculate_ets(fuel_type, mi, voyage_l, phase_in):
    fuel   = fuel_data[fuel_type]
    mi_nc  = mi * fuel["cj"]
    mi_c   = mi - mi_nc

    co2_direct = mi_c * fuel["efco2"]
    ch4_eq     = (mi_c * fuel["efch4"] + mi_nc) * 28
    n2o_eq     = mi_c * fuel["efn2o"] * 265
    co2e_total = co2_direct + ch4_eq + n2o_eq

    return {
        "co2_direct": co2_direct, "ch4_eq": ch4_eq,
        "n2o_eq": n2o_eq, "co2e_total": co2e_total,
        "mi_nc": mi_nc, "eua": co2e_total * voyage_l * phase_in,
    }


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="ff-logo">FuelFlow <span></span></div>', unsafe_allow_html=True)

    st.markdown('<div class="ff-section">Vessel</div>', unsafe_allow_html=True)
    vessel_display = st.selectbox("Vessel Type", list(VESSEL_TYPE_OPTIONS.keys()), index=0)
    vessel_type    = VESSEL_TYPE_OPTIONS[vessel_display]

    needs_gt = vessel_type in ("Ro_ro_vehicle_carrier", "Ro_ro_passenger_ship", "Cruise_passenger_ship")
    DWT = st.number_input("DWT (tonnes)", min_value=1000, max_value=500000, value=75000, step=1000)

    if needs_gt:
        GT = st.number_input("GT (tonnes) — required for this vessel type", min_value=1000, max_value=250000, value=50000, step=1000)
        st.caption("⚠ This vessel type uses GT for Reference CII and Transport Work.")
    else:
        GT = 0

    st.markdown('<div class="ff-section">Fuel</div>', unsafe_allow_html=True)
    categories   = sorted(set(v["category"] for v in fuel_data.values()))
    cat_filter   = st.selectbox("Fuel Category", ["All"] + categories)
    fuel_keys    = [k for k, v in fuel_data.items() if cat_filter == "All" or v["category"] == cat_filter]
    fuel_labels  = {k: fuel_data[k]["label"] for k in fuel_keys}
    fuel_display = st.selectbox("Fuel Type", list(fuel_labels.values()))
    fuel_type    = [k for k, v in fuel_labels.items() if v == fuel_display][0]
    mi           = st.number_input("Fuel Consumed (tonnes)", min_value=1.0, value=5442.0, step=10.0)

    st.markdown('<div class="ff-section">Voyage</div>', unsafe_allow_html=True)
    distance = st.number_input("Total Distance (nm)", min_value=1, value=100000, step=100)

    st.markdown('<div class="ff-section">CII</div>', unsafe_allow_html=True)
    cii_year = st.selectbox("Reporting Year (CII)", [2023, 2024, 2025, 2026], index=3)

    st.markdown('<div class="ff-section">EU ETS</div>', unsafe_allow_html=True)
    voyage_display   = st.selectbox("Voyage Type (ETS Coverage)", list(VOYAGE_OPTIONS.keys()), index=0)
    _, voyage_l      = VOYAGE_OPTIONS[voyage_display]
    ets_year_display = st.selectbox("Reporting Year (ETS)", list(ETS_PHASE_IN.keys()), index=2)
    ets_phase_in     = ETS_PHASE_IN[ets_year_display]
    ets_price        = st.number_input("EU ETS Carbon Price (€/tonne)", min_value=1.0, value=77.15, step=0.5)


# ─────────────────────────────────────────────────────────────────────────────
# CALCULATIONS
# ─────────────────────────────────────────────────────────────────────────────

cii           = calculate_cii(vessel_type, fuel_type, DWT, GT, distance, cii_year, mi)
ets           = calculate_ets(fuel_type, mi, voyage_l, ets_phase_in)
ets_liability = ets["co2e_total"] * ets_price * voyage_l * ets_phase_in


# ─────────────────────────────────────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────────────────────────────────────

st.markdown('<div class="ff-title">FuelFlow Compliance Suite</div>', unsafe_allow_html=True)

_capacity_label = f'{cii["capacity"]:,.0f} {cii["capacity_basis"]}'
st.markdown(
    f'<div class="ff-subtitle">'
    f'{vessel_display} &nbsp;·&nbsp; {_capacity_label} &nbsp;·&nbsp; '
    f'{fuel_data[fuel_type]["label"]} &nbsp;·&nbsp; {distance:,} nm'
    f'</div>',
    unsafe_allow_html=True
)

tab_cii, tab_ets, tab_summary = st.tabs(["  CII Calculator", "  EU ETS Liability", "  Summary"])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — CII
# ════════════════════════════════════════════════════════════════════════════
with tab_cii:
    col_left, col_right = st.columns([1, 1.3], gap="large")

    with col_left:
        st.markdown('<div class="ff-section">CII Rating</div>', unsafe_allow_html=True)

        r = cii["rating"]
        st.markdown(
            f'<div style="text-align:center; padding: 1rem 0;">'
            f'<div class="rating-badge rating-{r}">{r}</div>'
            f'<div style="color:#64748b; font-size:0.85rem; margin-top:0.5rem;">{RATING_DESCRIPTIONS[r]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        if cii["is_zero"]:
            st.markdown(
                '<div class="zero-box">'
                '⬡ <strong>Zero-emission fuel detected</strong><br>'
                'Cf = 0 → Attained CII = 0.000 g CO₂/t·nm<br>'
                'No tank-to-wake CO₂ is produced. This vessel operationally exceeds the A rating band.'
                '</div>', unsafe_allow_html=True
            )
        else:
            direction = "below" if cii["delta_pct"] < 0 else "above"
            colour    = "#16a34a" if cii["delta_pct"] < 0 else "#dc2626"
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="label">vs Required CII</div>'
                f'<div class="value" style="color:{colour};">{abs(cii["delta_pct"]):.2f}%</div>'
                f'<div class="unit">{direction} the required threshold</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown('<div class="ff-section">CII Values</div>', unsafe_allow_html=True)

        for label, val, highlight in [
            ("Attained CII", cii["attained"], True),
            ("Required CII", cii["required"], False),
            ("Reference CII", cii["reference"], False),
        ]:
            colour = "#FF4B4B" if highlight else "#64748b"
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="label">{label}</div>'
                f'<div class="value" style="color:{colour};">{val:.4f}</div>'
                f'<div class="unit">g CO₂ / t·nm</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    with col_right:
        st.markdown('<div class="ff-section">Rating Boundaries</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="info-box">Based on Required CII = <strong>{cii["required"]:.4f}</strong> g CO₂/t·nm &nbsp;|&nbsp; '
            f'Year: {cii_year} &nbsp;|&nbsp; Reduction Z = {cii["rf"]*100:.0f}%</div>',
            unsafe_allow_html=True
        )

        b   = cii["boundaries"]
        att = cii["attained"]
        rating_colours = {"A": "#16a34a", "B": "#22c55e", "C": "#ca8a04", "D": "#ea580c", "E": "#dc2626"}

        for letter, lo, hi, rng in [
            ("A", 0,        b["A_B"], f"< {b['A_B']:.4f}"),
            ("B", b["A_B"], b["B_C"], f"{b['A_B']:.4f} – {b['B_C']:.4f}"),
            ("C", b["B_C"], b["C_D"], f"{b['B_C']:.4f} – {b['C_D']:.4f}"),
            ("D", b["C_D"], b["D_E"], f"{b['C_D']:.4f} – {b['D_E']:.4f}"),
            ("E", b["D_E"], float("inf"), f"> {b['D_E']:.4f}"),
        ]:
            is_here      = lo <= att < hi
            active_class = "boundary-active" if is_here else ""
            dot_class    = "boundary-dot-active" if is_here else "boundary-dot"
            here_tag     = " &nbsp;◄ your vessel" if is_here else ""
            st.markdown(
                f'<div class="boundary-row">'
                f'<span class="boundary-letter" style="color:{rating_colours[letter]};">{letter}</span>'
                f'<span class="boundary-dot {dot_class}"></span>'
                f'<span class="boundary-range {active_class}">{rng}{here_tag}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown('<div class="ff-section">Fuel & Emissions</div>', unsafe_allow_html=True)

        fuel_info   = fuel_data[fuel_type]
        cat_colours = {"Fossil": "#64748b", "Bio": "#16a34a", "eFuel": "#FF4B4B"}
        cat_colour  = cat_colours.get(fuel_info["category"], "#64748b")

        st.markdown(
            f'<div class="metric-card">'
            f'<div class="label">Fuel &nbsp;<span style="color:{cat_colour}; font-size:0.7rem;">[{fuel_info["category"]}]</span></div>'
            f'<div class="value" style="font-size:1rem; color:#1a1a2e;">{fuel_info["label"]}</div>'
            f'<div class="unit">Cf = {fuel_info["efco2"]} tCO₂/tFuel &nbsp;|&nbsp; {mi:,.0f} t consumed</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="label">CO₂ Produced</div>'
            f'<div class="value">{cii["CO2_tonnes"]:,.2f}</div>'
            f'<div class="unit">tonnes CO₂ &nbsp;({cii["CO2_grams"]:,.0f} g)</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="label">Transport Work</div>'
            f'<div class="value">{cii["transport_work"]:,.0f}</div>'
            f'<div class="unit">tonne · nautical miles</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="info-box">'
            '<strong>Regulatory basis:</strong> MEPC.337(76) — Reference CII &nbsp;|&nbsp; '
            'MEPC.338(76) — Reduction factors &nbsp;|&nbsp; MEPC.339(76) — Rating boundaries'
            '</div>',
            unsafe_allow_html=True
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — EU ETS
# ════════════════════════════════════════════════════════════════════════════
with tab_ets:
    col_l, col_r = st.columns([1, 1.3], gap="large")

    with col_l:
        st.markdown('<div class="ff-section">ETS Liability</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="ets-card">'
            f'<div class="ets-label">Total EU ETS Liability</div>'
            f'<div class="ets-value">€{ets_liability:,.2f}</div>'
            f'<div class="ets-sub">{ets_year_display} &nbsp;|&nbsp; {voyage_display.split("(")[0].strip()} &nbsp;|&nbsp; €{ets_price}/tCO₂e</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        per_tonne = ets_liability / mi if mi > 0 else 0
        per_nm    = ets_liability / distance if distance > 0 else 0

        st.markdown(
            f'<div class="metric-card">'
            f'<div class="label">Liability per Tonne of Fuel</div>'
            f'<div class="value" style="color:#FF4B4B;">€{per_tonne:,.2f}</div>'
            f'<div class="unit">€ / tonne fuel consumed</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="label">Liability per Nautical Mile</div>'
            f'<div class="value" style="color:#FF4B4B;">€{per_nm:,.2f}</div>'
            f'<div class="unit">€ / nm</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        if ets["co2e_total"] == 0:
            st.markdown(
                '<div class="zero-box">'
                '⬡ <strong>Zero-emission fuel</strong> — no EU ETS liability generated.<br>'
                'e-H₂ and e-NH₃ produce no CO₂e under TtW accounting.'
                '</div>', unsafe_allow_html=True
            )

    with col_r:
        st.markdown('<div class="ff-section">Emissions Breakdown</div>', unsafe_allow_html=True)

        co2e      = ets["co2e_total"]
        breakdown = [
            ("Direct CO₂",      ets["co2_direct"], "#FF4B4B"),
            ("CH₄ (GWP × 28)",  ets["ch4_eq"],     "#6366f1"),
            ("N₂O (GWP × 265)", ets["n2o_eq"],      "#ec4899"),
        ]

        for label, val, colour in breakdown:
            pct   = (val / co2e * 100) if co2e > 0 else 0
            bar_w = max(pct, 1)
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="label">{label}</div>'
                f'<div style="display:flex; align-items:center; gap:0.8rem; margin: 0.3rem 0;">'
                f'<div style="flex:1; background:#E2E8F0; border-radius:4px; height:6px;">'
                f'<div style="width:{bar_w}%; background:{colour}; height:6px; border-radius:4px;"></div>'
                f'</div>'
                f'<span style="font-family:\'JetBrains Mono\',monospace; color:{colour}; font-size:0.75rem; min-width:45px; text-align:right;">{pct:.1f}%</span>'
                f'</div>'
                f'<div class="value" style="font-size:1.1rem; color:{colour};">{val:,.4f} <span style="font-size:0.75rem; color:#94a3b8;">tCO₂e</span></div>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown(
            f'<div class="metric-card" style="border-color:#fecaca;">'
            f'<div class="label">Total CO₂-equivalent</div>'
            f'<div class="value">{co2e:,.4f}</div>'
            f'<div class="unit">tCO₂e before coverage & phase-in</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="ff-section">Coverage & Phase-in</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="label">Voyage Coverage Factor (l)</div>'
            f'<div class="value" style="color:#FF4B4B;">{voyage_l:.0%}</div>'
            f'<div class="unit">{voyage_display}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="label">Phase-in Factor (p) — {ets_year_display}</div>'
            f'<div class="value" style="color:#FF4B4B;">{ets_phase_in:.0%}</div>'
            f'<div class="unit">of verified emissions are surrendered</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        if ets["mi_nc"] > 0:
            st.markdown(
                f'<div class="warn-box">'
                f'⚠ <strong>Methane slip detected</strong><br>'
                f'{ets["mi_nc"]:.4f} t of fuel is unburned (cj = {fuel_data[fuel_type]["cj"]}). '
                f'This contributes to the CH₄ GWP calculation under EU MRV.'
                f'</div>', unsafe_allow_html=True
            )

        st.markdown(
            '<div class="info-box">'
            '<strong>Formula:</strong> ETS Liability = CO₂e × ETS Price × l × p<br>'
            '<strong>Basis:</strong> EU MRV Regulation 2015/757 &nbsp;|&nbsp; EU ETS Directive 2003/87/EC'
            '</div>',
            unsafe_allow_html=True
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — SUMMARY
# ════════════════════════════════════════════════════════════════════════════
with tab_summary:
    st.markdown('<div class="ff-section">Vessel & Voyage</div>', unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(
            f'<div class="metric-card"><div class="label">Vessel Type</div>'
            f'<div class="value" style="font-size:1rem;">{vessel_display}</div>'
            f'<div class="unit">{cii["capacity_basis"]} = {cii["capacity"]:,} t</div></div>',
            unsafe_allow_html=True
        )
    with s2:
        st.markdown(
            f'<div class="metric-card"><div class="label">Fuel</div>'
            f'<div class="value" style="font-size:1rem;">{fuel_data[fuel_type]["label"]}</div>'
            f'<div class="unit">{mi:,.0f} t consumed &nbsp;|&nbsp; Cf = {fuel_data[fuel_type]["efco2"]}</div></div>',
            unsafe_allow_html=True
        )
    with s3:
        st.markdown(
            f'<div class="metric-card"><div class="label">Voyage</div>'
            f'<div class="value" style="font-size:1rem;">{distance:,} nm</div>'
            f'<div class="unit">Transport work: {cii["transport_work"]:,.0f} t·nm</div></div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="ff-section">Compliance Snapshot</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    r = cii["rating"]
    rating_bg = {"A":"#dcfce7","B":"#f0fdf4","C":"#fefce8","D":"#fff7ed","E":"#fef2f2"}
    rating_fg = {"A":"#16a34a","B":"#22c55e","C":"#ca8a04","D":"#ea580c","E":"#dc2626"}
    rating_bd = {"A":"#86efac","B":"#bbf7d0","C":"#fde68a","D":"#fdba74","E":"#fca5a5"}

    with c1:
        st.markdown(
            f'<div class="metric-card" style="background:{rating_bg[r]}; border-color:{rating_bd[r]};">'
            f'<div class="label">CII Rating</div>'
            f'<div class="value" style="color:{rating_fg[r]}; font-size:3rem; text-align:center;">{r}</div>'
            f'<div class="unit" style="text-align:center;">{RATING_DESCRIPTIONS[r]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f'<div class="metric-card"><div class="label">Attained CII</div>'
            f'<div class="value">{cii["attained"]:.4f}</div>'
            f'<div class="unit">g CO₂ / t·nm</div></div>',
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f'<div class="metric-card"><div class="label">Total CO₂e (ETS)</div>'
            f'<div class="value">{ets["co2e_total"]:,.2f}</div>'
            f'<div class="unit">tCO₂e (before coverage & phase-in)</div></div>',
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f'<div class="ets-card"><div class="ets-label">EU ETS Liability</div>'
            f'<div class="ets-value">€{ets_liability:,.2f}</div>'
            f'<div class="ets-sub">{ets_year_display} &nbsp;|&nbsp; €{ets_price}/tCO₂e</div></div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="ff-section">Regulatory References</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="info-box">'
        '<strong>CII:</strong> MEPC.337(76) — Reference CII parameters &nbsp;|&nbsp; '
        'MEPC.338(76) — Annual reduction factors &nbsp;|&nbsp; '
        'MEPC.339(76) — Rating boundary vectors<br>'
        '<strong>ETS:</strong> EU MRV Regulation 2015/757 &nbsp;|&nbsp; '
        'EU ETS Directive 2003/87/EC (amended) &nbsp;|&nbsp; '
        'IMO MEPC.1/Circ.795/Rev.6 — Emission factors<br>'
        '<strong>Validated against:</strong> Lloyd\'s Register CII Calculator (June 2026)'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="text-align:center; margin-top:2rem; color:#E2E8F0; font-size:0.75rem; font-family:\'JetBrains Mono\',monospace;">'
        'FUELFLOW · TRANSITION HOLDINGS · LAGOS'
        '</div>',
        unsafe_allow_html=True
    )
