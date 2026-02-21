import threading
import queue

class Consumer(threading.Thread):
    def __init__(self, task_queue, result_queue, name, producer_thread):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.name = name
        self.producer_thread = producer_thread
        self.daemon = True
        self.processed_count = 0
        self.tasks_done = 0
        
    def run(self):
        while True:
            try:
                task = self.task_queue.get(timeout=1)
                
                if task is None:
                    break
                
                processed_pixels = self.invert_pixels(task['pixels'])
                self.processed_count += len(processed_pixels)
                self.tasks_done += 1
                
                result = (task['start_idx'], processed_pixels)
                self.result_queue.put(result)
                
                self.task_queue.task_done()
                
            except queue.Empty:
                if not self.producer_thread.is_alive() and self.task_queue.empty():
                    break
                continue
        
    
    def invert_pixels(self, pixels):
        inverted = []
        for i, pixel in enumerate(pixels):
            try:
                if isinstance(pixel, (tuple, list)) and len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                    inverted.append((255 - r, 255 - g, 255 - b))
                else:
                    print(f"{self.name}: type error: {pixel}")
            except Exception as e:
                print(f"{self.name}: error: {e}")
        return inverted
