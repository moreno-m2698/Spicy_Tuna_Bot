

#OBJECTS

#Not objects in Java, they are primitives because their literal values are stored
#int four = 4; -> 0000000000100 -> is this not a location, its a literal value

#char kay = 'k' -> 0000010001011

#Person michael = new Person(); -> 011000110010101 -> this is a location/address/reference in memmory hex/binary/decimal

# x -> location of 1

# x = 1

# print(hex(id(x)))

# x = 2

# print(hex(id(x)))

# x = 1

# print(hex(id(x)))

# print(hex(id(1)))


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __str__(self):
        return f"My name is {self.name} and I'm {self.age} years old, my place in memory is {hex(id(self))}"

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return Person(self.name, self.age)

    def __eq__(self, person2):
        return self.name == person2.name and self.age == person2.age

    def __add__(self, person2):
        return Person(self.name + person2.name, self.age + person2.age)
    
    def __sub__(self, person2):
        return Person(self.name[0:int(len(self.name)/2)] + person2.name[int(len(person2.name)/2):int(len(person2.name)+1)], self.age - person2.age)




# person1 = Person("John", 69) 

# person2 = Person("Sarah", 32)

# person3 = person1.copy()

# person4 = person3


# print(person1)
# print(person3)

# # is -> id(x) == id(y)

# print(person3 is person4)

# print(person1 - person2)

# #line above same as

# print(person1.__sub__(person2))

# #this is a tuple

# people = (person1, person3)

# print(people[0])





    





