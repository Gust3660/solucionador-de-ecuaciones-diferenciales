# Solucionador de ecuaciones diferenciales

Aplicación Streamlit para resolver ejemplos de ecuaciones diferenciales ordinarias escalares y comparar Euler, Heun y Runge-Kutta de cuarto orden con una solución analítica.

## Ejemplos incluidos

- Decaimiento `y' = -ky`.
- Crecimiento logístico `y' = ry(1-y/K)`.
- Ecuación forzada `y' = A cos(ωt)`.

La app grafica ambas soluciones y reporta el error absoluto máximo en el intervalo.

## Estructura

```text
.
├── backend.py       # Integradores y soluciones de referencia
├── frontend.py      # Interfaz Streamlit y gráfica
├── requirements.txt
└── README.md
```

## Instalación y ejecución

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run frontend.py
```

En macOS o Linux, activa el entorno con `source .venv/bin/activate`.

## Uso

Elige la ecuación, el método y sus parámetros en la barra lateral. Ajusta el tiempo final y los pasos; una malla más fina suele reducir el error, aunque aumenta el cálculo.
