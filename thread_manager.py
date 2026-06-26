"""Wrapper over threading so that i get errors in
worker threads visible in main"""

from concurrent.futures import ThreadPoolExecutor as TPE
import logging
#import log

logger = logging.getLogger(__name__)

class ThreadManager:
    """A wrapper around ThreadPoolExecutor 
    to handle exceptions in worker threads."""
    def __init__(self):
        self.tp = TPE()

    def start(self,worker,*args,**kwargs):
        """Start a worker thread and attach an exception handler."""
        logger.debug("Starting thread")
        fut = self.tp.submit(worker,*args,**kwargs)
        fut.add_done_callback(self._handle_thread_completion)

    def shutdown(self, wait=True):
        """Stop accepting work and let existing worker threads finish."""
        logger.debug("Shutting down thread")
        self.tp.shutdown(wait=wait, cancel_futures=True)

    def _handle_thread_completion(self, fut):
        logger.debug("Thread Callback entered")
        logger.debug("done=%s cancelled=%s exception=%r",fut.done(),fut.cancelled(),fut.exception())
        try:
            fut.result()
        except Exception:
            logging.exception("Worker Thread CRASHED")
        finally:
            logger.debug("Thread Exited")
        
         

i = 0        
def worker(a,b,f=None):
    global i
    print("a:",a,"b:",b,f)
    while True:
        i += 1 
        print(i)  
        if i == 5:
            1/0

if __name__ == "__main__":        
    sp = ThreadManager()
    sp.start(worker,5,6,f=10)
    print("after")
    
        