import streamlit as st
import pandas as pd
import numpy as np
import joblib
from backend.auth import init_db, create_user, verify_user

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Tire Wear Prediction",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)
init_db()
AUTH_CSS = """
<style>

/* Remove ONLY the top empty container */
section.main > div:first-child {
    padding-top: 0rem !important;
}

/* Remove top spacing safely */
.block-container {
    padding-top: 0rem !important;
}

/* Hide header & footer */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* Login card */
.auth-box {
    background: rgba(255,255,255,0.08);
    padding: 40px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 0 30px rgba(0,0,0,0.4);
}

/* Button */
.stButton>button {
    width: 100%;
    background: linear-gradient(45deg, #ff9800, #ff5722);
    color: white;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
}

</style>
"""
def auth_gate():
    if st.session_state.get("auth_ok", False):
        return

    st.markdown(AUTH_CSS, unsafe_allow_html=True)

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown(
            "<h2 style='text-align:center;color:white;'>🚗 Tire Wear Prediction</h2>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align:center;color:#ddd;'>Sign in to access the dashboard</p>",
            unsafe_allow_html=True
        )

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            u = st.text_input("Username", key="login_user")
            p = st.text_input("Password", type="password", key="login_pass")

            if st.button("Login"):
                if verify_user(u, p):
                    st.session_state["auth_ok"] = True
                    st.session_state["auth_user"] = u.strip()
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with tab2:
            new_u = st.text_input("New Username", key="su_user")
            new_email = st.text_input("Email (optional)", key="su_email")
            new_p = st.text_input("New Password", type="password", key="su_pass")
            new_p2 = st.text_input("Confirm Password", type="password", key="su_pass2")

            if st.button("Create Account"):
                if new_p != new_p2:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = create_user(
                        new_u,
                        new_p,
                        new_email if new_email.strip() else None
                    )
                    if ok:
                        st.success("Account created. Go to Login tab and sign in.")
                    else:
                        st.error(msg)

    st.stop()

auth_gate()

# ------------------ THEME CSS ------------------
CUSTOM_CSS = """
<style>
.stApp{
  background:
    radial-gradient(900px 500px at 8% 8%, rgba(255,196,0,0.10), transparent 60%),
    radial-gradient(900px 550px at 95% 10%, rgba(60,160,255,0.10), transparent 60%),
    linear-gradient(180deg, #0a0f1d 0%, #060a14 100%);
}
.block-container{
  max-width: 1400px;
  padding-top: 1rem;
  padding-bottom: 2rem;
}
section[data-testid="stSidebar"]{
  background: rgba(255,255,255,0.04);
  border-right: 1px solid rgba(255,255,255,0.08);
}
.card{
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 18px;
  padding: 14px 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.25);
  backdrop-filter: blur(8px);
}
.hr{
  height: 1px;
  background: rgba(255,255,255,0.10);
  margin: 8px 0 12px 0;
  border-radius: 999px;
}
.small-muted{
  color: rgba(255,255,255,0.72);
  font-size: 0.9rem;
}

/* Wear badges */
.badge{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 999px;
  font-weight: 800;
  border: 1px solid rgba(255,255,255,0.12);
}
.badge-low{ background: rgba(34,197,94,0.16); color: #bbf7d0; }
.badge-mid{ background: rgba(245,158,11,0.18); color: #fde68a; }
.badge-high{ background: rgba(239,68,68,0.18); color: #fecaca; }

/* Tips and recommendations */
.tip-box{
  max-height: 240px;
  overflow-y: auto;
  padding-right: 6px;
}
.tip-item{
  display:flex;
  gap:10px;
  margin-bottom:10px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding:10px;
}
.tip-bar{
  width: 6px;
  border-radius: 999px;
  background: linear-gradient(180deg, #22c55e, #f59e0b, #ef4444);
}
.tip-text{
  color: rgba(255,255,255,0.88);
  font-size: 0.95rem;
  line-height: 1.25rem;
}
.rec-item{
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding:10px;
  margin-bottom:10px;
}
.rec-title{
  font-weight:700;
  margin-bottom:4px;
}
.rec-desc{
  color: rgba(255,255,255,0.80);
  font-size: 0.92rem;
}

/* Factor panel (screenshot style inspired) */
.factor-card{
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
  padding: 10px 12px;
}
.factor-title{
  font-weight: 800;
  font-size: 1.15rem;
  margin-bottom: 10px;
  color: #dbeafe;
}
.factor-row{
  display: grid;
  grid-template-columns: 170px 1fr;
  gap: 10px;
  align-items: center;
  margin-bottom: 10px;
}
.factor-label{
  color: rgba(255,255,255,0.92);
  font-weight: 600;
  font-size: 0.98rem;
}
.factor-track{
  position: relative;
  height: 16px;
  background: rgba(180,200,220,0.28);
  border-radius: 999px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.06);
}
.factor-fill{
  height: 100%;
  border-radius: 999px;
}
.factor-impact{
  position: absolute;
  right: 6px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0,0,0,0.30);
  color: white;
  font-size: 0.78rem;
  font-weight: 800;
  padding: 1px 8px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.15);
}

/* Maintenance alert card */
.alert-head{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:10px;
}
.alert-title{
  font-size:1.15rem;
  font-weight:800;
  color:#fee2e2;
}
.alert-icon{
  width:34px;
  height:34px;
  border-radius:999px;
  display:flex;
  align-items:center;
  justify-content:center;
  background: rgba(239,68,68,0.18);
  border:1px solid rgba(239,68,68,0.35);
  color:#fecaca;
  font-size:18px;
}
.alert-table{
  width:100%;
}
.alert-row{
  display:grid;
  grid-template-columns: 1.15fr 1fr 1fr;
  gap:10px;
  align-items:center;
  padding:8px 0;
  border-bottom:1px solid rgba(255,255,255,0.06);
}
.alert-row:last-child{
  border-bottom:none;
}
.alert-header{
  background: rgba(255,255,255,0.05);
  border-radius: 12px;
  padding:8px 10px;
  margin-bottom:8px;
  font-weight:700;
  color:#e5e7eb;
}
.pos-name{
  display:flex;
  align-items:center;
  gap:8px;
  font-weight:600;
  color:#f8fafc;
}
.dot{
  width:10px;
  height:10px;
  border-radius:999px;
  display:inline-block;
}
.level-pill{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  min-width:66px;
  padding:4px 10px;
  border-radius:999px;
  font-weight:800;
  color:white;
}
.action-pill{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  min-width:110px;
  padding:5px 10px;
  border-radius:999px;
  font-weight:800;
  border:1px solid rgba(255,255,255,0.08);
}
.action-danger{ background: rgba(239,68,68,0.20); color:#fecaca; }
.action-warn{ background: rgba(245,158,11,0.18); color:#fde68a; }
.action-mid{ background: rgba(250,204,21,0.14); color:#fde047; }
.action-good{ background: rgba(34,197,94,0.14); color:#bbf7d0; }

/* Forecast tire cards */
.tire-mini-card{
  background: rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.08);
  border-radius:14px;
  padding:10px;
  margin-bottom:10px;
}
.tire-mini-title{
  font-weight:700;
  color:#f8fafc;
}
.tire-mini-value{
  font-size:1.35rem;
  font-weight:800;
  margin-top:4px;
}
.tire-mini-track{
  height:8px;
  background: rgba(255,255,255,0.08);
  border-radius:999px;
  margin-top:8px;
  overflow:hidden;
}
.tire-mini-fill{
  height:8px;
  border-radius:999px;
}

.stButton > button, .stFormSubmitButton > button{
  border-radius: 14px;
  padding: 10px 14px;
  border: 1px solid rgba(255,255,255,0.14);
  background: linear-gradient(90deg, rgba(255,185,0,0.95), rgba(255,120,0,0.92));
  color: #111827;
  font-weight: 900;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ------------------ LOAD MODEL ------------------
@st.cache_resource
def load_model():
    return joblib.load("tire_wear_model.pkl")

model = load_model()

# ------------------ VEHICLE PROFILES ------------------
vehicle_profiles = {
    "Sedan": {"max_load": 500, "safe_speed": 90, "brake_tolerance": 4},
    "SUV": {"max_load": 700, "safe_speed": 100, "brake_tolerance": 6},
    "Truck": {"max_load": 1200, "safe_speed": 80, "brake_tolerance": 8},
}

# ------------------ SESSION STATE ------------------
if "has_result" not in st.session_state:
    st.session_state.has_result = False

# ------------------ HELPERS (UI ONLY) ------------------
def get_badge_html(wear_bucket, final_wear):
    if wear_bucket == "low":
        return f"<span class='badge badge-low'>🟢 Low Tire Wear ({final_wear:.2f})</span>"
    elif wear_bucket == "moderate":
        return f"<span class='badge badge-mid'>🟡 Moderate Tire Wear ({final_wear:.2f})</span>"
    return f"<span class='badge badge-high'>🔴 High Tire Wear - Maintenance Needed ({final_wear:.2f})</span>"

def build_factor_scores(inp, load_stress, speed_stress, brake_stress):
    # UI-only factor scores (0 to 10). Core prediction logic stays unchanged.
    pressure_dev = abs(float(inp["tire_pressure"]) - 32.0)
    weather_temp = float(inp["ambient_temp"])

    road_score_map = {"Poor": 7.2, "Average": 5.0, "Good": 2.8}

    speed_score = float(np.clip(speed_stress * 8.5, 0, 10))
    brake_score = float(np.clip(brake_stress * 6.8, 0, 10))
    load_score = float(np.clip(load_stress * 6.2, 0, 10))

    if weather_temp >= 38:
        weather_score = 5.8
    elif weather_temp >= 32:
        weather_score = 4.8
    elif weather_temp >= 25:
        weather_score = 3.6
    else:
        weather_score = 2.8

    pressure_score = float(np.clip(2.0 + pressure_dev * 1.5, 0, 10))

    factors = [
        ("Driving Speed", speed_score, "#ef4444"),
        ("Road Surface", road_score_map[inp["road_condition"]], "#f59e0b"),
        ("Braking", brake_score, "#facc15"),
        ("Tire Pressure", pressure_score, "#22c55e"),
        ("Weather", weather_score, "#3b82f6"),
        ("Vehicle Load", load_score, "#10b981"),
    ]
    return sorted(factors, key=lambda x: x[1], reverse=True)

def render_factor_panel(inp, load_stress, speed_stress, brake_stress):
    factors = build_factor_scores(inp, load_stress, speed_stress, brake_stress)

    rows_html = []
    for i, (label, score, color) in enumerate(factors):
        width_pct = int(np.clip((score / 10.0) * 100, 0, 100))
        impact_html = f"<span class='factor-impact'>Impact {score:.1f}</span>" if i == 0 else ""
        rows_html.append(
            f"""
            <div class="factor-row">
              <div class="factor-label">{label}</div>
              <div class="factor-track">
                <div class="factor-fill" style="width:{width_pct}%; background:{color};"></div>
                {impact_html}
              </div>
            </div>
            """
        )

    html = f"""
    <div class="factor-card">
      <div class="factor-title">Factors Affecting Wear</div>
      {''.join(rows_html)}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def get_input_based_tips(inp, profile, load_stress, speed_stress, brake_stress, wear_bucket):
    tips = []

    if inp["avg_speed"] > profile["safe_speed"]:
        tips.append("Speed is above the safe limit for this vehicle type. Reduce cruising speed.")
    elif inp["avg_speed"] >= profile["safe_speed"] * 0.9:
        tips.append("Speed is near the safe threshold. Smooth acceleration helps tire life.")
    else:
        tips.append("Speed is in a good range for tire longevity.")

    if inp["vehicle_load"] > profile["max_load"] * 0.9:
        tips.append("Vehicle load is high for this vehicle type. Reduce extra cargo if possible.")
    elif inp["vehicle_load"] > profile["max_load"] * 0.75:
        tips.append("Load is moderately high. Check tire pressure regularly.")
    else:
        tips.append("Vehicle load is in a comfortable range for this vehicle type.")

    if inp["braking_frequency"] > profile["brake_tolerance"]:
        tips.append("Frequent braking is increasing tire stress. Keep more following distance.")
    elif inp["braking_frequency"] >= profile["brake_tolerance"] * 0.8:
        tips.append("Braking frequency is a bit high. Brake more smoothly when possible.")
    else:
        tips.append("Braking frequency looks reasonable.")

    if inp["tire_pressure"] < 30:
        tips.append("Tire pressure is low. Under-inflation can increase heat and wear.")
    elif inp["tire_pressure"] > 35:
        tips.append("Tire pressure is high. Over-inflation may increase center wear.")
    else:
        tips.append("Tire pressure is in a balanced range.")

    if inp["road_condition"] == "Poor":
        tips.append("Poor road condition can accelerate tire wear. Inspect tires more often.")
    if inp["driving_style"] == "Aggressive":
        tips.append("Aggressive driving style increases wear through hard braking and acceleration.")
    if inp["ambient_temp"] >= 35:
        tips.append("High ambient temperature can increase tire heat buildup.")
    if inp["tire_age"] >= 36:
        tips.append("Older tire age detected. Rubber aging may affect performance.")

    if wear_bucket == "high":
        tips.append("Predicted wear is high for the current inputs. Plan maintenance soon.")
    elif wear_bucket == "moderate":
        tips.append("Predicted wear is moderate. Monitor tread and plan rotation.")
    else:
        tips.append("Predicted wear is low. Continue regular checks and good driving habits.")

    scored = []
    for t in tips:
        s = 0.0
        tl = t.lower()
        if "speed" in tl:
            s += speed_stress
        if "load" in tl or "cargo" in tl:
            s += load_stress
        if "braking" in tl or "brake" in tl:
            s += brake_stress
        if "high" in tl or "maintenance" in tl:
            s += 0.3
        scored.append((s, t))

    scored.sort(key=lambda x: x[0], reverse=True)

    seen, out = set(), []
    for _, t in scored:
        if t not in seen:
            out.append(t)
            seen.add(t)
    return out[:8]

def get_input_based_recommendations(inp, wear_bucket, load_stress, speed_stress, brake_stress):
    recs = []

    stress_parts = {"Load": load_stress, "Speed": speed_stress, "Braking": brake_stress}
    top_driver = max(stress_parts, key=stress_parts.get)

    if top_driver == "Load":
        recs.append(("Reduce Load", "Keep cargo closer to the recommended limit for the selected vehicle type."))
    elif top_driver == "Speed":
        recs.append(("Control Speed", "Drive closer to the safe speed for this vehicle type to reduce wear."))
    else:
        recs.append(("Smooth Braking", "Avoid frequent hard braking and maintain a safe following distance."))

    if inp["tire_pressure"] < 30:
        recs.append(("Increase Tire Pressure", "Bring pressure to the recommended range to reduce excess heat and wear."))
    elif inp["tire_pressure"] > 35:
        recs.append(("Reduce Tire Pressure Slightly", "Over-inflation can increase center wear and reduce grip."))

    if inp["tire_age"] >= 36:
        recs.append(("Inspect Tire Age", "Check tread and sidewalls. Older tires may need replacement soon."))

    if inp["road_condition"] == "Poor":
        recs.append(("Alignment Check", "Rough roads can affect alignment and tire wear patterns."))

    if inp["driving_style"] == "Aggressive":
        recs.append(("Driving Habit Improvement", "Smoother acceleration and braking helps tire life."))

    if wear_bucket == "high":
        recs.append(("Service Soon", "Schedule inspection, rotation, alignment, and tread depth check soon."))
    elif wear_bucket == "moderate":
        recs.append(("Planned Maintenance", "Monitor tread and rotate tires at the next service interval."))
    else:
        recs.append(("Routine Monitoring", "Continue regular tire pressure checks and rotation schedule."))

    return recs[:6]

def compute_tire_positions(final_wear, braking_frequency, road_condition, driving_style):
    # UI only. Does not change prediction logic.
    front_bias = 1.10 if braking_frequency >= 5 else 1.00
    style_bias = 1.08 if driving_style == "Aggressive" else (1.03 if driving_style == "Normal" else 0.98)
    road_bias = 1.08 if road_condition == "Poor" else (1.03 if road_condition == "Average" else 0.98)

    base_pct = float(np.clip(final_wear * 10, 5, 95))

    fl = np.clip(base_pct * front_bias * style_bias * road_bias, 0, 100)
    fr = np.clip(base_pct * front_bias * (1.02 if road_condition == "Poor" else 1.0), 0, 100)
    rl = np.clip(base_pct * (0.78 if driving_style == "Smooth" else 0.88) * road_bias, 0, 100)
    rr = np.clip(base_pct * (0.84 if braking_frequency < 4 else 0.95) * road_bias, 0, 100)

    return {
        "Front Left": round(float(fl), 1),
        "Front Right": round(float(fr), 1),
        "Rear Right": round(float(rr), 1),
        "Rear Left": round(float(rl), 1),
    }

def _severity_from_pct(v):
    if v >= 70:
        return ("Replace Soon!", "danger", "#ef4444")
    elif v >= 55:
        return ("Check Soon", "warn", "#f97316")
    elif v >= 40:
        return ("Moderate", "mid", "#eab308")
    else:
        return ("Good", "good", "#16a34a")
def render_factor_panel(inp, load_stress, speed_stress, brake_stress):
    factors = build_factor_scores(inp, load_stress, speed_stress, brake_stress)

    rows_html = []
    for i, (label, score, color) in enumerate(factors):
        width_pct = int(np.clip((score / 10.0) * 100, 0, 100))
        impact_html = f"<span class='factor-impact'>Impact {score:.1f}</span>" if i == 0 else ""

        row = (
            f"<div class='factor-row'>"
            f"<div class='factor-label'>{label}</div>"
            f"<div class='factor-track'>"
            f"<div class='factor-fill' style='width:{width_pct}%; background:{color};'></div>"
            f"{impact_html}"
            f"</div>"
            f"</div>"
        )
        rows_html.append(row)

    html = (
        "<div class='card'>"
        "<div class='factor-title'>Factors Affecting Wear</div>"
        "<div class='hr'></div>"
        f"{''.join(rows_html)}"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)
def render_maintenance_alert(tire_positions):
    order = ["Front Left", "Front Right", "Rear Right", "Rear Left"]

    rows_html = []
    for pos in order:
        v = float(tire_positions[pos])
        action_text, action_class, pill_color = _severity_from_pct(v)

        row = (
            "<div class='alert-row'>"
            f"<div class='pos-name'><span class='dot' style='background:{pill_color};'></span><span>{pos}</span></div>"
            f"<div><span class='level-pill' style='background:{pill_color};'>{v:.0f}%</span></div>"
            f"<div><span class='action-pill action-{action_class}'>{action_text}</span></div>"
            "</div>"
        )
        rows_html.append(row)

    html = (
        "<div class='card'>"
        "<div class='alert-head'>"
        "<div class='alert-title'>⚠️ Maintenance Alert</div>"
        "<div class='alert-icon'>🚨</div>"
        "</div>"
        "<div class='hr'></div>"
        "<div class='alert-header alert-row' style='grid-template-columns: 1.15fr 1fr 1fr;'>"
        "<div>Tire Position</div><div>Wear Level</div><div>Action</div>"
        "</div>"
        f"{''.join(rows_html)}"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown(
    """
    <div class="card">
      <h1 style="margin:0;">🚗 Tire Wear Prediction System</h1>
      <div class="small-muted">Vehicle-type-aware tire wear prediction with dynamic tips and recommendations.</div>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("")

# ------------------ INPUTS (SIDEBAR) ------------------
with st.sidebar:
    st.markdown("## Inputs")
    with st.form("tire_form"):
        avg_speed = st.slider("Average Speed (km/h)", 30, 120, 60)
        distance_driven = st.slider("Distance Driven (km)", 500, 20000, 5000)
        braking_frequency = st.slider("Braking Frequency (per 100 km)", 1, 10, 3)
        vehicle_load = st.slider("Vehicle Load (kg)", 200, 1200, 400)
        tire_pressure = st.slider("Tire Pressure (PSI)", 28.0, 36.0, 32.0, step=0.5)
        tire_age = st.slider("Tire Age (months)", 1, 48, 12)
        ambient_temp = st.slider("Ambient Temperature (°C)", 10, 45, 25)

        road_condition = st.selectbox("Road Condition", ["Poor", "Average", "Good"])
        vehicle_type = st.selectbox("Vehicle Type", ["Sedan", "SUV", "Truck"])
        driving_style = st.selectbox("Driving Style", ["Smooth", "Normal", "Aggressive"])

        submitted = st.form_submit_button("🔍 Predict Tire Wear")

# ------------------ PREDICTION (ORIGINAL LOGIC PRESERVED) ------------------
if submitted:
    road_map = {"Poor": 0, "Average": 1, "Good": 2}
    vehicle_map = {"Sedan": 0, "SUV": 1, "Truck": 2}
    driving_map = {"Smooth": 0, "Normal": 1, "Aggressive": 2}

    input_df = pd.DataFrame([{
        "avg_speed": avg_speed,
        "distance_driven": distance_driven,
        "braking_frequency": braking_frequency,
        "vehicle_load": vehicle_load,
        "tire_pressure": tire_pressure,
        "tire_age_months": tire_age,
        "ambient_temperature": ambient_temp,
        "road_condition": road_map[road_condition],
        "vehicle_type": vehicle_map[vehicle_type],
        "driving_style": driving_map[driving_style],
    }])

    # Original ML prediction
    ml_wear = float(np.clip(model.predict(input_df)[0], 0, 10))

    # Original vehicle-aware stress logic
    profile = vehicle_profiles[vehicle_type]
    load_stress = vehicle_load / profile["max_load"]
    speed_stress = avg_speed / profile["safe_speed"]
    brake_stress = braking_frequency / profile["brake_tolerance"]

    stress_score = (
        0.4 * load_stress +
        0.3 * speed_stress +
        0.3 * brake_stress
    )

    # Original final wear decision (UNCHANGED)
    if stress_score < 0.9:
        final_wear = float(np.clip(ml_wear, 0, 3))
        wear_bucket = "low"
        status_text = "Low Tire Wear"
    elif stress_score < 1.2:
        final_wear = float(np.clip(ml_wear, 3, 6))
        wear_bucket = "moderate"
        status_text = "Moderate Tire Wear"
    else:
        final_wear = float(np.clip(ml_wear, 6, 10))
        wear_bucket = "high"
        status_text = "High Tire Wear - Maintenance Needed"

    st.session_state.has_result = True
    st.session_state.result = {
        "final_wear": final_wear,
        "ml_wear": ml_wear,
        "wear_bucket": wear_bucket,
        "status_text": status_text,
        "load_stress": float(load_stress),
        "speed_stress": float(speed_stress),
        "brake_stress": float(brake_stress),
        "stress_score": float(stress_score),
        "profile": profile,
        "inputs": {
            "avg_speed": avg_speed,
            "distance_driven": distance_driven,
            "braking_frequency": braking_frequency,
            "vehicle_load": vehicle_load,
            "tire_pressure": tire_pressure,
            "tire_age": tire_age,
            "ambient_temp": ambient_temp,
            "road_condition": road_condition,
            "vehicle_type": vehicle_type,
            "driving_style": driving_style,
        }
    }

# ------------------ SHOW RESULT ------------------
if not st.session_state.has_result:
    st.info("Select inputs and click Predict Tire Wear.")
    st.stop()

res = st.session_state.result
final_wear = res["final_wear"]
ml_wear = res["ml_wear"]
wear_bucket = res["wear_bucket"]     # low / moderate / high from ORIGINAL stress logic
status_text = res["status_text"]
load_stress = res["load_stress"]
speed_stress = res["speed_stress"]
brake_stress = res["brake_stress"]
stress_score = res["stress_score"]
profile = res["profile"]
inp = res["inputs"]

tips = get_input_based_tips(inp, profile, load_stress, speed_stress, brake_stress, wear_bucket)
recs = get_input_based_recommendations(inp, wear_bucket, load_stress, speed_stress, brake_stress)
tire_positions = compute_tire_positions(final_wear, inp["braking_frequency"], inp["road_condition"], inp["driving_style"])

# ------------------ MAIN LAYOUT (2 COLUMN STRUCTURED) ------------------
left_col, right_col = st.columns([1.2, 1.0], gap="large")

# LEFT COLUMN. Forecast + Explanation
with left_col:
    # Forecast card
    st.markdown("<div class='card'><h3 style='margin:0;'>Tire Wear Forecast</h3><div class='hr'></div>", unsafe_allow_html=True)

    st.markdown(f"<div style='margin:8px 0 10px 0'>{get_badge_html(wear_bucket, final_wear)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-muted' style='margin-bottom:12px;'>{status_text}</div>", unsafe_allow_html=True)

    a, b = st.columns(2)
    c, d = st.columns(2)

    def pos_card(title, value):
        color = "#22c55e" if value < 35 else "#f59e0b" if value < 65 else "#ef4444"
        st.markdown(
            f"""
            <div class="tire-mini-card">
                <div class="tire-mini-title">{title}</div>
                <div class="tire-mini-value" style="color:{color};">{value:.1f}%</div>
                <div class="tire-mini-track">
                    <div class="tire-mini-fill" style="width:{min(value,100)}%; background:{color};"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with a:
        pos_card("Front Left", tire_positions["Front Left"])
    with b:
        pos_card("Front Right", tire_positions["Front Right"])
    with c:
        pos_card("Rear Left", tire_positions["Rear Left"])
    with d:
        pos_card("Rear Right", tire_positions["Rear Right"])

    st.caption("Per tire percentages are visual indicators only. Core prediction logic is unchanged.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # Explanation card
    st.markdown("<div class='card'><h3 style='margin:0;'>Wear Explanation</h3><div class='hr'></div>", unsafe_allow_html=True)

    if wear_bucket == "low":
        st.success(f"🟢 Low Tire Wear ({final_wear:.2f})")
    elif wear_bucket == "moderate":
        st.warning(f"🟡 Moderate Tire Wear ({final_wear:.2f})")
    else:
        st.error(f"🔴 High Tire Wear - Maintenance Needed ({final_wear:.2f})")

    st.progress(min(final_wear / 10.0, 1.0))
    st.caption("Final wear severity scale from 0 to 10.")

    e1, e2 = st.columns(2)
    with e1:
        st.write(f"ML Wear Prediction: **{ml_wear:.2f}**")
        st.write(f"Load Stress: **{load_stress:.2f}**")
        st.write(f"Speed Stress: **{speed_stress:.2f}**")
    with e2:
        st.write(f"Braking Stress: **{brake_stress:.2f}**")
        st.write(f"Overall Stress Score: **{stress_score:.2f}**")
        st.write(f"Vehicle Type: **{inp['vehicle_type']}**")

    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT COLUMN. Factor panel + Maintenance Alert + Tips + Recommendations
with right_col:
    render_factor_panel(inp, load_stress, speed_stress, brake_stress)
    st.write("")

    render_maintenance_alert(tire_positions)
    st.write("")

    tips_html = "".join(
        [f"<div class='tip-item'><div class='tip-bar'></div><div class='tip-text'>{t}</div></div>" for t in tips]
    )
    st.markdown(
        f"""
        <div class="card">
          <h3 style="margin:0;">Dynamic Tips (Based on Inputs)</h3>
          <div class="hr"></div>
          <div class="tip-box">{tips_html}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    rec_html = ""
    for title, desc in recs:
        rec_html += f"""
        <div class="rec-item">
          <div class="rec-title">{title}</div>
          <div class="rec-desc">{desc}</div>
        </div>
        """

    st.markdown(
        f"""
        <div class="card">
          <h3 style="margin:0;">Recommendations (Based on Inputs)</h3>
          <div class="hr"></div>
          <div class="tip-box">{rec_html}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    

    st.markdown("</div>", unsafe_allow_html=True)