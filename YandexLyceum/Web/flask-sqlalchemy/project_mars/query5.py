import sys
import db_session
from jobs import Jobs


def main():
    db_name = input().strip()
    if not db_name:
        sys.exit(1)

    try:
        db_session.global_init(db_name)
        session = db_session.create_session()

        target_jobs = session.query(Jobs).filter(
            Jobs.work_size < 20,
            Jobs.is_finished == False
        ).all()

        for job in target_jobs:
            print(job)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        if 'session' in locals() and session:
            session.close()


if __name__ == '__main__':
    main()
