class MinHeap:
    def __init__(self, values=()):
        self.heap = []
        self.keys = dict()

        for x in values:
            self.insert_key(x)

    def is_empty(self):
        return self.size() == 0

    def insert_key(self, key):
        i = len(self.heap)
        self.heap.append(key)
        self.keys[key] = i
        self.heapify_up(i)

    def peek(self):
        if self.is_empty():
            raise IndexError('Empty heap')
        return self.heap[0]

    def extract_min(self):
        if self.is_empty():
            raise IndexError('Empty heap')
        ret = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        del self.keys[ret]
        if not self.is_empty():
            self.keys[self.heap[0]] = 0
        self.heapify_down(0)
        return ret

    def heapify_up(self, i):
        lst = self.heap
        while i > 0:
            parent = MinHeap.parent(i)
            if lst[parent] <= lst[i]:
                break
            lst[i], lst[parent] = lst[parent], lst[i]
            self.keys[lst[i]] = i
            self.keys[lst[parent]] = parent
            i = parent

    def heapify_down(self, i):
        while True:
            left, right = MinHeap.left_child(i), MinHeap.right_child(i)
            smallest = i
            lst = self.heap
            if left < len(lst) and lst[left] < lst[smallest]:
                smallest = left
            if right < len(lst) and lst[right] < lst[smallest]:
                smallest = right
            if smallest == i:
                break
            lst[i], lst[smallest] = lst[smallest], lst[i]
            self.keys[lst[i]] = i
            self.keys[lst[smallest]] = smallest
            self.heapify_down(smallest)

    def decrease_key(self, key, new_val):
        self.decrease_key_at_index(self.keys[key], new_val)

    def decrease_key_at_index(self, i, new_val):
        if new_val > self.heap[i]:
            raise ValueError('Key value larger than before')
        del self.keys[self.heap[i]]
        self.heap[i] = new_val
        self.keys[new_val] = i
        self.heapify_up(i)

    def size(self):
        return len(self.heap)

    def __iter__(self):
        while not self.is_empty():
            yield self.extract_min()

    @staticmethod
    def parent(i):
        return (i - 1) // 2

    @staticmethod
    def left_child(i):
        return 2 * i + 1

    @staticmethod
    def right_child(i):
        return 2 * i + 2
