import sqlalchemy as sa
import sqlalchemy.orm as orm

SqlAlchemyBase = orm.declarative_base()

__factory = None

def global_init(db_file: str):
    global __factory

    if __factory:
        return
    
    if not db_file or not db_file.strip():
        raise Exception("Не указан путь к базе данных")
    
    conn_url = f"sqlite:///{db_file.strip()}?check_same_thread=False"

    engine = sa.create_engine(conn_url, echo=False)
    __factory = orm.sessionmaker(engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> orm.Session:
    global __factory
    return __factory()