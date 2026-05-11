from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('postgresql://admin:admin@localhost')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    email = Column(String(60))
    login = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=True)
    col_from_vlad_dev = Column(String(50))

    def __repr__(self):
        return f"{self.name}, {self.email}, {self.login}"


if __name__ == '__main__':
    Base.metadata.create_all(engine)
