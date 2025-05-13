class Student:
    def __init__ (self, name,marks):
        self.name= name
        self.marks=marks
        
    def display_student(self):
        print(f"Name: {self.name}, Marks:{self.marks}")

s1 =Student("Amna","236")
s2 = Student("Ali","255")

s1.display_student()
s2.display_student()

