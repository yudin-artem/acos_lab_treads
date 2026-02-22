import threading
import cv2


class Producer(threading.Thread):
    print_lock = threading.Lock()

    def __init__(self, queue_in, queue_out, image_path=None, consumers=5):
        super().__init__()
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.image_path = image_path
        self.daemon = True
        self.consumers = consumers

    def run(self):
        try:
            if self.image_path is None:
                raise Exception("Image path is None ")
            
            print(f'Producer starts his work ')
            self.image = cv2.imread(self.image_path)

            for i, row in enumerate(self.image):
                self.queue_in.put((i, row))

        except Exception as e:
            print(f'Producer error: {e} ')

        finally:
            for i in range(self.consumers):
                self.queue_in.put(None)
            with self.print_lock:
                print(f'Producer ended his work: total tasks = {self.image.shape[0]} total pixels = {self.image.shape[0] * self.image.shape[1]} ')
