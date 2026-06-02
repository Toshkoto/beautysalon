from utilities import *
import random

class SalonManager:
    def __init__(self) -> None:
        self.OPENING_TIME = time(7, 0)
        self.CLOSING_TIME = time(17, 0)
        self.client_database: list[Client] = [
            # made with chatgpt 
            # murzel sum
            Client("Emma Johnson", "+359887102341", 120),
            Client("Olivia Smith", "+359888203452", 75),
            Client("Sophia Brown", "+359889304563", 230),
            Client("Isabella Davis", "+359878405674", 45),
            Client("Mia Wilson", "+359879506785", 310),
            Client("Charlotte Moore", "+359887607896", 90),
            Client("Amelia Taylor", "+359888708907", 180),
            Client("Harper Anderson", "+359889809018", 60),
            Client("Evelyn Thomas", "+359878910129", 150),
            Client("Abigail Jackson", "+359879011230", 20),

            Client("Emily White", "+359887112341", 270),
            Client("Ella Harris", "+359888213452", 95),
            Client("Avery Martin", "+359889314563", 130),
            Client("Scarlett Thompson", "+359878415674", 40),
            Client("Grace Garcia", "+359879516785", 220),
            Client("Chloe Martinez", "+359887617896", 170),
            Client("Victoria Robinson", "+359888718907", 85),
            Client("Riley Clark", "+359889819018", 55),
            Client("Aria Rodriguez", "+359878920129", 300),
            Client("Lily Lewis", "+359879021230", 140),

            Client("Zoey Lee", "+359887122341", 200),
            Client("Nora Walker", "+359888223452", 65),
            Client("Hannah Hall", "+359889324563", 110),
            Client("Layla Allen", "+359878425674", 250),
            Client("Aurora Young", "+359879526785", 35),
            Client("Savannah Hernandez", "+359887627896", 190),
            Client("Brooklyn King", "+359888728907", 80),
            Client("Bella Wright", "+359889829018", 145),
            Client("Claire Lopez", "+359878930129", 15),
            Client("Skylar Hill", "+359879031230", 275),

            Client("Lucy Scott", "+359887132341", 50),
            Client("Paisley Green", "+359888233452", 160),
            Client("Everly Adams", "+359889334563", 105),
            Client("Anna Baker", "+359878435674", 240),
            Client("Caroline Nelson", "+359879536785", 70),
            Client("Nova Carter", "+359887637896", 330),
            Client("Genesis Mitchell", "+359888738907", 95),
            Client("Emilia Perez", "+359889839018", 180),
            Client("Kennedy Roberts", "+359878940129", 25),
            Client("Samantha Turner", "+359879041230", 210),

            Client("Maya Phillips", "+359887142341", 155),
            Client("Willow Campbell", "+359888243452", 88),
            Client("Kinsley Parker", "+359889344563", 265),
            Client("Naomi Evans", "+359878445674", 48),
            Client("Elena Edwards", "+359879546785", 120),
            Client("Sarah Collins", "+359887647896", 175),
            Client("Ariana Stewart", "+359888748907", 205),
            Client("Allison Sanchez", "+359889849018", 60),
            Client("Madelyn Morris", "+359878950129", 98),
            Client("Ruby Rogers", "+359879051230", 145),
        ]
        self.non_app_client: Queue[Client] # clienti bez chas 
        self.reservations: list[Apointment]

        service_prices = {
            "facial": 30,
            "hair care": 10,
            "nails": 35,
            "balding": 4,
            "showering": 19
        }

    def add_reservation(self, ap: Apointment) -> list:
        DURATION = 1

        current_start = ap.t
        current_end = time(ap.t.hour + DURATION, ap.t.minute)

        if current_start < self.OPENING_TIME or current_end > self.CLOSING_TIME: return [r.t for r in self.reservations]
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

    def serve_client(self):
        self.reservations.pop(0)

    def draw_menu(self):
        while True:
            print([r.t for r in self.reservations])
            print("*******************************")
            print("BEAUTY SALON TOMMY")
            print("(free facials)")
            print("*******************************")
            print("add reservation (1)")
            print("serve a client (2)")
            print("view client's file (3)")
            inp = input(">>> ")
            if not inp.isdigit(): continue

            if int(inp) == 1:
                t = input("Enter time of reservation: ")
                t = t.split(", ")
                t = list(map(int, t))
                t = time(t[0], t[1])
                treatment = inp("name of the service >>> ")
                if treatment not in self.service_prices: 
                    print("treatment not available")
                    continue

                if not self.add_reservation(t, treatment, self.service_prices[treatment],
                                            random.choice(self.client_database)):
                    print("reservation cannot be added at that time")

"""
available services: hair care, nails, facial, hair removal(balding), kypane treatment
making an apointment
new Apointment(facial, time(14, 30), 30, client)
algorithm for creating a random client
"""

salon_manager = SalonManager()
salon_manager.reservations = [Apointment(time(9, 0)), Apointment(time(10, 30)), Apointment(time(15, 0))]
# print([ap.t for ap in salon_manager.reservations])
# print(salon_manager.add_reservation(Apointment(time(8, 1))))

salon_manager.draw_menu()