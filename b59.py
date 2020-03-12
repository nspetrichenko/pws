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

@time_this(2)
def f():
    for j in range(1000000):
        pass
f()
