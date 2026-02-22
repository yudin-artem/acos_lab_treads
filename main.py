import queue
from consumer import Consumer
from producer import Producer
import cv2
import numpy as np

queue_in = queue.Queue()
queue_out = queue.Queue()
consumers_count = 5

try:
    producer = Producer(queue_in, queue_out, './image.jpeg', consumers_count)
    consumers_list = [Consumer(i+1, queue_in, queue_out) for i in range(consumers_count)]

    producer.start()
    for consumer in consumers_list:
            consumer.start()

    none_count = 0
    res = []

    while none_count != consumers_count:
        elem = queue_out.get()
        if elem is None:
            none_count += 1
            continue
        res.append(elem)

    res.sort()
    res = [elem[1] for elem in res]
    try:
        np_array = np.array(res)
    except:
        print('numpy convertion error!')
    else:
        cv2.imwrite('res.jpeg', np_array)
except Exception as e:
    print(f'error: {e}')