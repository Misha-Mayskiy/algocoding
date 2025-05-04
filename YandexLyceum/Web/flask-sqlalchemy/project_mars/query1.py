import sys
import db_session
from users import User


def main():
    db_name = input().strip()
    if not db_name:
        print("Ошибка: Имя файла базы данных не может быть пустым.")
        sys.exit(1)

    try:
        db_session.global_init(db_name)
        session = db_session.create_session()
        colonists_in_module_1 = session.query(User).filter(User.address == "module_1").all()

        for colonist in colonists_in_module_1:
            print(f"<Colonist> {colonist.id} {colonist.surname} {colonist.name}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        if 'session' in locals() and session:
            session.close()


if __name__ == '__main__':
    main()
