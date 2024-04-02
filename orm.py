from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey, Boolean, JSON
from sqlalchemy.orm import registry, relationship
import model

mapper_registry = registry()

metadata = MetaData()

problems = Table(
    "problems",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("text", String(1000)),
    Column("title", String(1000)),
    Column("description", String(1000)),
    Column("category", String(255)),
    Column("code", String(1000)),
    Column("input_arrays", JSON, nullable=True),  # JSON field for Input_Arrays
)

# Not actually using this
# test_cases = Table(
#     "test_cases",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("input", String(255)),
#     Column("output", String(255)),
#     Column("problem_id", ForeignKey("problems.id"))
# )


def start_mappers():
    mapper_registry.map_imperatively(model.Problem, problems)
    # mapper_registry.map_imperatively(model.TestCase, test_cases)

