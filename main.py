from utilities import *
import random

class SalonManager:
    def __init__(self) -> None:
        self.profit = 0
        self.OPENING_TIME = time(7, 0)
        self.CLOSING_TIME = time(17, 0)
        self.history: Stack = Stack()
        self.reservations = Queue(read_reservations_csv())
        self.times: Queue = Queue([time(r['t'][0], r['t'][1]) for r in self.reservations.items])
        print(self.reservations.items)
        print(self.times.items)

        self.service_prices = {
            "facial": 30,
            "hair care": 10,
            "nails": 35,
            "balding": 4,
            "showering": 19
        }

        self.client_db = read_clients_csv()

    def add_reservation(self, ap: Apointment) -> bool:

        if self.reservations.is_empty():
            self.reservations.push(ap.get_obj())
            write_reservations_csv(self.reservations.items)
            self.times.push(ap.t)
            return True

        DURATION = 1

        current_start = ap.t
        current_end = time(ap.t.hour + DURATION, ap.t.minute)

        if current_start < self.OPENING_TIME or current_end > self.CLOSING_TIME: return False
        if self.reservations is None:
            self.reservations.push(ap.get_obj())
            write_reservations_csv(self.reservations.items)
            return True
        
        # insert reservation at the start (first)
        if self.OPENING_TIME <= current_start and current_end <= list_to_time(self.reservations.items[0]['t']):
            self.reservations.push(ap.get_obj())
            write_reservations_csv(self.reservations.items)
            return True
        
        next_start = list_to_time(self.reservations.items[-1]['t'])
        # try to insert somewhere in the middle
        for i in range(1, len(self.reservations.items)):
            prev_end = time(self.reservations.items[i - 1]['t'][0] + DURATION, self.reservations.items[i - 1]['t'][1])
            next_start = list_to_time(self.reservations.items[i]['t'])
            
            if prev_end <= current_start and current_end <= next_start:
                self.reservations.push(ap.get_obj())
                write_reservations_csv(self.reservations.items)
                return True

        # insert reservation at the end (last)
        last_end = time(next_start.hour + DURATION, next_start.minute)
        if current_start >= last_end and current_end <= self.CLOSING_TIME:
            self.reservations.push(ap.get_obj())
            write_reservations_csv(self.reservations.items)
            return True
        
        return False

    def serve_client(self) -> Apointment:

        if self.reservations.is_empty():
            print("There are no clients to serve")
            input()
            return
        
        popped = self.reservations.dequeue()
        
        if self.reservations.is_empty():
            df = pd.DataFrame(columns=['treatment', 'time_hour', 'time_minute', 'price', 'client_name', 'client_phone', 'client_loyalty_points'])
            df.to_csv('reservations.csv', index=False)
        else:
            write_reservations_csv(self.reservations.items)

        self.profit += popped['price']
        
        return Apointment(popped)

    def draw_menu(self):
        while True:
            sort_reservations(self.reservations.items)
            print("\033[2J\033[H")
            print(random.choice(["いらしゃいませ", "はじめまして", "here comes a black guy", "Howdy"]))
            print("*******************************")
            print("BEAUTY SALON TOMMY")
            print("(free facials)")
            print("*******************************")
            print("add reservation (1)")
            print("serve a client (2)")
            print("view reservations (3)")
            print("view history (4)")
            print("take profit (5)")
            print("quit (q)")
            inp = input(">>> ")
            if inp == 'q': return
            if not inp.isdigit(): continue

            inp = int(inp)
            if inp == 1:
                t = input("Enter time of reservation: ")
                t = t.split(", ")
                t = tuple(map(int, t))
                treatment = input("name of the service >>> ")
                if treatment not in self.service_prices: 
                    print("treatment not available")
                    continue
                
                client = Client(self.client_db[random.randrange(0, len(self.client_db))])
                ap_data = {
                    "t": t,
                    "treatment": treatment,
                    "price": self.service_prices[treatment],
                    "client": client.get_obj()
                }
                if not self.add_reservation(Apointment(ap_data)):
                    print("reservation cannot be added at that time")
                    input()

                self.history.push(f"adding reservation {ap_data}")

            elif inp == 2:
                print(self.serve_client())
                self.history.push("serving client")

            elif inp == 3:
                print(self.get_reservations())
                self.history.push("get_reservations command done")
                print("expand? (y/n)")
                inp = input(">>> ").lower()

                if inp == 'y':
                    self.history.push("reservation data expanded")
                    self.expand_reservations()

            elif inp == 4:
                print(self.history)
                input()

            elif inp == 5:
                self.take_profit()
                input()

    def get_reservations(self):
        return ["There are no reservations" if self.reservations.is_empty() else r['t'] for r in self.reservations.items]
    
    def search(self, column: str, target: str):
        reserv = pd.read_csv("reservations.csv")
        print(reserv.loc[reserv[str(column)] == str(target)])
        self.history.push(f"searching through reservations: target = {str(target)}")

    def expand_reservations(self):

        data = []
        for r in self.reservations.items:
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
        print(df)
        
        print()
        while True:
            inp = input()
            if inp != "search": break
            search = input(">>> ")
            search = search.split(" ")
            if len(search) == 3:
                search[1] = search[1] + " " + search[2]
                search.pop()
            self.search(search[0], search[1])

    def take_profit(self):
        print(f"total profit so far: {self.profit}")
        self.history.push("profit taken")

if __name__ == "__main__":
    salon_manager = SalonManager()
    salon_manager.draw_menu()