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
    
    def add_task(self, fn, *args, **kwargs):
        if not self.event_loop.loop.is_running():
            print("not running,starting up")
            self.start_event_loop()
        self.event_loop.submit_task("", fn, *args, **kwargs)
        
    def add_periodic_task(self, interval, callback, *args, **kwargs):
        if not self.event_loop.loop.is_running():
            self.start_event_loop()
        PeriodicTask(self.event_loop, interval ,callback, *args, **kwargs).start()
        

async def test():
    
    print("what a joke")
    
def test2():
    
    print("another joke")
    
if __name__ == "__main__":
    hm = HermesManager()
    #hm.start_event_loop()
    #hm.add_task(test)
    hm.add_periodic_task(5, test2)
    while True:
        pass
    