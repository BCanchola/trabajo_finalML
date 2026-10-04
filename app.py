import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Executive Customer Analytics Dashboard", layout="wide")

# Cargar datos generados por el Pipeline
@st.cache_data
def load_data():
    return pd.read_csv('pipeline_output_customers.csv')

try:
    df = load_data()
    
    st.title("📊 Executive Customer Analytics & MLOps Dashboard")
    st.markdown("Plataforma interactiva de monitoreo estratégico de segmentos, anomalías y simulación de ROI.")

    # Métricas Top Level (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Clientes", f"{len(df):,}")
    col2.metric("Ingresos Totales", f"${df['Monetario'].sum():,.2f}")
    col3.metric("Ticket Promedio", f"${df['Monetario'].mean():,.2f}")
    col4.metric("Clientes Atípicos", f"{len(df[df['Es_Atipico'] == 'Atípico']):,}")

    st.divider()

    # Simulador de Escenarios de Negocio
    st.sidebar.header("🎛️ Simulador de Impacto de Marketing")
    inversion = st.sidebar.slider("Inversión en Retención ($)", 1000, 50000, 10000, step=1000)
    mejora_retencion = st.sidebar.slider("% Mejora en Retención de Clientes en Riesgo", 1, 30, 10)

    clientes_riesgo = df[df['Segmento'] == 'En Riesgo']
    ingreso_recuperado = (clientes_riesgo['Monetario'].sum() * (mejora_retencion / 100))
    roi_estimado = ((ingreso_recuperado - inversion) / inversion) * 100

    st.sidebar.markdown("### 📈 Resultado de la Simulación")
    st.sidebar.metric("Ingreso Adicional Estimado", f"${ingreso_recuperado:,.2f}")
    st.sidebar.metric("ROI Estimado de Campaña", f"{roi_estimado:.1f}%")

    # Gráficos Principales
    c1, c2 = st.columns(2)

    with c1:
        fig_pie = px.pie(df, names='Segmento', values='Monetario', title="Distribución de Ingresos por Segmento")
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        fig_scatter = px.scatter(df, x='PC1', y='PC2', color='Segmento', size='Monetario', title="Espacio Multidimensional (PCA)")
        st.plotly_chart(fig_scatter, use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar 'pipeline_output_customers.csv'. Ejecuta primero el pipeline en tu cuaderno. Detalle: {e}")
