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

        """
        TODO
        dawa error line 32, pusni debugger i dobyrshi systemata
        """

    def add_reservation(self, ap: Apointment) -> bool:

        reserv = open("reservations.json", "w+")
        self.reservations = json.load(reserv)

        if not self.reservations:
            reserv.append(ap)
            reserv.write(json.dumps(reserv))
            reserv.close()
            return True

        DURATION = 1

        current_start = ap.t
        current_end = time(ap.t.hour + DURATION, ap.t.minute)

        if current_start < self.OPENING_TIME or current_end > self.CLOSING_TIME: return False
        if self.reservations is None:
            self.reservations.append(ap)
            return True
        
        # insert reservation at the start (first)
        if self.OPENING_TIME <= current_start and current_end <= self.reservations[0].t:
            self.reservations.insert(0, ap)
            return True
        
        # try to insert somewhere in the middle
        for i in range(1, len(self.reservations)):
            prev_end = time(self.reservations[i - 1].t.hour + DURATION, self.reservations[i - 1].t.minute)
            next_start = self.reservations[i].t
            
            if prev_end <= current_start and current_end <= next_start:
                self.reservations.insert(i, ap)
                return True

        # insert reservation at the end (last)
        last = time(next_start.hour + DURATION, next_start.minute)
        if current_start >= last and current_end <= self.CLOSING_TIME:
            self.reservations.append(ap)
            return True
        
        return False

    def serve_client(self) -> Apointment:
        if not self.reservations:
            print("There are no clients to serve")
            return
        
        return self.reservations.pop(0)

    def print_reservations(self) -> None:
        print([r.t for r in self.reservations])

    def draw_menu(self):
        while True:
            print("*******************************")
            print("BEAUTY SALON TOMMY")
            print("(free facials)")
            print("*******************************")
            print("add reservation (1)")
            print("serve a client (2)")
            print("view client's file (3)")
            print("view reservations (4)")
            inp = input(">>> ")
            if not inp.isdigit(): continue

            if int(inp) == 1:
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

                # self.print_reservations()

    def get_reservations(self) -> list:
        return [r['t'] for r in self.reservations]


"""
f = open("reservations.json", "w+")
reserv = json.load(f)

"""

"""
available services: hair care, nails, facial, hair removal(balding), kypane treatment
making an apointment
new Apointment(facial, time(14, 30), 30, client)
algorithm for creating a random client
"""

if __name__ == "__main__":
    salon_manager = SalonManager()
    salon_manager.draw_menu()