from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, or_, select


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North", secret_name="Esteban Roger", age=93)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)

        session.commit()

        session.refresh(hero_1)
        session.refresh(hero_2)
        session.refresh(hero_3)
        session.refresh(hero_4)
        session.refresh(hero_5)
        session.refresh(hero_6)
        session.refresh(hero_7)


def select_heroes():
    """Select all Heroes"""
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        print(heroes)


def select_hero_by_name(name: str):
    with Session(engine) as session:
        hero = session.exec(select(Hero).where(Hero.name == name)).one()
        print(hero)


def select_hero_by_id(id: int):
    with Session(engine) as session:
        hero = session.get(Hero, id)
        print(hero)


def select_heroes_by_age_range(ge: int, lt: int):
    with Session(engine) as session:
        heroes = session.exec(select(Hero).where(Hero.age >= ge, Hero.age < lt)).all()
        print(heroes)


def select_heroes_by_out_age_range(le: int, gt: int):
    with Session(engine) as session:
        heroes = session.exec(
            select(Hero).where(or_(Hero.age <= le, Hero.age > gt))
        ).all()
        print(heroes)


def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()
    select_hero_by_name("Deadpond")
    select_hero_by_id(6)
    select_heroes_by_age_range(35, 45)
    select_heroes_by_out_age_range(35, 90)


if __name__ == "__main__":
    main()
