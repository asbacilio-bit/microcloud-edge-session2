import streamlit as st
import pandas as pd

st.set_page_config(page_title="MicroCloud-Edge | Business Resilience Simulator", page_icon="☁️", layout="wide")

# ---------- Language ----------
st.sidebar.header("🌐 Language / Idioma")
language = st.sidebar.radio("Choose / Elegir", ["English", "Español"], horizontal=True)
es = language == "Español"
def T(en, es_text): return es_text if es else en

def money(x): return f"S/ {x:,.2f}"
def clamp(x, lo=0, hi=100): return max(lo, min(hi, x))

def simulate(c,p,f,v,d,cmp,inf,conn,op,tech,prod,sup,edge):
    br=c*p; bc=f+c*v; bp=br-bc; bm=(bp/br*100) if br else 0
    demand=clamp(d+cmp*.5,0,95); conn_effect=conn*(1-edge/100)
    sc=max(0,c*(1-demand/100-tech*.20/100-prod*.25/100))
    sp=p*max(.5,1-inf*.20/100); sr=sc*sp
    svc=sc*v; costs=f*(1+op/100)+svc*(1+inf/100)+sr*(sup/100)
    sr*=max(.5,1-conn_effect*.25/100); profit=sr-costs
    margin=(profit/sr*100) if sr else -100
    rev_change=((sr-br)/br*100) if br else -100
    pc=clamp((profit/max(br,1)+.5)*100); rc=clamp(sr/max(br,1)*100)
    cc=clamp(100-(tech*.5+prod*.4+conn_effect*.6)); mc=clamp(margin+50)
    score=round(clamp(pc*.4+rc*.25+cc*.2+mc*.15),1)
    if score>=80: cat,interp=T("HIGH RESILIENCE","ALTA RESILIENCIA"),T("The business model absorbs the simulated stress relatively well.","El modelo de negocio absorbe relativamente bien el estrés simulado.")
    elif score>=60: cat,interp=T("MODERATE RESILIENCE","RESILIENCIA MODERADA"),T("The business remains viable, but some variables require corrective action.","El negocio sigue siendo viable, pero algunas variables requieren acciones correctivas.")
    elif score>=40: cat,interp=T("LOW RESILIENCE","BAJA RESILIENCIA"),T("The stress produces significant deterioration. The model needs adaptation.","El estrés produce un deterioro importante. El modelo necesita adaptación.")
    else: cat,interp=T("CRITICAL","CRÍTICO"),T("The business model is highly vulnerable under the selected stress conditions.","El modelo de negocio es muy vulnerable bajo las condiciones seleccionadas.")
    return locals()

# ---------- Business model ----------
st.sidebar.header(T("1. Business model","1. Modelo de negocio"))
customers=st.sidebar.number_input(T("Initial customers","Clientes iniciales"),1,10000,20,1)
price=st.sidebar.number_input(T("Monthly subscription per customer (S/)","Suscripción mensual por cliente (S/)"),1.0,5000.0,50.0,5.0)
fixed=st.sidebar.number_input(T("Monthly fixed costs (S/)","Costos fijos mensuales (S/)"),0.0,100000.0,400.0,50.0)
variable=st.sidebar.number_input(T("Variable cost per customer (S/)","Costo variable por cliente (S/)"),0.0,1000.0,10.0,1.0)

# ---------- Scenario ----------
st.sidebar.header(T("Scenario","Escenario"))
scenario_names=[T("Normal","Normal"),T("Moderate Crisis","Crisis Moderada"),T("Severe Crisis","Crisis Severa"),T("Custom","Personalizado")]
scenario=st.sidebar.selectbox(T("Select a scenario","Selecciona un escenario"),scenario_names,index=1)

presets={
    "normal":{"d":0,"cmp":0,"inf":0,"conn":0,"op":0,"tech":0,"prod":0,"sup":0},
    "moderate":{"d":20,"cmp":10,"inf":10,"conn":20,"op":15,"tech":10,"prod":10,"sup":10},
    "severe":{"d":50,"cmp":30,"inf":30,"conn":70,"op":40,"tech":35,"prod":30,"sup":30},
}
key={scenario_names[0]:"normal",scenario_names[1]:"moderate",scenario_names[2]:"severe",scenario_names[3]:"custom"}[scenario]

# The selected scenario now provides starting values, but EVERY stress variable remains editable.
def scenario_default(name, field, custom_default):
    if key == "custom":
        return custom_default
    return presets[key][field]

# ---------- External stress ----------
st.sidebar.header(T("2. External stress","2. Estrés externo"))
demand=st.sidebar.slider(T("Demand decrease (%)","Disminución de la demanda (%)"),0,90,scenario_default("d","d",20),5,key=f"demand_{key}")
competitor=st.sidebar.slider(T("Competitor pressure (%)","Presión de competidores (%)"),0,80,scenario_default("cmp","cmp",10),5,key=f"competitor_{key}")
inflation=st.sidebar.slider(T("Inflation / input-cost pressure (%)","Inflación / presión de costos (%)"),0,80,scenario_default("inf","inf",10),5,key=f"inflation_{key}")
connectivity=st.sidebar.slider(T("Connectivity disruption (%)","Interrupción de conectividad (%)"),0,100,scenario_default("conn","conn",20),5,key=f"connectivity_{key}")

# ---------- Internal stress ----------
st.sidebar.header(T("3. Internal stress","3. Estrés interno"))
operating=st.sidebar.slider(T("Operating-cost increase (%)","Aumento de costos operativos (%)"),0,100,scenario_default("op","op",15),5,key=f"operating_{key}")
technical=st.sidebar.slider(T("Technical failure impact (%)","Impacto de fallas técnicas (%)"),0,80,scenario_default("tech","tech",10),5,key=f"technical_{key}")
productivity=st.sidebar.slider(T("Productivity loss (%)","Pérdida de productividad (%)"),0,80,scenario_default("prod","prod",10),5,key=f"productivity_{key}")
support=st.sidebar.slider(T("Support / maintenance increase (%)","Aumento de soporte / mantenimiento (%)"),0,80,scenario_default("sup","sup",10),5,key=f"support_{key}")

# ---------- Cloud-Edge resilience assumption ----------
st.sidebar.header(T("4. Cloud-Edge resilience assumption","4. Supuesto de resiliencia Cloud-Edge"))
edge=st.sidebar.slider(T("Connectivity impact reduction from Edge (%)","Reducción del impacto de conectividad por Edge (%)"),0,100,70,5)

sim=simulate(customers,price,fixed,variable,demand,competitor,inflation,connectivity,operating,technical,productivity,support,edge)

# ---------- Main ----------
st.title("☁️ MicroCloud-Edge")
st.subheader(T("Business Resilience Simulator","Simulador de Resiliencia del Modelo de Negocio"))
st.caption(T("Session 2 — Interactive simulation of internal and external business stress. Technology selected: Cloud and Edge Computing.","Sesión 2 — Simulación interactiva del estrés interno y externo del negocio. Tecnología seleccionada: Computación en la Nube y en el Borde."))
st.info(f"**{T('Active scenario','Escenario activo')}:** {scenario}. {T('The scenario provides starting values, but all stress parameters can be modified manually.','El escenario proporciona valores iniciales, pero todos los parámetros de estrés pueden modificarse manualmente.')}")

st.markdown(f"## {T('Simulation result','Resultado de la simulación')}")
a,b,c,d=st.columns(4)
a.metric(T("Resilience score","Puntaje de resiliencia"),f"{sim['score']}/100")
b.metric(T("Stressed revenue","Ingresos bajo estrés"),money(sim["sr"]))
c.metric(T("Stressed profit","Utilidad bajo estrés"),money(sim["profit"]))
d.metric(T("Stressed margin","Margen bajo estrés"),f"{sim['margin']:.1f}%")
st.success(f"### {sim['cat']}\n\n{sim['interp']}")

comparison=pd.DataFrame({T("Baseline","Base"):[sim["br"],sim["bc"],sim["bp"],sim["bm"]],T("Stressed","Bajo estrés"):[sim["sr"],sim["costs"],sim["profit"],sim["margin"]]},index=[T("Revenue (S/)","Ingresos (S/)"),T("Costs (S/)","Costos (S/)"),T("Profit (S/)","Utilidad (S/)"),T("Margin (%)","Margen (%)")])
st.markdown(f"### {T('Baseline vs. stress','Base vs. estrés')}")
st.dataframe(comparison,use_container_width=True)
chart=pd.DataFrame({T("Baseline","Base"):[sim["br"],sim["bc"],sim["bp"]],T("Stressed","Bajo estrés"):[sim["sr"],sim["costs"],sim["profit"]]},index=[T("Revenue","Ingresos"),T("Costs","Costos"),T("Profit","Utilidad")])
st.bar_chart(chart)

st.markdown(f"### {T('Scenario parameters','Parámetros del escenario')}")
p1,p2=st.columns(2)
with p1:
    st.write(f"**{T('External stress','Estrés externo')}**")
    st.write(f"• {T('Demand decrease','Disminución de demanda')}: {demand}%")
    st.write(f"• {T('Competitor pressure','Presión de competidores')}: {competitor}%")
    st.write(f"• {T('Inflation','Inflación')}: {inflation}%")
    st.write(f"• {T('Connectivity disruption','Interrupción de conectividad')}: {connectivity}%")
with p2:
    st.write(f"**{T('Internal stress','Estrés interno')}**")
    st.write(f"• {T('Operating-cost increase','Aumento de costos operativos')}: {operating}%")
    st.write(f"• {T('Technical failure impact','Impacto de fallas técnicas')}: {technical}%")
    st.write(f"• {T('Productivity loss','Pérdida de productividad')}: {productivity}%")
    st.write(f"• {T('Support / maintenance increase','Aumento de soporte / mantenimiento')}: {support}%")

st.markdown(f"### {T('Key decision signals','Señales clave para la decisión')}")
if sim["profit"]<0: st.write(T("⚠️ The business becomes unprofitable under this scenario.","⚠️ El negocio deja de ser rentable bajo este escenario."))
elif sim["profit"]<sim["bp"]: st.write(T("⚠️ Profit decreases under stress; review costs and demand.","⚠️ La utilidad disminuye bajo estrés; revise costos y demanda."))
if sim["rev_change"]<=-30: st.write(T("⚠️ Revenue retention is weak.","⚠️ La retención de ingresos es débil."))
if sim["margin"]<15: st.write(T("⚠️ Stressed margin is low; review pricing and variable costs.","⚠️ El margen bajo estrés es reducido; revise precios y costos variables."))
if connectivity>0 and edge>0: st.write(T("☁️ Edge computing is modeled as a mechanism that reduces the business impact of connectivity disruption.","☁️ Edge Computing se modela como un mecanismo que reduce el impacto empresarial de una interrupción de conectividad."))

with st.expander(T("Simulation methodology","Metodología de la simulación")):
    st.write(T("The simulator establishes a baseline and then applies internal and external stress factors. The resilience score combines financial performance (40%), revenue retention (25%), operational continuity (20%) and stressed margin (15%).","El simulador establece una línea base y luego aplica factores de estrés internos y externos. El puntaje de resiliencia combina desempeño financiero (40%), retención de ingresos (25%), continuidad operativa (20%) y margen bajo estrés (15%)."))
    st.write(T("The Cloud-Edge benefit is a modeling assumption and must later be validated with measured results from the physical prototype.","El beneficio de Cloud-Edge es un supuesto de modelamiento y deberá validarse posteriormente con resultados medidos del prototipo físico."))

st.markdown("---")
st.caption(T("MicroCloud-Edge — Management by Results | Session 2","MicroCloud-Edge — Gestión por Resultados | Sesión 2"))
