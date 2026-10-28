import heapq


def can_attend_all(events):
    events = sorted(events)
    for i in range(1, len(events)):
        if events[i][0] < events[i - 1][1]:
            return False
    return True


def min_rooms_required(events):
    heap = []  # end times of rooms that are in use
    for start, end in sorted(events):
        if heap and heap[0] <= start:
            heapq.heappop(heap)  # reuse that room
        heapq.heappush(heap, end)
    return len(heap)


def assign_rooms(events):
    # returns a list of (event, room name) in the same order as the input
    order = sorted(range(len(events)), key=lambda i: events[i])
    busy = []   # (end time, room number)
    free = []   # room numbers that are free
    count = 0
    result = [None] * len(events)
    for i in order:
        start, end = events[i]
        while busy and busy[0][0] <= start:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)
        else:
            room = count
            count += 1
        heapq.heappush(busy, (end, room))
        result[i] = (events[i], "Room " + chr(65 + room))
    return result
