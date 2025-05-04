import sys
import db_session
from users import User
from jobs import Jobs


def main():
    db_name = input().strip()
    if not db_name:
        sys.exit(1)

    try:
        db_session.global_init(db_name)
        session = db_session.create_session()
        all_jobs = session.query(Jobs).all()

        if not all_jobs:
            return

        max_team_size = 0
        jobs_with_sizes = []

        for job in all_jobs:
            collaborators_str = job.collaborators if job.collaborators else ""
            ids = [item for item in collaborators_str.split(',') if item.strip()]
            current_team_size = len(ids)
            jobs_with_sizes.append((current_team_size, job.team_leader))
            if current_team_size > max_team_size:
                max_team_size = current_team_size

        if max_team_size == 0:
            return

        leader_ids_with_max_team = {
            leader_id for size, leader_id in jobs_with_sizes if size == max_team_size
        }

        if not leader_ids_with_max_team:
            return

        leaders = session.query(User).filter(User.id.in_(leader_ids_with_max_team)).all()

        for leader in leaders:
            print(f"{leader.surname} {leader.name}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        if 'session' in locals() and session:
            session.close()


if __name__ == '__main__':
    main()
