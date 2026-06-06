from datetime import time

def list_to_time(arr):
    return time(arr[0], arr[1])

class Client:
    def __init__(self, object: dict) -> None:
        self.name: str = object["name"]
        self.phone: str = object["phone"]
        self.points: int = object["loyalty_points"]
        self.history: Stack[Apointment]

    def get_obj(self) -> dict:
        return {
            "name": self.name,
            "phone": self.phone,
            "loyalty-points": self.points
        }

class Apointment:
    def __init__(self, object: dict) -> None:
        self.treatment: str = object["treatment"]
        self.t: time = time(object["t"][0], object["t"][1])
        self.price: int = object["price"]
        self.client: dict = object["client"]

    def get_obj(self) -> dict:
        return {
            "treatment": self.treatment,
            "t": (self.t.hour, self.t.minute),
            "price": self.price,
            "client": self.client
        }

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