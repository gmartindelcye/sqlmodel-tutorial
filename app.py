from typing import List, Optional 

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, or_, select


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: List["Hero"] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team=team_z_force
        )
        hero_rusty_man = Hero(
            name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_preventers
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)

        hero_spider_boy.team = team_preventers
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("Updated hero:", hero_spider_boy)

        hero_black_lion = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
        hero_sure_e = Hero(name="Princess Sure-E", secret_name="Sure-E")
        team_wakaland = Team(
            name="Wakaland",
            headquarters="Wakaland Capital City",
            heroes=[hero_black_lion, hero_sure_e],
        )
        session.add(team_wakaland)
        session.commit()
        session.refresh(team_wakaland)
        print("Team Wakaland:", team_wakaland)

        hero_tarantula = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
        hero_dr_weird = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
        hero_cap = Hero(
            name="Captain North America", secret_name="Esteban Rogelios", age=93
        )

        team_preventers.heroes.append(hero_tarantula)
        team_preventers.heroes.append(hero_dr_weird)
        team_preventers.heroes.append(hero_cap)
        session.add(team_preventers)
        session.commit()
        session.refresh(hero_tarantula)
        session.refresh(hero_dr_weird)
        session.refresh(hero_cap)
        print("Preventers new hero:", hero_tarantula)
        print("Preventers new hero:", hero_dr_weird)
        print("Preventers new hero:", hero_cap)


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


def select_heroes_and_teams():
    """Select all heroes and if they have, their team"""
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team, isouter=True)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)


def assign_hero_to_team(teamid: int, heroid: int):
    """Seach hero by id, assign team id"""
    with Session(engine) as session:
        hero = session.get(Hero, heroid)
        if hero:
            hero.team_id = teamid
            session.add(hero)
            session.commit()
            session.refresh(hero)


def remove_hero_from_team(id: int):
    """Seach hero by id, remove team id"""
    with Session(engine) as session:
        hero = session.get(Hero, id)
        if hero:
            hero.team_id = None
            session.add(hero)
            session.commit()
            session.refresh(hero)


def main():
    create_db_and_tables()
    create_heroes()
    # select_heroes()
    # select_hero_by_name("Deadpond")
    # select_hero_by_id(6)
    # select_heroes_by_age_range(35, 45)
    # select_heroes_by_out_age_range(35, 90)
    # update_hero_age(id=2, age=16)
    # delete_hero(5)
    # select_heroes_teams()
    # assign_hero_to_team(2, 7)
    # remove_hero_from_team(1)
    # select_heroes_and_teams()


if __name__ == "__main__":
    main()
