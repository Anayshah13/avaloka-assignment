import threading
from lru_cache import LRUCache, SafeLRUCache
from event_scheduler import can_attend_all, min_rooms_required, assign_rooms


def test_lru_basic():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)            # evicts 2
    assert c.get(2) == -1
    c.put(4, 4)            # evicts 1
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4


def test_lru_update():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 10)           # 1 is now most recent
    c.put(3, 3)            # evicts 2
    assert c.get(1) == 10
    assert c.get(2) == -1


def test_lru_edge():
    c = LRUCache(1)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == -1
    assert c.get(2) == 2
    assert LRUCache(3).get(5) == -1


def test_threads():
    c = SafeLRUCache(100)

    def work(n):
        for i in range(1000):
            c.put((n, i % 150), i)
            c.get((n, i % 150))

    ts = [threading.Thread(target=work, args=(n,)) for n in range(8)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert len(c.map) == 100


def test_can_attend():
    assert can_attend_all([(9, 10), (10, 11), (11, 12)]) == True
    assert can_attend_all([(0, 30), (5, 10), (15, 20)]) == False
    assert can_attend_all([]) == True


def test_min_rooms():
    assert min_rooms_required([(9, 10), (10, 11), (11, 12)]) == 1
    assert min_rooms_required([(0, 30), (5, 10), (15, 20)]) == 2
    assert min_rooms_required([(11, 12), (9, 10), (10, 11)]) == 1   # unsorted
    assert min_rooms_required([(1, 5)] * 4) == 4
    assert min_rooms_required([(1, 10), (2, 9), (3, 8)]) == 3
    assert min_rooms_required([]) == 0


def test_assign_rooms():
    got = assign_rooms([(0, 30), (5, 10), (10, 20)])
    assert got == [((0, 30), "Room A"), ((5, 10), "Room B"), ((10, 20), "Room B")]


tests = [test_lru_basic, test_lru_update, test_lru_edge, test_threads,
         test_can_attend, test_min_rooms, test_assign_rooms]
for t in tests:
    t()
    print("passed:", t.__name__)
print("all", len(tests), "tests passed")
