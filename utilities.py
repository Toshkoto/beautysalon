from datetime import time
import pandas as pd

def list_to_time(arr):
    return time(arr[0], arr[1])

def read_clients_csv():
    df = pd.read_csv('client_database.csv')
    return df.to_dict('records')

def read_reservations_csv():
    df = pd.read_csv('reservations.csv')
    reservations = []
    for _, row in df.iterrows():
        client_dict = {
            "name": row['client_name'],
            "phone": row['client_phone'],
            "loyalty-points": int(row['client_loyalty_points'])
        }
        reservation_dict = {
            "treatment": row['treatment'],
            "t": (int(row['time_hour']), int(row['time_minute'])),
            "price": int(row['price']),
            "client": client_dict
        }
        reservations.append(reservation_dict)
    return reservations

def write_reservations_csv(reservations_list):
    data = []
    for r in reservations_list:
        data.append({
            'treatment': r['treatment'],
            'time_hour': r['t'][0],
            'time_minute': r['t'][1],
            'price': r['price'],
            'client_name': r['client']['name'],
            'client_phone': r['client']['phone'],
            'client_loyalty_points': r['client']['loyalty-points']
        })
    df = pd.DataFrame(data)
    df.to_csv('reservations.csv', index=False)

def append_reservation_csv(reservation):
    df = pd.read_csv('reservations.csv')
    new_row = {
        'treatment': reservation['treatment'],
        'time_hour': reservation['t'][0],
        'time_minute': reservation['t'][1],
        'price': reservation['price'],
        'client_name': reservation['client']['name'],
        'client_phone': reservation['client']['phone'],
        'client_loyalty_points': reservation['client']['loyalty-points']
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv('reservations.csv', index=False)

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