import threading
import queue
import time

class Consumer(threading.Thread):
    print_lock = threading.Lock()
    
    def __init__(self, name, task_queue, result_queue):
        super().__init__()
        self.name = name
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.daemon = True
        self.processed_count = 0
        self.tasks_done = 0
        
    def run(self):
        while True:
            try:
                task = self.task_queue.get(timeout=1)
                
                if task is None:
                    break
                
                processed_pixels = self.invert_pixels(task[1])
                self.processed_count += len(processed_pixels)
                self.tasks_done += 1
                
                result = (task[0], processed_pixels)
                self.result_queue.put(result)
                
            except queue.Empty:
                if self.tasks_done == 0:
                    print(f"Consumer {self.name} didn't find task ")
                time.sleep(0.5)
                continue
            except Exception as e:
                print(f"Consumer {self.name}: unexpected error: {e} ")
                break

        self.result_queue.put(None)
        with self.print_lock:
            print(f"Consumer {self.name} finished work: total tasks = {self.tasks_done} total pixels converted = {self.processed_count} ")
    
    def invert_pixels(self, pixels):
        inverted = []
        for pixel in pixels:
            try:
                if len(pixel) == 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                    inverted.append((255 - r, 255 - g, 255 - b))
                else:
                    print(f"{self.name}: type error: {pixel} ")
            except Exception as e:
                print(f"Consumer {self.name}: error: {e} ")
        return inverted
