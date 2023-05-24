import heapq

from typing import List, Tuple, Any


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, Any]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: Any, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> Any:
        return heapq.heappop(self.elements)[1]

