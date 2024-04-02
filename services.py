from __future__ import annotations

import model
from repository import AbstractRepository


def add_problem(problem: model.Problem, repo, session):
    session.add(problem)
    session.commit()

    problems = repo.list() # list all problems

    print("Problems table")
    for problem in problems:
        print(f"id: {problem.id} text: {problem.text}")




