class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}
        self.head = Node(0, 0)   # dummy nodes so no edge cases
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def add_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self.remove(node)
        self.add_front(node)
        return node.val

    def put(self, key, value):
        if key in self.map:
            self.remove(self.map[key])
        elif len(self.map) == self.cap:
            lru = self.tail.prev
            self.remove(lru)
            del self.map[lru.key]
        node = Node(key, value)
        self.map[key] = node
        self.add_front(node)


# thread safe version: same thing but with a lock
import threading


class SafeLRUCache(LRUCache):
    def __init__(self, capacity):
        LRUCache.__init__(self, capacity)
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            return LRUCache.get(self, key)

    def put(self, key, value):
        with self.lock:
            LRUCache.put(self, key, value)
