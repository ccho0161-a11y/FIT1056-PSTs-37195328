class Teacher:
    def __init__(self,name):
        self.name = name
        self.__salary = 300000

    def get_salary(self):
        return self.__health
    
    def set_salary(self, value):
        if 30000 <= value <= 150000:
            self.__salary = value
        else:
            print("Invalid salary.")

class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        print("Some generic sound")

class Lion(Animal):
    def speak(self):
        print("Roar!")

class Parrot(Animal):
        def speak(self):
            print("Squawk!")

a1 = Lion("Simba")
a2 = Parrot("Kiwi")

class Animal:
    total_animals = 0
    def __init__(self, name):
        self.name = name
        Animal.total_animals += 1

    @staticmethod
    def show_total():
        print("Total animals created:", Animal.total_animals)

a1 = Animal("Cat")
a2 = Animal("Dog")
Animal.show_total()