from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set


@dataclass
class Problem:
    text: str
    title: str
    description: str
    category: str
    code: str
    id: Optional[str] = None
    input_arrays: Optional[List[int]] = None

    def __json__(self):
        return {
            "id": self.id,
            "text": self.text,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "code": self.code,
            "input_arrays": self.input_arrays,
            # Do i even need these? i can store it all in json lists
            # "input_boolean": self.input_boolean,
            # "input_string": self.input_string,
        }


# class TestCase:
#     id: int
#     input: str
#     output: str
#     problem_id: int

