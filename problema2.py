from medicion import medir, hacer_profiling


def function(n):
    if n <= 1:
        return
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            print("Sequence")
            break


if __name__ == "__main__":
    print("Problema 2")
    medir(function, "problema2")
    hacer_profiling(function, 10000, "problema2")
