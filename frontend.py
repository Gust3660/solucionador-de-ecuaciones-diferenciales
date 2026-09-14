"""Interfaz Streamlit para comparar soluciones numéricas de EDO."""

from __future__ import annotations

import matplotlib.pyplot as plt
import streamlit as st

from backend import solve_ode


st.set_page_config(page_title="Solucionador de EDO", page_icon="∫", layout="wide")
st.title("Solucionador de ecuaciones diferenciales")
st.write("Compara métodos numéricos con soluciones exactas en ejemplos de ecuaciones diferenciales ordinarias.")

with st.sidebar:
    example = st.selectbox("Ecuación", ["Decaimiento: y' = -k y", "Logística: y' = r y (1-y/K)", "Forzada: y' = A cos(ωt)"])
    method = st.selectbox("Método", ["RK4", "Heun", "Euler"])
    y0 = st.number_input("Condición inicial y₀", min_value=0.01, value=10.0, step=1.0)
    duration = st.number_input("Tiempo final", min_value=0.1, value=10.0, step=1.0)
    steps = st.slider("Pasos de integración", 20, 5000, 500, 20)
    if example.startswith("Decaimiento"):
        params = {"k": st.number_input("Tasa k", min_value=0.0, value=0.4, step=0.1)}
    elif example.startswith("Logística"):
        params = {"r": st.number_input("Tasa r", min_value=0.01, value=0.6, step=0.1),
                  "K": st.number_input("Capacidad K", min_value=0.1, value=100.0, step=10.0)}
    else:
        params = {"A": st.number_input("Amplitud A", value=2.0, step=0.5),
                  "omega": st.number_input("Frecuencia ω", min_value=0.01, value=1.0, step=0.1)}

try:
    result = solve_ode(example, y0, duration, steps, params, method)
except ValueError as error:
    st.error(str(error))
    st.stop()

st.metric("Error absoluto máximo frente a solución exacta", f"{result.max_error:.6g}")
fig, axis = plt.subplots(figsize=(10, 5))
axis.plot(result.times, result.exact, label="Solución exacta", linewidth=2)
axis.plot(result.times, result.numeric, "--", label=f"{method}")
axis.set(title=example, xlabel="Tiempo t", ylabel="y(t)")
axis.grid(True, alpha=0.3)
axis.legend()
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)
st.caption("Reduce el tamaño del paso para observar cómo cambia el error numérico.")
