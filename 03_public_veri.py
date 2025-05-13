class Car: #class definition
    def __init__(self,brand): #constructor
        self.brand=brand #public attribute
        

    def start(self): #method
        print(f"{self.brand} is starting.")

car1=Car("Honda") #object creation public
print(car1.brand)
car1.start()

        
