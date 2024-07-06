from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, Text, UniqueConstraint
from typing import List

Base = declarative_base()


class Case(Base):
    __tablename__ = 'cases'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)
    risk = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    step = Column(Text, nullable=False)
    caur = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='uq_case_name'),
    )

    def to_list(self) -> list:
        return [str(self.id), self.name, self.risk, self.description, self.step, self.caur]

    def __repr__(self):
        return (f"Case(id={self.id}, name='{self.name}', risk={self.risk}, "
                f"description='{self.description[:20]}...', step='{self.step[:20]}...', "
                f"caur='{self.caur[:20]}...')")


class Database:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)


class CRUDHelper:
    def __init__(self, database_url):
        self.db = Database(database_url)
        # self.db.drop_tables()
        # self.db.create_tables()

    def add(self, instance):
        session = self.db.Session()
        try:
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        except Exception as e:
            session.rollback()
            print(f"Error adding instance: {e}")
            return None
        finally:
            session.close()

    def get_all(self, model_class):
        session = self.db.Session()
        try:
            return session.query(model_class).all()
        except Exception as e:
            print(f"Error getting all instances: {e}")
            return []
        finally:
            session.close()

    def get_by_id(self, model_class, id_):
        session = self.db.Session()
        try:
            return session.query(model_class).get(id_)
        except Exception as e:
            print(f"Error getting instance by id: {e}")
            return None
        finally:
            session.close()

    def update(self, instance):
        session = self.db.Session()
        try:
            session.merge(instance)
            session.commit()
            return instance
        except Exception as e:
            session.rollback()
            print(f"Error updating instance: {e}")
            return None
        finally:
            session.close()

    def delete(self, model_class, id_):
        session = self.db.Session()
        try:
            instance = session.query(model_class).get(id_)
            if instance:
                session.delete(instance)
                session.commit()
                return True
            else:
                print(f"No instance found with id: {id_}")
                return False
        except Exception as e:
            session.rollback()
            print(f"Error deleting instance: {e}")
            return False
        finally:
            session.close()

    def get_by_name_like(self, model_class, name):
        session = self.db.Session()
        try:
            return session.query(model_class).filter(model_class.name.like(f"%{name}%")).all()
        except Exception as e:
            print(f"Error getting instances by name like: {e}")
            return []
        finally:
            session.close()
