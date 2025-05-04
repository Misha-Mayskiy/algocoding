from users import User
import db_session

DB_NAME = "mars_explorer.db"


def main():
    print(f"Инициализация базы данных: {DB_NAME}")
    db_session.global_init(DB_NAME)
    print("База данных инициализирована.")

    session = db_session.create_session()
    print("Сессия создана.")

    captain = User()
    captain.surname = "Scott"
    captain.name = "Ridley"
    captain.age = 21
    captain.position = "captain"
    captain.speciality = "research engineer"
    captain.address = "module_1"
    captain.email = "scott_chief@mars.org"
    captain.hashed_password = "password_scott"
    print(f"Подготовка капитана: {captain.surname} {captain.name}")

    colonist1 = User()
    colonist1.surname = "Watney"
    colonist1.name = "Mark"
    colonist1.age = 25
    colonist1.position = "science specialist"
    colonist1.speciality = "botanist"
    colonist1.address = "module_1"
    colonist1.email = "mark_watney@mars.org"
    colonist1.hashed_password = "password_watney"
    print(f"Подготовка колониста 1: {colonist1.surname} {colonist1.name}")

    colonist2 = User()
    colonist2.surname = "Lewis"
    colonist2.name = "Melissa"
    colonist2.age = 30
    colonist2.position = "commander"
    colonist2.speciality = "geologist"
    colonist2.address = "module_1"
    colonist2.email = "melissa_lewis@mars.org"
    colonist2.hashed_password = "password_lewis"
    print(f"Подготовка колониста 2: {colonist2.surname} {colonist2.name}")

    colonist3 = User()
    colonist3.surname = "Martinez"
    colonist3.name = "Rick"
    colonist3.age = 28
    colonist3.position = "pilot"
    colonist3.speciality = "pilot"
    colonist3.address = "module_2"
    colonist3.email = "rick_martinez@mars.org"
    colonist3.hashed_password = "password_martinez"
    print(f"Подготовка колониста 3: {colonist3.surname} {colonist3.name}")

    try:
        session.add(captain)
        session.add_all([colonist1, colonist2, colonist3])
        print("Пользователи добавлены в сессию.")

        session.commit()
        print("Изменения сохранены в базе данных.")

    except Exception as e:
        print(f"Ошибка при добавлении пользователей: {e}")
        session.rollback()
    finally:
        session.close()
        print("Сессия закрыта.")


if __name__ == '__main__':
    main()
