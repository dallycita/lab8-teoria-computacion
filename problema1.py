from medicion import medir, hacer_profiling


def function(n):
    counter = 0
    for i in range(n // 2, n + 1):
        for j in range(1, n - n // 2 + 1):  # equivale a j + n/2 <= n
            k = 1
            while k <= n:  # range no permite multiplicar el paso
                counter += 1
                k = k * 2
    return counter


if __name__ == "__main__":
    print("Problema 1")
    medir(function, "problema1")
    hacer_profiling(function, 1000, "problema1")
