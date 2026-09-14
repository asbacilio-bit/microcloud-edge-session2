import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MicroCloud-Edge | Business Resilience Simulator",
    page_icon="☁️",
    layout="wide",
)

st.title("☁️ MicroCloud-Edge")
st.subheader("Business Resilience Simulator")
st.caption(
    "Session 2 — Interactive simulation of internal and external business stress. "
    "Technology selected: Cloud and Edge Computing."
)

# -----------------------------
# Helper functions
# -----------------------------
def money(x):
    return f"S/ {x:,.2f}"

def clamp(x, low=0, high=100):
    return max(low, min(high, x))

def simulate(
    customers,
    price,
    fixed_costs,
    variable_cost,
    demand_drop,
    competitor_pressure,
    inflation,
    connectivity,
    operating_cost_increase,
    technical_failure,
    productivity_loss,
    support_increase,
    cloud_edge_advantage,
):
    # Baseline
    base_revenue = customers * price
    base_variable = customers * variable_cost
    base_costs = fixed_costs + base_variable
    base_profit = base_revenue - base_costs
    base_margin = (base_profit / base_revenue * 100) if base_revenue else 0

    # Stress-adjusted demand.
    # Competitor pressure adds to the loss of demand.
    effective_demand_drop = clamp(demand_drop + competitor_pressure * 0.5, 0, 95)

    # Cloud-edge resilience reduces the impact of connectivity disruption.
    # This is a model assumption for the simulation, not a measured technical result.
    connectivity_effect = connectivity * (1 - cloud_edge_advantage / 100)

    stressed_customers = max(
        0,
        customers * (
            1
            - effective_demand_drop / 100
            - technical_failure * 0.20 / 100
            - productivity_loss * 0.25 / 100
        )
    )

    stressed_price = price * max(0.5, 1 - inflation * 0.20 / 100)
    stressed_revenue = stressed_customers * stressed_price

    stressed_variable_cost = stressed_customers * variable_cost
    stressed_costs = (
        fixed_costs
        * (1 + operating_cost_increase / 100)
        + stressed_variable_cost
        * (1 + inflation / 100)
        + stressed_revenue * (support_increase / 100)
    )

    # Connectivity still affects operations, but less when local Edge processing
    # is assumed to maintain part of the operation.
    operational_penalty = connectivity_effect * 0.25 / 100
    stressed_revenue *= max(0.50, 1 - operational_penalty)

    stressed_profit = stressed_revenue - stressed_costs
    stressed_margin = (stressed_profit / stressed_revenue * 100) if stressed_revenue else -100

    revenue_change = (
        (stressed_revenue - base_revenue) / base_revenue * 100
        if base_revenue else -100
    )

    profit_change = (
        (stressed_profit - base_profit) / abs(base_profit) * 100
        if base_profit != 0 else -100
    )

    # Resilience score:
    # 40% financial performance, 25% revenue retention,
    # 20% operational continuity, 15% margin.
    profit_component = clamp((stressed_profit / max(base_revenue, 1) + 0.5) * 100)
    revenue_component = clamp((stressed_revenue / max(base_revenue, 1)) * 100)
    continuity_component = clamp(100 - (
        technical_failure * 0.50
        + productivity_loss * 0.40
        + connectivity_effect * 0.60
    ))
    margin_component = clamp(stressed_margin + 50)

    score = (
        profit_component * 0.40
        + revenue_component * 0.25
        + continuity_component * 0.20
        + margin_component * 0.15
    )
    score = round(clamp(score), 1)

    if score >= 80:
        category = "HIGH RESILIENCE"
        interpretation = "The business model absorbs the simulated stress relatively well."
    elif score >= 60:
        category = "MODERATE RESILIENCE"
        interpretation = "The business remains viable, but some variables require corrective action."
    elif score >= 40:
        category = "LOW RESILIENCE"
        interpretation = "The stress produces significant deterioration. The model needs adaptation."
    else:
        category = "CRITICAL"
        interpretation = "The business model is highly vulnerable under the selected stress conditions."

    return {
        "base_revenue": base_revenue,
        "base_costs": base_costs,
        "base_profit": base_profit,
        "base_margin": base_margin,
        "stressed_customers": stressed_customers,
        "stressed_revenue": stressed_revenue,
        "stressed_costs": stressed_costs,
        "stressed_profit": stressed_profit,
        "stressed_margin": stressed_margin,
        "revenue_change": revenue_change,
        "profit_change": profit_change,
        "score": score,
        "category": category,
        "interpretation": interpretation,
        "connectivity_effect": connectivity_effect,
    }

# -----------------------------
# Sidebar: business model
# -----------------------------
st.sidebar.header("1. Business model")

customers = st.sidebar.number_input(
    "Initial customers", min_value=1, max_value=10000, value=20, step=1
)
price = st.sidebar.number_input(
    "Monthly subscription per customer (S/)",
    min_value=1.0,
    max_value=5000.0,
    value=50.0,
    step=5.0,
)
fixed_costs = st.sidebar.number_input(
    "Monthly fixed costs (S/)",
    min_value=0.0,
    max_value=100000.0,
    value=400.0,
    step=50.0,
)
variable_cost = st.sidebar.number_input(
    "Variable cost per customer (S/)",
    min_value=0.0,
    max_value=1000.0,
    value=10.0,
    step=1.0,
)

st.sidebar.header("2. External stress")

demand_drop = st.sidebar.slider(
    "Demand decrease (%)", 0, 90, 20, 5
)
competitor_pressure = st.sidebar.slider(
    "Competitor pressure (%)", 0, 80, 10, 5
)
inflation = st.sidebar.slider(
    "Inflation / input-cost pressure (%)", 0, 80, 10, 5
)
connectivity = st.sidebar.slider(
    "Connectivity disruption (%)", 0, 100, 20, 5
)

st.sidebar.header("3. Internal stress")

operating_cost_increase = st.sidebar.slider(
    "Operating-cost increase (%)", 0, 100, 15, 5
)
technical_failure = st.sidebar.slider(
    "Technical failure impact (%)", 0, 80, 10, 5
)
productivity_loss = st.sidebar.slider(
    "Productivity loss (%)", 0, 80, 10, 5
)
support_increase = st.sidebar.slider(
    "Support / maintenance increase (%)", 0, 80, 10, 5
)

st.sidebar.header("4. Cloud-Edge resilience assumption")
cloud_edge_advantage = st.sidebar.slider(
    "Connectivity impact reduction from Edge (%)",
    0,
    100,
    70,
    5,
    help=(
        "Simulation assumption: local Edge processing reduces the business impact "
        "of connectivity disruption. This value must later be validated with the "
        "physical prototype."
    ),
)

# -----------------------------
# Presets
# -----------------------------
st.markdown("### Scenario presets")

preset_cols = st.columns(4)

if preset_cols[0].button("Normal"):
    st.session_state["preset"] = "normal"
if preset_cols[1].button("Moderate Crisis"):
    st.session_state["preset"] = "moderate"
if preset_cols[2].button("Severe Crisis"):
    st.session_state["preset"] = "severe"
if preset_cols[3].button("Custom"):
    st.session_state["preset"] = "custom"

preset = st.session_state.get("preset", "moderate")

preset_values = {
    "normal": {
        "demand": 0, "competitor": 0, "inflation": 0, "connectivity": 0,
        "operating": 0, "technical": 0, "productivity": 0, "support": 0,
    },
    "moderate": {
        "demand": 20, "competitor": 10, "inflation": 10, "connectivity": 20,
        "operating": 15, "technical": 10, "productivity": 10, "support": 10,
    },
    "severe": {
        "demand": 50, "competitor": 30, "inflation": 30, "connectivity": 70,
        "operating": 40, "technical": 35, "productivity": 30, "support": 30,
    },
}

# A preset cannot directly move sidebar widgets after they are rendered.
# We therefore show the selected preset and provide a one-click "simulate preset"
# button that uses preset values for the calculation.
if preset in preset_values:
    p = preset_values[preset]
    sim = simulate(
        customers, price, fixed_costs, variable_cost,
        p["demand"], p["competitor"], p["inflation"], p["connectivity"],
        p["operating"], p["technical"], p["productivity"], p["support"],
        cloud_edge_advantage,
    )
    scenario_label = {
        "normal": "Normal scenario",
        "moderate": "Moderate crisis",
        "severe": "Severe crisis",
    }[preset]
else:
    sim = simulate(
        customers, price, fixed_costs, variable_cost,
        demand_drop, competitor_pressure, inflation, connectivity,
        operating_cost_increase, technical_failure, productivity_loss,
        support_increase, cloud_edge_advantage,
    )
    scenario_label = "Custom scenario"

st.info(
    f"**Active scenario:** {scenario_label}. "
    "The model compares baseline performance with the selected stress conditions."
)

# -----------------------------
# KPI section
# -----------------------------
st.markdown("## Simulation result")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Resilience score", f"{sim['score']}/100")
k2.metric("Stressed revenue", money(sim["stressed_revenue"]))
k3.metric("Stressed profit", money(sim["stressed_profit"]))
k4.metric("Stressed margin", f"{sim['stressed_margin']:.1f}%")

st.success(f"### {sim['category']}\n\n{sim['interpretation']}")

# -----------------------------
# Baseline vs stressed
# -----------------------------
comparison = pd.DataFrame(
    {
        "Baseline": [
            sim["base_revenue"],
            sim["base_costs"],
            sim["base_profit"],
            sim["base_margin"],
        ],
        "Stressed": [
            sim["stressed_revenue"],
            sim["stressed_costs"],
            sim["stressed_profit"],
            sim["stressed_margin"],
        ],
    },
    index=["Revenue (S/)", "Costs (S/)", "Profit (S/)", "Margin (%)"],
)

st.markdown("### Baseline vs. stress")
st.dataframe(comparison, use_container_width=True)

chart_data = pd.DataFrame(
    {
        "Baseline": [sim["base_revenue"], sim["base_costs"], sim["base_profit"]],
        "Stressed": [sim["stressed_revenue"], sim["stressed_costs"], sim["stressed_profit"]],
    },
    index=["Revenue", "Costs", "Profit"],
)
st.bar_chart(chart_data)

# -----------------------------
# Interpretation
# -----------------------------
st.markdown("### Business interpretation")

left, right = st.columns(2)

with left:
    st.write("**External stress impact**")
    st.write(f"- Demand decrease: {demand_drop if preset == 'custom' else preset_values[preset]['demand']}%")
    st.write(f"- Competitor pressure: {competitor_pressure if preset == 'custom' else preset_values[preset]['competitor']}%")
    st.write(f"- Inflation pressure: {inflation if preset == 'custom' else preset_values[preset]['inflation']}%")
    st.write(f"- Connectivity disruption: {connectivity if preset == 'custom' else preset_values[preset]['connectivity']}%")

with right:
    st.write("**Internal stress impact**")
    st.write(f"- Operating-cost increase: {operating_cost_increase if preset == 'custom' else preset_values[preset]['operating']}%")
    st.write(f"- Technical failure impact: {technical_failure if preset == 'custom' else preset_values[preset]['technical']}%")
    st.write(f"- Productivity loss: {productivity_loss if preset == 'custom' else preset_values[preset]['productivity']}%")
    st.write(f"- Support/maintenance increase: {support_increase if preset == 'custom' else preset_values[preset]['support']}%")

st.markdown("### Key decision signals")

signals = []

if sim["stressed_profit"] < 0:
    signals.append("⚠️ The business becomes unprofitable under the selected stress.")
elif sim["stressed_profit"] < sim["base_profit"]:
    signals.append("⚠️ Profit decreases under stress; cost and demand management are priorities.")

if sim["revenue_change"] <= -30:
    signals.append("⚠️ Revenue retention is weak; customer acquisition and retention need attention.")

if sim["stressed_margin"] < 15:
    signals.append("⚠️ The stressed margin is low; review pricing and variable costs.")

if connectivity > 0 and cloud_edge_advantage > 0:
    signals.append(
        "☁️ Edge computing is modeled as a resilience mechanism that reduces the business "
        "impact of connectivity disruption."
    )

if not signals:
    signals.append("✅ The model remains comparatively stable under the selected scenario.")

for signal in signals:
    st.write(signal)

st.caption(
    "Important: the resilience score is a management simulation, not a scientific forecast. "
    "The Cloud-Edge connectivity benefit is an explicit assumption that should be validated "
    "later using the project's physical prototype and measured indicators."
)

# -----------------------------
# Methodology
# -----------------------------
with st.expander("Simulation methodology"):
    st.write(
        "The simulator establishes a baseline from customers, price, fixed costs and "
        "variable costs. It then applies internal and external stress factors and compares "
        "the resulting revenue, costs, profit and margin with the baseline."
    )
    st.write(
        "The resilience score combines four dimensions: financial performance (40%), "
        "revenue retention (25%), operational continuity (20%) and stressed margin (15%)."
    )
    st.write(
        "For the Cloud-Edge business model, connectivity disruption can be partially mitigated "
        "by local Edge processing. The percentage selected by the user is a modeling assumption "
        "and must not be presented as a measured technical result."
    )

st.markdown("---")
st.caption("MicroCloud-Edge — Management by Results | Session 2")