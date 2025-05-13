class Counter: #class
    count = 0  #class variable

    def __init__(self): #count method
        Counter.count += 1

    @classmethod #decorator to call class method
    def get_count(cls): # class method to acees class variable
        print(f"Total Objects Created: {cls.count}")

c1 = Counter()
c2 = Counter()
c3 = Counter()
Counter.get_count()

        
