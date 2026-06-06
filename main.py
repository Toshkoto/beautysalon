from utilities import *
import random
import json

class SalonManager:
    def __init__(self) -> None:
        self.OPENING_TIME = time(7, 0)
        self.CLOSING_TIME = time(17, 0)
        self.non_ap_client: Queue[Client] # clienti bez chas

        self.service_prices = {
            "facial": 30,
            "hair care": 10,
            "nails": 35,
            "balding": 4,
            "showering": 19
        }

        with open("client_database.json") as db:
            self.client_db = json.load(db)

        # pri wseki method kydeto se izpolzwa self.reservations trqbwa da se prochita nanowo za da e actualno 

    def add_reservation(self, ap: Apointment) -> bool:

        with open("reservations.json", "r") as reserv:
            self.reservations = json.load(reserv)

        if not self.reservations:
            self.reservations.append(ap.get_obj())
            with open("reservations.json", "w") as reserv:
                reserv.write(json.dumps(self.reservations))
            return True

        DURATION = 1

        current_start = ap.t
        current_end = time(ap.t.hour + DURATION, ap.t.minute)

        if current_start < self.OPENING_TIME or current_end > self.CLOSING_TIME: return False
        if self.reservations is None:
            self.reservations.append(ap.get_obj())
            with open("reservations.json", "w") as reserv:
                reserv.write(json.dumps(self.reservations))
            return True
        
        # insert reservation at the start (first)
        if self.OPENING_TIME <= current_start and current_end <= list_to_time(self.reservations[0]['t']):
            self.reservations.insert(0, ap.get_obj())
            with open("reservations.json", "w") as reserv:
                reserv.write(json.dumps(self.reservations))
            return True
        
        next_start = list_to_time(self.reservations[-1]['t'])
        # try to insert somewhere in the middle
        for i in range(1, len(self.reservations)):
            prev_end = time(self.reservations[i - 1]['t'][0] + DURATION, self.reservations[i - 1]['t'][1])
            next_start = list_to_time(self.reservations[i]['t'])
            
            if prev_end <= current_start and current_end <= next_start:
                self.reservations.insert(i, ap.get_obj())
                with open("reservations.json", "w") as reserv:
                    reserv.write(json.dumps(self.reservations))
                return True

        # insert reservation at the end (last)
        last_end = time(next_start.hour + DURATION, next_start.minute)
        if current_start >= last_end and current_end <= self.CLOSING_TIME:
            self.reservations.append(ap.get_obj())
            with open("reservations.json", "w") as reserv:
                reserv.write(json.dumps(self.reservations))
            return True
        
        return False

    def serve_client(self) -> Apointment:
        with open("reservations.json", "r") as reserv:
            self.reservations = json.load(reserv)

        if not self.reservations:
            print("There are no clients to serve")
            return
        
        popped = self.reservations.pop(0)
        with open("reservations.json", "w") as reserv:
            reserv.write(json.dumps(self.reservations))
        
        return Apointment(popped)

    def draw_menu(self):
        while True:
            print("\033[2J\033[H")
            print("*******************************")
            print("BEAUTY SALON TOMMY")
            print("(free facials)")
            print("*******************************")
            print("add reservation (1)")
            print("serve a client (2)")
            print("view client's file (3)")
            print("view reservations (4)")
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

            elif inp == 2:
                # wizh lista otnosno shansowete da se padne smotan client.
                # ako smotaniq client ima dosie s poweche tochki ot reservaciqta - obsluzhwame nego
                print(self.serve_client())

            elif inp == 4:
                print(self.get_reservations())
                input()

    def get_reservations(self) -> list:
        with open("reservations.json", "r") as reserv:
            self.reservations = json.load(reserv)
            return [r['t'] for r in self.reservations]

if __name__ == "__main__":
    print(random.choice(["いらしゃいませ", "はじめして", "here comes a black guy"]))
    salon_manager = SalonManager()
    salon_manager.draw_menu()