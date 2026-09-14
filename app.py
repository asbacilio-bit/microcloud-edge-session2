import streamlit as st
import pandas as pd

st.set_page_config(page_title="MicroCloud-Edge | Business Resilience Simulator", page_icon="☁️", layout="wide")

# -----------------------------
# Language
# -----------------------------
st.sidebar.header("🌐 Language / Idioma")
language = st.sidebar.radio("Choose / Elegir", ["English", "Español"], horizontal=True)
es = language == "Español"

def T(en, es_text):
    return es_text if es else en

def money(x):
    return f"S/ {x:,.2f}"

def clamp(x, low=0, high=100):
    return max(low, min(high, x))

def simulate(customers, price, fixed_costs, variable_cost, demand_drop, competitor_pressure,
             inflation, connectivity, operating_cost_increase, technical_failure,
             productivity_loss, support_increase, cloud_edge_advantage):
    base_revenue = customers * price
    base_variable = customers * variable_cost
    base_costs = fixed_costs + base_variable
    base_profit = base_revenue - base_costs
    base_margin = (base_profit / base_revenue * 100) if base_revenue else 0

    effective_demand_drop = clamp(demand_drop + competitor_pressure * 0.5, 0, 95)
    connectivity_effect = connectivity * (1 - cloud_edge_advantage / 100)

    stressed_customers = max(0, customers * (
        1 - effective_demand_drop / 100
        - technical_failure * 0.20 / 100
        - productivity_loss * 0.25 / 100
    ))
    stressed_price = price * max(0.5, 1 - inflation * 0.20 / 100)
    stressed_revenue = stressed_customers * stressed_price
    stressed_variable_cost = stressed_customers * variable_cost
    stressed_costs = (
        fixed_costs * (1 + operating_cost_increase / 100)
        + stressed_variable_cost * (1 + inflation / 100)
        + stressed_revenue * (support_increase / 100)
    )
    operational_penalty = connectivity_effect * 0.25 / 100
    stressed_revenue *= max(0.50, 1 - operational_penalty)
    stressed_profit = stressed_revenue - stressed_costs
    stressed_margin = (stressed_profit / stressed_revenue * 100) if stressed_revenue else -100

    revenue_change = ((stressed_revenue - base_revenue) / base_revenue * 100) if base_revenue else -100
    profit_change = ((stressed_profit - base_profit) / abs(base_profit) * 100) if base_profit != 0 else -100

    profit_component = clamp((stressed_profit / max(base_revenue, 1) + 0.5) * 100)
    revenue_component = clamp((stressed_revenue / max(base_revenue, 1)) * 100)
    continuity_component = clamp(100 - (technical_failure * 0.50 + productivity_loss * 0.40 + connectivity_effect * 0.60))
    margin_component = clamp(stressed_margin + 50)
    score = round(clamp(
        profit_component * 0.40 + revenue_component * 0.25 + continuity_component * 0.20 + margin_component * 0.15
    ), 1)

    if score >= 80:
        category = T("HIGH RESILIENCE", "ALTA RESILIENCIA")
        interpretation = T("The business model absorbs the simulated stress relatively well.", "El modelo de negocio absorbe relativamente bien el estrés simulado.")
    elif score >= 60:
        category = T("MODERATE RESILIENCE", "RESILIENCIA MODERADA")
        interpretation = T("The business remains viable, but some variables require corrective action.", "El negocio sigue siendo viable, pero algunas variables requieren acciones correctivas.")
    elif score >= 40:
        category = T("LOW RESILIENCE", "BAJA RESILIENCIA")
        interpretation = T("The stress produces significant deterioration. The model needs adaptation.", "El estrés produce un deterioro importante. El modelo necesita adaptación.")
    else:
        category = T("CRITICAL", "CRÍTICO")
        interpretation = T("The business model is highly vulnerable under the selected stress conditions.", "El modelo de negocio es muy vulnerable bajo las condiciones de estrés seleccionadas.")

    return locals()

# -----------------------------
# Header
# -----------------------------
st.title("☁️ MicroCloud-Edge")
st.subheader(T("Business Resilience Simulator", "Simulador de Resiliencia del Modelo de Negocio"))
st.caption(T(
    "Session 2 — Interactive simulation of internal and external business stress. Technology selected: Cloud and Edge Computing.",
    "Sesión 2 — Simulación interactiva del estrés interno y externo del negocio. Tecnología seleccionada: Computación en la Nube y en el Borde."
))

# -----------------------------
# Sidebar: business model
# -----------------------------
st.sidebar.header(T("1. Business model", "1. Modelo de negocio"))
customers = st.sidebar.number_input(T("Initial customers", "Clientes iniciales"), min_value=1, max_value=10000, value=20, step=1)
price = st.sidebar.number_input(T("Monthly subscription per customer (S/)", "Suscripción mensual por cliente (S/)"), min_value=1.0, max_value=5000.0, value=50.0, step=5.0)
fixed_costs = st.sidebar.number_input(T("Monthly fixed costs (S/)", "Costos fijos mensuales (S/)"), min_value=0.0, max_value=100000.0, value=400.0, step=50.0)
variable_cost = st.sidebar.number_input(T("Variable cost per customer (S/)", "Costo variable por cliente (S/)"), min_value=0.0, max_value=1000.0, value=10.0, step=1.0)

st.sidebar.header(T("2. External stress", "2. Estrés externo"))
demand_drop = st.sidebar.slider(T("Demand decrease (%)", "Disminución de la demanda (%)"), 0, 90, 20, 5)
competitor_pressure = st.sidebar.slider(T("Competitor pressure (%)", "Presión de competidores (%)"), 0, 80, 10, 5)
inflation = st.sidebar.slider(T("Inflation / input-cost pressure (%)", "Inflación / presión de costos de insumos (%)"), 0, 80, 10, 5)
connectivity = st.sidebar.slider(T("Connectivity disruption (%)", "Interrupción de conectividad (%)"), 0, 100, 20, 5)

st.sidebar.header(T("3. Internal stress", "3. Estrés interno"))
operating_cost_increase = st.sidebar.slider(T("Operating-cost increase (%)", "Aumento de costos operativos (%)"), 0, 100, 15, 5)
technical_failure = st.sidebar.slider(T("Technical failure impact (%)", "Impacto de fallas técnicas (%)"), 0, 80, 10, 5)
productivity_loss = st.sidebar.slider(T("Productivity loss (%)", "Pérdida de productividad (%)"), 0, 80, 10, 5)
support_increase = st.sidebar.slider(T("Support / maintenance increase (%)", "Aumento de soporte / mantenimiento (%)"), 0, 80, 10, 5)

st.sidebar.header(T("4. Cloud-Edge resilience assumption", "4. Supuesto de resiliencia Cloud-Edge"))
cloud_edge_advantage = st.sidebar.slider(
    T("Connectivity impact reduction from Edge (%)", "Reducción del impacto de conectividad por Edge (%)"),
    0, 100, 70, 5,
    help=T(
        "Simulation assumption: local Edge processing reduces the business impact of connectivity disruption. This value must later be validated with the physical prototype.",
        "Supuesto de simulación: el procesamiento local en Edge reduce el impacto empresarial de una interrupción de conectividad. Este valor deberá validarse posteriormente con el prototipo físico."
    )
)

# -----------------------------
# Presets
# -----------------------------
st.markdown(f"### {T('Scenario presets', 'Escenarios predefinidos')}")
preset_cols = st.columns(4)
if preset_cols[0].button(T("Normal", "Normal")): st.session_state["preset"] = "normal"
if preset_cols[1].button(T("Moderate Crisis", "Crisis Moderada")): st.session_state["preset"] = "moderate"
if preset_cols[2].button(T("Severe Crisis", "Crisis Severa")): st.session_state["preset"] = "severe"
if preset_cols[3].button(T("Custom", "Personalizado")): st.session_state["preset"] = "custom"
preset = st.session_state.get("preset", "moderate")

preset_values = {
    "normal": {"demand": 0, "competitor": 0, "inflation": 0, "connectivity": 0, "operating": 0, "technical": 0, "productivity": 0, "support": 0},
    "moderate": {"demand": 20, "competitor": 10, "inflation": 10, "connectivity": 20, "operating": 15, "technical": 10, "productivity": 10, "support": 10},
    "severe": {"demand": 50, "competitor": 30, "inflation": 30, "connectivity": 70, "operating": 40, "technical": 35, "productivity": 30, "support": 30},
}

if preset in preset_values:
    p = preset_values[preset]
    sim = simulate(customers, price, fixed_costs, variable_cost, p["demand"], p["competitor"], p["inflation"], p["connectivity"], p["operating"], p["technical"], p["productivity"], p["support"], cloud_edge_advantage)
    scenario_label = {"normal": T("Normal scenario", "Escenario normal"), "moderate": T("Moderate crisis", "Crisis moderada"), "severe": T("Severe crisis", "Crisis severa")}[preset]
else:
    sim = simulate(customers, price, fixed_costs, variable_cost, demand_drop, competitor_pressure, inflation, connectivity, operating_cost_increase, technical_failure, productivity_loss, support_increase, cloud_edge_advantage)
    scenario_label = T("Custom scenario", "Escenario personalizado")

st.info(f"**{T('Active scenario', 'Escenario activo')}:** {scenario_label}. {T('The model compares baseline performance with the selected stress conditions.', 'El modelo compara el desempeño base con las condiciones de estrés seleccionadas.')}")

# -----------------------------
# Results
# -----------------------------
st.markdown(f"## {T('Simulation result', 'Resultado de la simulación')}")
k1, k2, k3, k4 = st.columns(4)
k1.metric(T("Resilience score", "Puntaje de resiliencia"), f"{sim['score']}/100")
k2.metric(T("Stressed revenue", "Ingresos bajo estrés"), money(sim["stressed_revenue"]))
k3.metric(T("Stressed profit", "Utilidad bajo estrés"), money(sim["stressed_profit"]))
k4.metric(T("Stressed margin", "Margen bajo estrés"), f"{sim['stressed_margin']:.1f}%")
st.success(f"### {sim['category']}\n\n{sim['interpretation']}")

comparison = pd.DataFrame({
    T("Baseline", "Base"): [sim["base_revenue"], sim["base_costs"], sim["base_profit"], sim["base_margin"]],
    T("Stressed", "Bajo estrés"): [sim["stressed_revenue"], sim["stressed_costs"], sim["stressed_profit"], sim["stressed_margin"]],
}, index=[T("Revenue (S/)", "Ingresos (S/)"), T("Costs (S/)", "Costos (S/)"), T("Profit (S/)", "Utilidad (S/)"), T("Margin (%)", "Margen (%)")])
st.markdown(f"### {T('Baseline vs. stress', 'Base vs. estrés')}")
st.dataframe(comparison, use_container_width=True)

chart_data = pd.DataFrame({
    T("Baseline", "Base"): [sim["base_revenue"], sim["base_costs"], sim["base_profit"]],
    T("Stressed", "Bajo estrés"): [sim["stressed_revenue"], sim["stressed_costs"], sim["stressed_profit"]],
}, index=[T("Revenue", "Ingresos"), T("Costs", "Costos"), T("Profit", "Utilidad")])
st.bar_chart(chart_data)

# -----------------------------
# Interpretation
# -----------------------------
st.markdown(f"### {T('Business interpretation', 'Interpretación del negocio')}")
left, right = st.columns(2)
external = p if preset in preset_values else {"demand": demand_drop, "competitor": competitor_pressure, "inflation": inflation, "connectivity": connectivity}
internal = p if preset in preset_values else {"operating": operating_cost_increase, "technical": technical_failure, "productivity": productivity_loss, "support": support_increase}
with left:
    st.write(f"**{T('External stress impact', 'Impacto del estrés externo')}**")
    st.write(f"- {T('Demand decrease', 'Disminución de demanda')}: {external['demand']}%")
    st.write(f"- {T('Competitor pressure', 'Presión de competidores')}: {external['competitor']}%")
    st.write(f"- {T('Inflation pressure', 'Presión inflacionaria')}: {external['inflation']}%")
    st.write(f"- {T('Connectivity disruption', 'Interrupción de conectividad')}: {external['connectivity']}%")
with right:
    st.write(f"**{T('Internal stress impact', 'Impacto del estrés interno')}**")
    st.write(f"- {T('Operating-cost increase', 'Aumento de costos operativos')}: {internal['operating']}%")
    st.write(f"- {T('Technical failure impact', 'Impacto de fallas técnicas')}: {internal['technical']}%")
    st.write(f"- {T('Productivity loss', 'Pérdida de productividad')}: {internal['productivity']}%")
    st.write(f"- {T('Support/maintenance increase', 'Aumento de soporte/mantenimiento')}: {internal['support']}%")

st.markdown(f"### {T('Key decision signals', 'Señales clave para la decisión')}")
signals = []
if sim["stressed_profit"] < 0:
    signals.append(T("⚠️ The business becomes unprofitable under the selected stress.", "⚠️ El negocio deja de ser rentable bajo el estrés seleccionado."))
elif sim["stressed_profit"] < sim["base_profit"]:
    signals.append(T("⚠️ Profit decreases under stress; cost and demand management are priorities.", "⚠️ La utilidad disminuye bajo estrés; gestionar costos y demanda es prioritario."))
if sim["revenue_change"] <= -30:
    signals.append(T("⚠️ Revenue retention is weak; customer acquisition and retention need attention.", "⚠️ La retención de ingresos es débil; se debe prestar atención a la captación y retención de clientes."))
if sim["stressed_margin"] < 15:
    signals.append(T("⚠️ The stressed margin is low; review pricing and variable costs.", "⚠️ El margen bajo estrés es reducido; revise precios y costos variables."))
if connectivity > 0 and cloud_edge_advantage > 0:
    signals.append(T("☁️ Edge computing is modeled as a resilience mechanism that reduces the business impact of connectivity disruption.", "☁️ Edge Computing se modela como un mecanismo de resiliencia que reduce el impacto empresarial de una interrupción de conectividad."))
if not signals:
    signals.append(T("✅ The model remains comparatively stable under the selected scenario.", "✅ El modelo se mantiene relativamente estable bajo el escenario seleccionado."))
for signal in signals: st.write(signal)

st.caption(T(
    "Important: the resilience score is a management simulation, not a scientific forecast. The Cloud-Edge connectivity benefit is an explicit assumption that should be validated later using the project's physical prototype and measured indicators.",
    "Importante: el puntaje de resiliencia es una simulación de gestión, no un pronóstico científico. El beneficio de Cloud-Edge sobre la conectividad es un supuesto explícito que deberá validarse posteriormente mediante el prototipo físico y métricas medidas."
))

with st.expander(T("Simulation methodology", "Metodología de la simulación")):
    st.write(T(
        "The simulator establishes a baseline from customers, price, fixed costs and variable costs. It then applies internal and external stress factors and compares the resulting revenue, costs, profit and margin with the baseline.",
        "El simulador establece una línea base a partir de clientes, precio, costos fijos y costos variables. Luego aplica factores de estrés internos y externos y compara los ingresos, costos, utilidad y margen resultantes con la línea base."
    ))
    st.write(T(
        "The resilience score combines four dimensions: financial performance (40%), revenue retention (25%), operational continuity (20%) and stressed margin (15%).",
        "El puntaje de resiliencia combina cuatro dimensiones: desempeño financiero (40%), retención de ingresos (25%), continuidad operativa (20%) y margen bajo estrés (15%)."
    ))
    st.write(T(
        "For the Cloud-Edge business model, connectivity disruption can be partially mitigated by local Edge processing. The percentage selected by the user is a modeling assumption and must not be presented as a measured technical result.",
        "Para el modelo de negocio Cloud-Edge, una interrupción de conectividad puede mitigarse parcialmente mediante procesamiento local en Edge. El porcentaje seleccionado por el usuario es un supuesto de modelamiento y no debe presentarse como un resultado técnico medido."
    ))

st.markdown("---")
st.caption(T("MicroCloud-Edge — Management by Results | Session 2", "MicroCloud-Edge — Gestión por Resultados | Sesión 2"))
