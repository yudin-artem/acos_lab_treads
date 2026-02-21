import threading
import queue

class Consumer(threading.Thread):
    def __init__(self, processor, name):
        super().__init__()
        self.processor = processor
        self.name = name
        self.daemon = True
        self.processed_count = 0
        self.tasks_done = 0
        
    def run(self):
        print(f"{self.name}: start")
        
        while True:
            try:
                task = self.processor.task_queue.get(timeout=1)
                if task is None:
                    break
                processed_pixels = self.invert_pixels(task['pixels'])
                self.processed_count += len(processed_pixels)
                self.tasks_done += 1
                result = (task['start_idx'], processed_pixels)
                self.processor.result_queue.put(result)
                
                self.processor.task_queue.task_done()
                
            except queue.Empty:
                if not self.processor.producer.is_alive() and self.processor.task_queue.empty():
                    break
                continue
        
    
    def invert_pixels(self, pixels):
        inverted = []
        for pixel in pixels:
            try:
                if isinstance(pixel, (tuple, list)) and len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                    inverted.append((255 - r, 255 - g, 255 - b))
                else:
                    inverted.append((128, 128, 128))
            except Exception as e:
                inverted.append((0, 0, 0))          
        return inverted
