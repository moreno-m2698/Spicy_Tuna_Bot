from dataclasses import dataclass

# these functions have names
def helloWorld():
    return 'Hello World'


#?
x = helloWorld

# calling the function
y = helloWorld()

print(x)

print(y)

print(x())

#higher order functions

def hey():
    return "hey"

def Ultrahey(x, y):
    return x() + y()



print(Ultrahey(hey,x))


#anonymous functions/ lambda functions

add10 = lambda x: x + 10

y = add10(5)

addTwoNumbers = lambda x,y: x + y

z = addTwoNumbers(10,5)
print(y)
print(z)

#function composition
fog = addTwoNumbers(add10(5), add10(add10(6)))

print(fog)


#Make a higher order function called map, that accepts a list and a function
#It applies the function to every element in the list and returns the modified list
#assume the list can only take integer values


#this returns a new value in memory based on the previous
def map(ls, ftn):
    result = []
    for item in ls:
        result.append(ftn(item))
    return result    



#mutating values in memory
def mutateMap(ls, ftn):
    for index in range(len(ls)):
        ls[index] = ftn(ls[index])




# michaelList = [1,2,3,4]

# print(michaelList)

# newList = map(michaelList, lambda x: x * x)

# print(michaelList)

# print(newList)



# myList = [1,2,3,4]
# print(myList)
# myNewList = mutateMap(myList, lambda x: x* x)
# print(myList)
# print(myNewList)
# print(myList is myNewList)


@dataclass
class Person:
    name: str
    age: int



#Make a higher order function called filter which accepts a list and a function that returns a boolean
#assume that the list has only people and the function accepts an input of people
#filter gets rid of any elements where the function returns true
#no mutations :)

personList = [Person("John", 32), Person("Bob", 14), Person("Dylan", 44), Person("Kanye West", 87)]

# filter -> (personList, lambda x: x.age < 35) -> [Dylan, Kanye]

def filter(ls, ftn):
    result = []
    for l in ls:
        if not(ftn(l)):
            result.append(l)

    return result

print(filter(personList, lambda x: x.name[0] =='J'))



