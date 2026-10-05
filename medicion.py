import contextlib
import cProfile
import csv
import os
import pstats
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

VALORES_N = [1, 10, 100, 1000, 10000, 100000, 1000000]

# Si una corrida tarda más que esto, no se ejecutan los n siguientes:
# cada n es 10 veces más grande, así que tardarían al menos 10 veces más.
LIMITE_SEGUNDOS = 3


def tomar_tiempo(funcion, n):
    # Los prints se mandan a devnull para medir el algoritmo y no la consola
    with open(os.devnull, "w") as nulo, contextlib.redirect_stdout(nulo):
        inicio = time.perf_counter()
        funcion(n)
        fin = time.perf_counter()
    return fin - inicio


def medir(funcion, nombre, contar_operaciones):
    resultados = []
    saltar = False
    ultimo_n, ultimo_tiempo = None, None

    for n in VALORES_N:
        if saltar:
            # se estima escalando el último tiempo medido por la razón de
            # operaciones que da la fórmula de la parte a
            tiempo = ultimo_tiempo * contar_operaciones(n) / contar_operaciones(ultimo_n)
            print(f"n = {n:>8}  ->  {tiempo:.3e} s  (estimado, no se ejecutó)")
            resultados.append((n, tiempo, "estimado"))
            continue

        # para n chicos el tiempo es muy pequeño y ruidoso, así que se promedia
        repeticiones = 5 if n <= 1000 else 1
        total = 0
        for _ in range(repeticiones):
            total += tomar_tiempo(funcion, n)
        tiempo = total / repeticiones

        print(f"n = {n:>8}  ->  {tiempo:.3e} s")
        resultados.append((n, tiempo, "medido"))
        ultimo_n, ultimo_tiempo = n, tiempo

        if tiempo > LIMITE_SEGUNDOS:
            saltar = True

    guardar_csv(resultados, nombre)
    hacer_grafica(resultados, nombre)
    return resultados


def guardar_csv(resultados, nombre):
    with open(f"resultados/{nombre}.csv", "w", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["n", "tiempo_segundos", "tipo"])
        for n, tiempo, tipo in resultados:
            writer.writerow([n, f"{tiempo:.3e}", tipo])


def hacer_grafica(resultados, nombre):
    ns = [n for n, t, tipo in resultados]
    tiempos = [t for n, t, tipo in resultados]
    medidos = [(n, t) for n, t, tipo in resultados if tipo == "medido"]
    estimados = [(n, t) for n, t, tipo in resultados if tipo == "estimado"]

    plt.figure()
    plt.plot(ns, tiempos, color="tab:blue")
    plt.plot([n for n, t in medidos], [t for n, t in medidos], "o",
             color="tab:blue", label="medido")
    if estimados:
        plt.plot([n for n, t in estimados], [t for n, t in estimados], "o",
                 markerfacecolor="white", color="tab:blue", label="estimado (no se ejecutó)")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Tamaño de input (n)")
    plt.ylabel("Tiempo (s)")
    plt.title(f"Problema {nombre[-1]}: tamaño de input vs. tiempo")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.savefig(f"resultados/{nombre}.png", dpi=120)
    plt.close()


def hacer_profiling(funcion, n, nombre):
    perfil = cProfile.Profile()
    with open(os.devnull, "w") as nulo, contextlib.redirect_stdout(nulo):
        perfil.enable()
        funcion(n)
        perfil.disable()

    with open(f"resultados/{nombre}_profile.txt", "w") as archivo:
        archivo.write(f"cProfile de {nombre} con n = {n}\n\n")
        stats = pstats.Stats(perfil, stream=archivo)
        stats.sort_stats("cumulative").print_stats(10)

    print(f"Profiling guardado en resultados/{nombre}_profile.txt")
