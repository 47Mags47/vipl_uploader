from contextlib import contextmanager
from unittest.mock import Base

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

# Создание движка подключения
main_engine = create_engine(
    "mysql+pymysql://VIPL:VIPL@localhost/VIPL",
    echo=True,
)

metadata = MetaData()
metadata.reflect(bind=main_engine)

Base = automap_base(metadata=metadata)
Base.prepare()

models = {}
for table_name in metadata.tables:
    models[table_name] = getattr(Base.classes, table_name)
    
@contextmanager
def session():
    session = sessionmaker(main_engine,expire_on_commit=False)()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        
if __name__ == '__main__':
    User = Base.classes.main__users
    Divisions = Base.classes.glossary__divisions
    
    User = models['main__users']
    with session() as s:
        full = s.query(User, Divisions).join(Divisions).all()
        for user, division in full:
            print(user.id, division.code)
        pass