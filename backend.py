"""Solución numérica de EDO escalares y soluciones analíticas de referencia."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass(frozen=True)
class ODEResult:
    times: np.ndarray
    numeric: np.ndarray
    exact: np.ndarray
    max_error: float


def solve_ode(example: str, y0: float, duration: float, steps: int,
              params: dict[str, float], method: str = "RK4") -> ODEResult:
    if y0 <= 0 or duration <= 0 or steps < 2:
        raise ValueError("y₀ y la duración deben ser positivos; se requieren al menos 2 pasos.")
    if method not in {"Euler", "Heun", "RK4"}:
        raise ValueError("Método de integración desconocido.")
    if example == "Decaimiento: y' = -k y":
        k = params["k"]
        derivative = lambda t, y: -k * y
        exact_fn = lambda t: y0 * np.exp(-k * t)
    elif example == "Logística: y' = r y (1-y/K)":
        rate, capacity = params["r"], params["K"]
        if capacity <= y0 or rate <= 0:
            raise ValueError("Para el ejemplo logístico, K debe superar y₀ y r debe ser positiva.")
        derivative = lambda t, y: rate * y * (1 - y / capacity)
        exact_fn = lambda t: capacity / (1 + ((capacity - y0) / y0) * np.exp(-rate * t))
    elif example == "Forzada: y' = A cos(ωt)":
        amplitude, omega = params["A"], params["omega"]
        derivative = lambda t, y: amplitude * np.cos(omega * t)
        exact_fn = lambda t: y0 + amplitude / omega * np.sin(omega * t)
    else:
        raise ValueError("Selecciona una EDO disponible.")

    times = np.linspace(0, duration, steps + 1)
    values = np.empty(steps + 1, dtype=float)
    values[0] = y0
    h = duration / steps
    for index in range(steps):
        t, y = times[index], values[index]
        k1 = derivative(t, y)
        if method == "Euler":
            values[index + 1] = y + h * k1
        elif method == "Heun":
            k2 = derivative(t + h, y + h * k1)
            values[index + 1] = y + h * (k1 + k2) / 2
        else:
            k2 = derivative(t + h / 2, y + h * k1 / 2)
            k3 = derivative(t + h / 2, y + h * k2 / 2)
            k4 = derivative(t + h, y + h * k3)
            values[index + 1] = y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    exact = exact_fn(times)
    if not np.all(np.isfinite(values)):
        raise ValueError("La solución numérica diverge; reduce el paso o cambia los parámetros.")
    return ODEResult(times, values, exact, float(np.max(np.abs(values - exact))))
