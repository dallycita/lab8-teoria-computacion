from medicion import medir, hacer_profiling


def function(n):
    for i in range(1, n // 3 + 1):
        for j in range(1, n + 1, 4):
            print("Sequence")


if __name__ == "__main__":
    print("Problema 3")
    medir(function, "problema3")
    hacer_profiling(function, 1000, "problema3")
