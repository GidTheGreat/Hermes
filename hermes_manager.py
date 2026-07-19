from .thread_manager import ThreadManager
from .loop_manager import LoopManager
from .periodic_task import PeriodicTask

class HermesManager:
    def __init__(self):
        self.event_loop = LoopManager()
        self.thread = ThreadManager()
        
    def start_event_loop(self):
        self.thread.start(self.event_loop.run_loop)
        
    def add_thread(self, fn, *args, **kwargs):
        self.thread.start(fn, *args, **kwargs)
    
    def add_task(self, name, fn, *args, **kwargs):
        if not self.event_loop.loop.is_running():
            print("not running,starting up")
            #self.start_event_loop()
        self.event_loop.submit_task(name, fn, *args, **kwargs)
        
    def add_periodic_task(self, interval, callback, *args, **kwargs):
        if not self.event_loop.loop.is_running():
            print("loop not running")
            #self.start_event_loop()
        PeriodicTask(self.event_loop, interval ,callback, *args, **kwargs).start()
        
    def stop(self):
        self.event_loop.submit_task("stop", self.event_loop.stop)
        self.thread.shutdown()
        

async def test():
    
    print("what a joke")
    
def test2():
    
    print("another joke")
    
if __name__ == "__main__":
    import signal
    import time
    import log
   
    running = True
    def handle(sig,frame):
        global running
        print("stop recieved")
        running = False
        
    
    signal.signal(signal.SIGINT , handle)
    hm = HermesManager()
    hm.start_event_loop()
    time.sleep(5)
    #hm.add_task("test",test)
    hm.add_periodic_task( 5, test2)
    while running:
        time.sleep(5)
        
    else:
        hm.stop()
   