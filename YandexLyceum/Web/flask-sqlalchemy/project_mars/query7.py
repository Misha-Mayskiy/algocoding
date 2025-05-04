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

        colonists_to_update = session.query(User).filter(
            User.address == "module_1",
            User.age < 21
        ).all()

        for colonist in colonists_to_update:
            colonist.address = "module_3"

        session.commit()

    except Exception as e:
        if 'session' in locals() and session:
            session.rollback()
    finally:
        if 'session' in locals() and session:
            session.close()


if __name__ == '__main__':
    main()
