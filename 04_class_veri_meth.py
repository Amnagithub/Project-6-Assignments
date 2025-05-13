class Bank: #class
    my_bank="Stat Bank" #class variable
    
    @classmethod
    def change_bank_name(cls,name): #class method for change name
        cls.my_bank=name
        
c1 = Bank()
print(c1.my_bank)
Bank.change_bank_name("National Bank")
print(c1.my_bank)


    