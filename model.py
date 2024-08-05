from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, JSON, ForeignKey

Base = declarative_base()


class Problem(Base):
    __tablename__ = 'problems'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(1000))
    description = Column(String(1000))
    category = Column(String(255))
    difficulty = Column(String(255))

    # One-to-many relationship with Solution
    solutions = relationship("Solution", back_populates="problem")
    test_cases = relationship("TestCase", back_populates="problem")
    submissions = relationship("Submission", back_populates="problem")

    def __json__(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficulty': self.difficulty,
            'solutions': [sol.__json__() for sol in self.solutions],
            'test_cases': [tc.__json__() for tc in self.test_cases],
            'submissions': [s.__json__() for s in self.submissions]
        }


class Solution(Base):
    __tablename__ = 'solutions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    problem_id = Column(Integer, ForeignKey('problems.id'))
    language = Column(String(50))  # e.g., 'python', 'lisp'
    file_path = Column(String(1000))  # Path to the solution file

    problem = relationship("Problem", back_populates="solutions")

    def __json__(self):
        return {
            'id': self.id,
            'problem_id': self.problem_id,
            'language': self.language,
            'file_path': self.file_path
        }


class TestCase(Base):
    __tablename__ = 'test_cases'
    id = Column(Integer, primary_key=True, autoincrement=True)
    problem_id = Column(Integer, ForeignKey('problems.id'))
    inputs = Column(JSON)
    expected_outputs = Column(JSON)

    problem = relationship("Problem", back_populates="test_cases")

    def __json__(self):
        return {
            'id': self.id,
            'problem_id': self.problem_id,
            'inputs': self.inputs,
            'expected_outputs': self.expected_outputs
        }


class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    problem_id = Column(Integer, ForeignKey('problems.id'))
    code = Column(JSON)
    outputs = Column(JSON)

    problem = relationship("Problem", back_populates="submissions")

    def __json__(self):
        return {
            'id': self.id,
            'problem_id': self.problem_id,
            'code': self.code,
            'outputs': self.outputs
        }
