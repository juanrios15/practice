from multiprocessing import Pool
import time

N = 5000000

def cube(x):
    res = []
    for y in range(5000000):
        res.append(y)
    print(x)

if __name__ == "__main__":
    # first way, using multiprocessing
    start_time = time.perf_counter()
    with Pool() as pool:
      result = pool.map(cube, range(1,100))
    finish_time = time.perf_counter()
    print("Program finished in {} seconds - using multiprocessing".format(finish_time-start_time))
    print("---")
    # second way, serial computation
    start_time = time.perf_counter()
    result = []
    for x in range(1,100):
      result.append(cube(x))
    finish_time = time.perf_counter()
    print("Program finished in {} seconds".format(finish_time-start_time))