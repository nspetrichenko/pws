import time

def time_this(NUM_RUNS=10):
    def decorator(function):
        def func(*args, **kwargs):
            avg = 0
            for i in range(NUM_RUNS):
                t0 = time.time()
                function(*args, **kwargs)
                t1 = time.time()
                avg += (t1 - t0)
            avg /= NUM_RUNS
            print("%s запусков. Среднее время выполнения %s за : %.5f секунд" % (NUM_RUNS, function.__name__, avg))
        return func

    return decorator

@time_this()
def f():
    for j in range(1000000):
        pass
f()
