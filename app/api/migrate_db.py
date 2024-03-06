from sqlalchemy import create_engine

from api.models.item import Base as ItemBase
from api.models.sales import Base as SalesBase

DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    ItemBase.metadata.drop_all(bind=engine)
    ItemBase.metadata.create_all(bind=engine)
    SalesBase.metadata.drop_all(bind=engine)
    SalesBase.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()