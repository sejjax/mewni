from enum import Enum

class Sex(Enum):
    MALE = 'male'
    FEMALE = 'female'
class State:
    name: str
    age: int
    sex: Sex
    def __call__(self, *args, **kwargs):

class Stage:

    @filter(State.name)
    def set_name(self):
        State.name = 'Danil'

    @filter(State.name)
    def set_age(self):
        State.age = 10

    @filter(State.name)
    def set_age(self):
        State.sex = Sex('male')

    def set_profile(self):
        while True:
            name = await ask('Please, enter your name')
            if is_name(name):
                break
        age = ask('Please, enter your age')
        sex = select('Please, choose beetween male and female')
