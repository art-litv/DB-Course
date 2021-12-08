from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    student_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    group_id = Column(String, ForeignKey("groups.group_id"))

    def __repr__(self):
        return "<Student(first_name='{}', last_name='{}', age={}, group_id={})>"\
            .format(self.first_name, self.last_name, self.age, self.group_id)


class Group(Base):
    __tablename__ = "groups"
    group_id = Column(Integer, primary_key=True)
    title = Column(String)

    def __repr__(self):
        return "<Group(title='{}')>"\
            .format(self.title)


class Subject(Base):
    __tablename__ = "subjects"
    subject_id = Column(Integer, primary_key=True)
    title = Column(String)

    def __repr__(self):
        return "<Subject(title='{}')>"\
            .format(self.title)


class Mark(Base):
    __tablename__ = "marks"
    mark_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"))
    mark = Column(Integer)

    def __repr__(self):
        return "<Mark(student_id={}, subject_id={}, mark={})>"\
            .format(self.student_id, self.subject_id, self.mark)
