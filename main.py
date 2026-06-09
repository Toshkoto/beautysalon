from utilities import *
import random

class SalonManager:
    def __init__(self) -> None:
        self.OPENING_TIME = time(7, 0)
        self.CLOSING_TIME = time(17, 0)
        self.history: Stack = Stack()

        self.service_prices = {
            "facial": 30,
            "hair care": 10,
            "nails": 35,
            "balding": 4,
            "showering": 19
        }

        self.client_db = read_clients_csv()

        # pri wseki method kydeto se izpolzwa self.reservations trqbwa da se prochita nanowo za da e actualno 

    def add_reservation(self, ap: Apointment) -> bool:

        self.reservations = read_reservations_csv()

        if not self.reservations:
            append_reservation_csv(ap.get_obj())
            return True

        DURATION = 1

        current_start = ap.t
        current_end = time(ap.t.hour + DURATION, ap.t.minute)

        if current_start < self.OPENING_TIME or current_end > self.CLOSING_TIME: return False
        if self.reservations is None:
            append_reservation_csv(ap.get_obj())
            return True
        
        # insert reservation at the start (first)
        if self.OPENING_TIME <= current_start and current_end <= list_to_time(self.reservations[0]['t']):
            self.reservations.insert(0, ap.get_obj())
            append_reservation_csv(ap.get_obj())
            return True
        
        next_start = list_to_time(self.reservations[-1]['t'])
        # try to insert somewhere in the middle
        for i in range(1, len(self.reservations)):
            prev_end = time(self.reservations[i - 1]['t'][0] + DURATION, self.reservations[i - 1]['t'][1])
            next_start = list_to_time(self.reservations[i]['t'])
            
            if prev_end <= current_start and current_end <= next_start:
                self.reservations.insert(i, ap.get_obj())
                append_reservation_csv(ap.get_obj())
                return True

        # insert reservation at the end (last)
        last_end = time(next_start.hour + DURATION, next_start.minute)
        if current_start >= last_end and current_end <= self.CLOSING_TIME:
            self.reservations.append(ap.get_obj())
            append_reservation_csv(ap.get_obj())
            return True
        
        return False

    def serve_client(self) -> Apointment:
        self.reservations = read_reservations_csv()

        if not self.reservations:
            print("There are no clients to serve")
            return
        
        popped = self.reservations.pop(0)
        write_reservations_csv(self.reservations)
        
        return Apointment(popped)

    # def client_incoming(self):
    #     num = random.randrange(0, 101)
    #     if num <= 50:
    #         print("AHHHHHH A SMOTAN CLIENT HAS COME IN WITHOUT A RESERVATION")
    #         client = Client(self.client_db[random.randrange(0, len(self.client_db))]).get_obj()
    #         time = (random.randrange(self.OPENING_TIME.hour, self.CLOSING_TIME.hour), random.randrange(0, 60))
    #         treatment = random.choice(list(self.service_prices.keys()))
    #         ap_data = {
    #             "t": time,
    #             "treatment": treatment,
    #             "price": self.service_prices[treatment],
    #             "client": client
    #         }

    #         while True:
    #             print(f"client: {client}")
    #             print(f"treatment: {treatment}")
    #             print(f"time: {time[0]}:{time[1]}")
    #             print("serve him? (y/n)")
    #             print("view reservations (3)")
    #             inp = input(">>> ").lower()
    #             if inp == 'y':
    #                 print("client served")
    #                 if
    #                 input()
                
    #             if inp == 'n':
    #                 print("client turned away")
    #                 break

    #             elif inp == '3':
    #                 print(self.get_reservations())
    #                 print("expand? (y/n)")
    #                 inp = input(">>> ").lower()

    #                 if inp == 'y':
    #                     self.expand_reservations()

    def draw_menu(self):
        while True:
            print("\033[2J\033[H")
            print("*******************************")
            print("BEAUTY SALON TOMMY")
            print("(free facials)")
            print("*******************************")
            print("add reservation (1)")
            print("serve a client (2)")
            print("view reservations (3)")
            print("quit (q)")
            inp = input(">>> ")
            if inp == 'q': return
            if not inp.isdigit(): continue

            status = self.client_incoming()
            if status == 1: continue
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
                # wizh lista otnosno shansowete da se padne smotan client.
                # ako smotaniq client ima dosie s poweche tochki ot reservaciqta - obsluzhwame nego
                print(self.serve_client())
                self.history.push("serving client")

            elif inp == 3:
                print(self.get_reservations())
                print("expand? (y/n)")
                inp = input(">>> ").lower()

                if inp == 'y':
                    self.expand_reservations()

    def get_reservations(self):
        sort_reservations()
        self.reservations = read_reservations_csv()
        return ["There are no reservations" if not self.reservations else r['t'] for r in self.reservations]
    
    def search(self, column: str, target: str):
        reserv = pd.read_csv("reservations.csv")
        print(reserv.loc[reserv[str(column)] == str(target)])
        

# ako ostane wreme - add reservation zapiswa samo imeto na klienta
# tyrsim drugite mu danni w client_database

    def expand_reservations(self):

        print(pd.read_csv("reservations.csv"))
        
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


if __name__ == "__main__":
    print(random.choice(["いらしゃいませ", "はじめまして", "here comes a black guy", "Howdy"]))
    salon_manager = SalonManager()
    salon_manager.draw_menu()