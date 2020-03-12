import time

def time_this(RUNS=10):
    def decorator(function):
        def func(*args, **kwargs):
            avg = 0
            for i in range(RUNS):
                t0 = time.time()
                function(*args, **kwargs)
                t1 = time.time()
                avg += (t1 - t0)
            avg /= RUNS
            print("%s запусков. Среднее время выполнения %s за : %.5f секунд" % (RUNS, function.__name__, avg))
        return func

    return decorator

@time_this(3)
def fib(N):
    a = 1
    b = 2
    sq = [1]
    for i in range(1, N):
        res = a + b
        a = b
        b = res
        sq.append(a)
    return sq
fib(100_000)
