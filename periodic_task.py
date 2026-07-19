"""periodic task scheduler"""
import logging
import threading

class PeriodicTask:
    def __init__(self,event_loop,interval,
    callback,*callback_args,**callback_kwargs):
        self.loop = event_loop.loop 
        self.interval = interval
        self.callback = callback
        self.event_loop_thread = event_loop.thread
        self.callback_args = callback_args
        self.callback_kwargs = callback_kwargs
        
    def start(self):
        current_thread = threading.current_thread()
        if current_thread == self.event_loop_thread:
            self.loop.call_later(self.interval,
            self.do_later)
            logging.info("Same thread,scheduling event")
        else:
            self.loop.call_soon_threadsafe(
            lambda:self.loop.call_later(self.interval,
            self.do_later))
            logging.info("Different threads,scheduling event")
            
    def do_later(self):
        self.loop.call_soon(self.start)
        self.callback(*self.callback_args, **self.callback_kwargs)
        logging.info("Executing scheduled task")
            

def test(*args,**kwargs):
    print(args)
    print(kwargs)  
def test2():
    print("we are in executor")

if __name__ == "__main__":
    import log
    import logging
    import signal
    from thread_manager import ThreadManager
    from loop_manager import LoopManager
    
    logger = logging.getLogger(__name__)

    thread = ThreadManager()
    event_loop = LoopManager()
    stop_event = threading.Event()
    thread.start(event_loop.run_loop)
    def handle(signal,frame):
        stop_event.set()
        logger.info("Stop signal received")
        
    signal.signal(signal.SIGINT,handle)
    
    PeriodicTask(event_loop,5,test,908).start()
    while not stop_event.is_set():
        stop_event.wait(timeout=5)
        pass
    else:
        event_loop.submit_task(
        "stop_loop",event_loop.stop)
        thread.shutdown()
    
 