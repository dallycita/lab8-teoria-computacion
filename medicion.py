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


def medir(funcion, nombre):
    resultados = []
    saltar = False

    for n in VALORES_N:
        if saltar:
            print(f"n = {n:>8}  ->  no ejecutado (excede el límite de tiempo)")
            resultados.append((n, None))
            continue

        # para n chicos el tiempo es muy pequeño y ruidoso, así que se promedia
        repeticiones = 5 if n <= 1000 else 1
        total = 0
        for _ in range(repeticiones):
            total += tomar_tiempo(funcion, n)
        tiempo = total / repeticiones

        print(f"n = {n:>8}  ->  {tiempo:.6f} s")
        resultados.append((n, tiempo))

        if tiempo > LIMITE_SEGUNDOS:
            saltar = True

    guardar_csv(resultados, nombre)
    hacer_grafica(resultados, nombre)
    return resultados


def guardar_csv(resultados, nombre):
    with open(f"resultados/{nombre}.csv", "w", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["n", "tiempo_segundos"])
        for n, tiempo in resultados:
            writer.writerow([n, f"{tiempo:.6f}" if tiempo is not None else "no ejecutado"])


def hacer_grafica(resultados, nombre):
    ns = [n for n, t in resultados if t is not None]
    tiempos = [t for n, t in resultados if t is not None]

    plt.figure()
    plt.plot(ns, tiempos, marker="o")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Tamaño de input (n)")
    plt.ylabel("Tiempo (s)")
    plt.title(f"{nombre}: tamaño de input vs. tiempo")
    plt.grid(True, which="both", alpha=0.3)
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
