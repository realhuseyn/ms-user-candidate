import enum


class Gender(str, enum.Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    NOT_SPECIFIC = 'Not Specific'


class Degree(str, enum.Enum):
    BACHELOR = 'Bachelor'
    MASTER = 'Master'
    HS = 'High School'


class JobMajor(str, enum.Enum):
    CS = 'Computer Science'
    CIS = 'Computer Information Systems'


class CareerLevel(str, enum.Enum):
    JUNIOR = 'Junior'
    MIDDLE = 'Middle'
    SENIOR = 'Senior'
    EXPERT = 'Expert'
