import threading
import time
import inspect
import ctypes
 
 
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
 
def stop_thread(thread):
    for i in range(7):
        _async_raise(thread.ident, SystemExit)
 
 
def test():
    while True:
        print('-------')
        time.sleep(1)
 
 
if __name__ == "__main__":
    t = threading.Thread(target=test)
    t.start()
    time.sleep(5)
    print("main thread sleep finish")
    stop_thread(t)
