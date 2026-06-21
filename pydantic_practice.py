from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age:  int

p1 = Person(name="Tanya", age=25)
print(p1)

p2 = Person(name="Tanya", age="not a number")
print(p2)
