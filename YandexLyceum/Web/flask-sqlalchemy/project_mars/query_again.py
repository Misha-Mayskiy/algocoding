import sys
from collections import defaultdict

import db_session
from users import User
from jobs import Jobs
from departments import Department


def main():
    db_name = input().strip()
    if not db_name:
        sys.exit(1)

    try:
        db_session.global_init(db_name)
        session = db_session.create_session()

        target_department_id = 1
        min_hours_threshold = 25

        department = session.get(Department, target_department_id)
        if not department:
            return

        member_ids_str = department.members if department.members else ""
        member_ids = [int(id_str.strip()) for id_str in member_ids_str.split(',') if id_str.strip()]
        if department.chief not in member_ids:
            member_ids.append(department.chief)

        if not member_ids:
            return

        all_jobs = session.query(Jobs).all()
        user_hours = defaultdict(int)

        for job in all_jobs:
            collaborators_ids = [int(id_str.strip()) for id_str in job.collaborators.split(',') if
                                 job.collaborators and id_str.strip()]
            work_size = job.work_size if job.work_size else 0
            for user_id in collaborators_ids:
                if user_id in member_ids:
                    user_hours[user_id] += work_size
            if job.team_leader in member_ids:
                user_hours[job.team_leader] += work_size

        eligible_user_ids = [user_id for user_id, total_hours in user_hours.items() if
                             total_hours > min_hours_threshold]

        if not eligible_user_ids:
            return

        eligible_users = session.query(User).filter(User.id.in_(eligible_user_ids)).all()

        for user in eligible_users:
            print(f"{user.surname} {user.name}")

    except Exception:
        if 'session' in locals() and session:
            session.rollback()
    finally:
        if 'session' in locals() and session:
            session.close()


if __name__ == '__main__':
    main()
