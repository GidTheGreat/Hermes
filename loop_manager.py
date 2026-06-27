"""Handle  all event loop operations and lifecycle"""
import asyncio
import logging
import threading

logger = logging.getLogger(__name__)

class LoopManager:
    def __init__(self):
        self.tasks = {}
        self.loop = asyncio.new_event_loop()
        self.thread = None
        
    def run_loop(self):
        """start loop and close it to ensure resources are allocated and yielded"""
        try:
            logger.debug("Starting event loop: %s",self.loop)
            asyncio.set_event_loop(self.loop)
            self.thread = threading.current_thread()
            logging.debug("Event loop thread is: %s",self.thread)
            self.loop.run_forever()
        finally:
            self.loop.close()
            logger.debug("Event loop: %s, closed succesfully",self.loop)
            self.thread = None
            self.tasks.clear()
            
    def _handle_task_completion(self,task):
        """Ensure task errors dont go unnoticed"""
        try:
            task.result()
        except asyncio.CancelledError:
            pass
        except Exception:
            logging.exception("%s, task crashed",task)    
    
    def _check_loop_status(self):
        if self.loop.is_closed():
            raise RuntimeError("Event loop has been closed.")
        if not self.loop.is_running():
            raise RuntimeError(
            "Event loop is not running. Start the event loop before submitting tasks."
        )
        
    def _dedupe_tasks(self,name):
        """Prevent recreation of the same task"""
        task = self.tasks.get(name)
        if task and not task.done():
            logger.debug("%s task already running",task)
            return task
                
    def submit_task(self, name, coro, *args, **kwargs):
        """Utility to handle safe task scheduling and naming for deuplication"""
        #self._check_loop_status()
        running_task = self._dedupe_tasks(name)
        if running_task:
            return running_task   
        def worker():
            task = self.loop.create_task(coro(*args,**kwargs),name=name)
            self.tasks[name] = task
            task.add_done_callback(
            self._handle_task_completion)
        self.loop.call_soon_threadsafe(
        worker)
        

    async def stop(self):
        """Cancel all tasks and stop loop"""
        current_loop = self.loop
        if current_loop.is_closed():
            logger.debug("%s, loop is not running")
            return
        current = asyncio.current_task()
        tasks = [t for t in asyncio.all_tasks() if t is not current]
        for task in tasks:
            task.cancel()
            logger.debug("Canceling task: %s", task)
           
        result = await asyncio.gather(*tasks,return_exceptions=True)
        logger.debug("All tasks canceled,confirmation results: %s",result)
        await current_loop.shutdown_asyncgens()
        current_loop.stop()
        logger.debug("Stopping the current event loop")
        
    