import sys
import db_session
from users import User


def main():
    db_name = input().strip()
    if not db_name:
        sys.exit(1)

    try:
        db_session.global_init(db_name)
        session = db_session.create_session()

        target_colonists = session.query(User).filter(
            (User.position.like('%chief%')) | (User.position.like('%middle%'))).all()

        for colonist in target_colonists:
            print(f"<Colonist> {colonist.id} {colonist.surname} {colonist.name} {colonist.position}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        if 'session' in locals() and session:
            session.close()


if __name__ == '__main__':
    main()
