#!/usr/bin/python

import time
import multiprocessing

def fib(n):
    if n < 0:
        raise ValueError
    if n < 2:
        return n
    return fib(n-1)+fib(n-2)

def fibonacci(in_queue, out_queue):
    while True:
        n = in_queue.get()
        if n == None:
            break
        start = time.time()
        res = fib(n)
        end = time.time()
        out_queue.put((n, res, end-start))
    out_queue.put((None, None, None))

def main():
    start = time.time()
    in_queue = multiprocessing.Queue()
    out_queue = multiprocessing.Queue()

    process_num = multiprocessing.cpu_count()
    for _ in range(process_num):
        multiprocessing.Process(target=fibonacci,
                                args=(in_queue, out_queue)).start()

    for i in range(30, 37):
        in_queue.put(i)
    for _ in range(process_num):
        in_queue.put(None)

    while True:
        n, res, spend_time = out_queue.get()
        if n == None:
            process_num -= 1
            if process_num == 0: break
        else:
            print "fib(%3d) = %7d   (took %0.3fs)" % ( n, res, spend_time)

    end = time.time()
    print "Total time: %0.3fs" % (end - start)

if __name__ == "__main__":
    main()