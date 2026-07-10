
import numpy as np
from sklearn.ensemble import RandomForestRegressor

class FlightAI: 
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
        self.X = np.array([
            ## Example input features: [distance, duration, passengers]
            [500, 30, 1],[500,5,1],[1000,30,2],[1000,5,2],[2000,30,3],[2000,30,3],
            [2000,5,3],[1500,15,3],[1500,15,2.5],[750,10,1.5],[1200,20,2.2],[1800,7,2.8]
            ]
        )  
        self.y = np.array([120,200,220,350,400,650,300,150,280,500,500,280])  # prices for above flights

    #train AI model
    def train(self):
        self.model.fit(self.X, self.y)
        self.trained = True
        print("AI prediction model trained successfully.")

    #predict flight price based on input features
    def predict(self, distance, days, duration):
        if not self.trained:
            print("Train the AI first before making predictions.")
            return None
        return round (self.model.predict([[distance, days, duration]])[0], 2)
    
    #Generate multiple flight options autimatically based on user input
    def generate_flight_options(self, distance, days):
        options = []
        for dur in np.linspace(distance/500, distance/400, 5):
            options.append((distance, days, round(dur,2)))
        return options
    
    # recommend top 3 flight option based on criterion (e.g., cheapest price)
    def recommend_flight_options(self, flights, criterion="cheapest"):
        if not self.trained:
            print("Train the AI first before making recommendations.")
            return 
        prices = [self.predict(flight[0], flight[1], flight[2]) for flight in flights]
        if criterion == "cheapest":
            sorted_idx = np.argsort(prices)
        elif criterion == "fastest":
            durations = [flight[2] for flight in flights]
            sorted_idx = np.argsort(durations)
        else:
            scores = np.array(prices) + np.array([flight[2]*100 for flight in flights])
            sorted_idx = np.argsort(scores)
        print(f"\n Top 3 flight options based on {criterion}:")
        for i in sorted_idx[:3]:
            flight = flights[i]
            print("Distance:", flight[0], "km")
            print("Days:", flight[1])
            print("Duration:", flight[2], "hours")
            print("Prices: $", prices[i])
            print("-"*20)

        #Front Desk
class App:
    #initialize the app with FlightAI instance
    def __init__(self):
        self.flight_ai = FlightAI()
        self.bookings = []
    
    #show main menu
    def menu(self):
        print("\n1.Train AI\n2.Book flight\n3.Suggest Flights\n4.View Bookings\n5.Exit")
    #run Application
    def run(self):
        while True:
            self.menu()
            choice = input("Choose: ")

            if choice == "1":
                self.flight_ai.train()

            elif choice == "2":
                try: 
                    d = int(input("Distance (km): "))
                    days = int(input("Days before flight: "))
                    dur = float(input("Duration (hr): "))
                    price = self.flight_ai.predict(d, days, dur)
                    if price:
                        print(f"Estimated flight price: $", price)
                        confirm = input("Do you want to book this flight? (y/n): ")
                        if confirm.lower() == "y":
                            self.bookings.append({
                                'distance': d,
                                'days': days,
                                'duration': dur,
                                'price': price
                            })
                            print("Flight booked successfully! Safe travels!")
                        else:print("Booking cancelled.")
                except:
                    print("Invalid input")
            elif choice == "3":
                try: 
                    d = int(input("Distance (km): "))
                    days = int(input("Days before flight: "))
                    flights = self.flight_ai.generate_flight_options(d, days)
                    crit = input("Enter criterion for recommendation (cheapest/fastest/balance): ").lower()
                    self.flight_ai.recommend_flight_options(flights, criterion=crit)
                except:
                    print("Invalid input")

                #loops through bookings list to show your tickets
            elif choice == "4":
                if not self.bookings:
                    print("No bookings yet.")
                else:
                    print("\nYour Bookings:")
                    for i, b, in enumerate (self.bookings, 1):
                        print("Booking #", i)
                        print("Distance:", b['distance'], "km")
                        print("Days:", b['days'])
                        print("Duration:", b['duration'], "hr")
                        print("Price: $", b['price'])
                        print("-"*20)
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

#Start the application
App().run()
