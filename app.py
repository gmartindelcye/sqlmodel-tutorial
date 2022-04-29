from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, or_, select


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()

        hero_1 = Hero(
            name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
        )
        hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        hero_3 = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team_id=team_preventers.id,
        )
        hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
        hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
        hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
        hero_7 = Hero(name="Captain North", secret_name="Esteban Roger", age=93)

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
    """Select hero by name. Using 'one' instead of 'first'."""
    with Session(engine) as session:
        hero = session.exec(select(Hero).where(Hero.name == name)).one()
        print(hero)


def select_hero_by_id(id: int):
    """Select Hero by Id. Using 'get' instead of 'exec'."""
    with Session(engine) as session:
        hero = session.get(Hero, id)
        print(hero)


def select_heroes_by_age_range(ge: int, lt: int):
    """Select heroes in the age range"""
    with Session(engine) as session:
        heroes = session.exec(select(Hero).where(Hero.age >= ge, Hero.age < lt)).all()
        print(heroes)


def select_heroes_by_out_age_range(le: int, gt: int):
    """Select heroes out of the selected age range"""
    with Session(engine) as session:
        heroes = session.exec(
            select(Hero).where(or_(Hero.age <= le, Hero.age > gt))
        ).all()
        print(heroes)


def update_hero_age(id: int, age: int):
    """Select Hero by Id. Then updates age."""
    with Session(engine) as session:
        hero = session.get(Hero, id)
        print(hero)

        hero.age = age

        session.add(hero)
        session.commit()
        session.refresh(hero)
        print(hero)


def delete_hero(id: str):
    """Select Hero by Id. Then delete it."""
    with Session(engine) as session:
        hero = session.get(Hero, id)

        session.delete(hero)  #
        session.commit()  #

        hero = session.get(Hero, id)
        if hero is None:  #
            print(f"There's no hero with id: {id}")


def select_heroes_teams():
    """Select only heroes in teams"""
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)


def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()
    # select_hero_by_name("Deadpond")
    # select_hero_by_id(6)
    # select_heroes_by_age_range(35, 45)
    # select_heroes_by_out_age_range(35, 90)
    # update_hero_age(id=2, age=16)
    # delete_hero(5)
    select_heroes_teams()


if __name__ == "__main__":
    main()
