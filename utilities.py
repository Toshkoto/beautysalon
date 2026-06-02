from datetime import time


class Client:
    def __init__(self, name: str, phone: str, points: int) -> None:
        self.name = name
        self.phone = phone
        self.points = points
        self.history: Stack[Apointment]

class Apointment:
    def __init__(self, t: time, service_name: str, price: float, client: Client) -> None:
        self.service_name = service_name
        self.t = t
        self.price = price
        self.client = client

class DataStructure:
    def __init__(self) -> None:
        self.items: list[Client] = []
        self.size = 0

    def add(self, items: Client) -> None:
        self.items.append(items)
        self.size += 1

    def is_empty(self) -> bool:
        return self.size == 0

    def peek(self) -> Client:
        return self.items[len(self.items) - 1]

class Stack(DataStructure):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"Stack [top...bottom] {self.items[::-1]}"

    def pop(self) -> Client:
        return self.items.pop()

class Queue(DataStructure):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"Queue: [front...back] {self.items}"

    def dequeue(self) -> Client:
        return self.items.pop(0)