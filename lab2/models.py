from pydantic import BaseModel


class Model(BaseModel):
    @classmethod
    def from_tuple(cls, data):
        return [cls(**{key: data[i] for i, key in enumerate(
                cls.__fields__.keys())})][0]


class Student(Model):
    __name__ = 'student'
    __table__ = "students"
    id: int
    first_name: str
    last_name: str
    age: int
    group_id: int


class Group(Model):
    __name__ = 'group'
    __table__ = "groups"
    id: int
    group_name: str


class Subject(Model):
    __name__ = 'subject'
    __table__ = "subjects"
    id: int
    subject_name: str


class Mark(Model):
    __name__ = 'mark'
    __table__ = "marks"
    id: int
    student_id: int
    subject_id: int
    mark: int
