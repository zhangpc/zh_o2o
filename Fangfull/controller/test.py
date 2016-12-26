
import os
import time
import threading

# 进程函数
def printthread(n):

    print (n,"-->进程创建")
    for a in range(4):
        print (a)
        time.sleep(1)
    print (n,"-->进程结束")
    sem.release()


if __name__ =='__main__':

    maxThread=5
    #
    sem=threading.BoundedSemaphore(maxThread)

    for a in range(12):

        sem.acquire()
        threading.Thread(target=printthread,args=(a,)).start()

    # print ("All thread has create,Wait for all thread exit.")
    #
    # for a in range(maxThread):
    #     sem.acquire();
    #
    # print ("All thread exit")