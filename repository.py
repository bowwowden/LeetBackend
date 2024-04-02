import abc
import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Problem):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Problem:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, problem):
        self.session.add(problem)
        # self.session.commit()

    def get(self, id):
        return self.session.query(model.Problem).filter_by(id=id).one()

    def list(self):
        return self.session.query(model.Problem).all()

    