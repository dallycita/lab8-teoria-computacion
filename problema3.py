from medicion import medir, hacer_profiling


def function(n):
    for i in range(1, n // 3 + 1):
        for j in range(1, n + 1, 4):
            print("Sequence")


def contar_operaciones(n):
    # floor(n/3) * ceil(n/4)
    return (n // 3) * ((n + 3) // 4)


if __name__ == "__main__":
    print("Problema 3")
    medir(function, "problema3", contar_operaciones)
    hacer_profiling(function, 1000, "problema3")
