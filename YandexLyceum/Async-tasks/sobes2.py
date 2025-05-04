import asyncio
import time


async def perform_single_task_stage(duration):
    await asyncio.sleep(duration / 100.0)


async def run_candidate_tasks(candidate_data):
    name, prep1, def1, prep2, def2 = candidate_data

    print(f"{name} started the 1 task.")
    await perform_single_task_stage(prep1)

    print(f"{name} started the 2 task.")
    await perform_single_task_stage(prep2)

    print(f"{name} moved on to the defense of the 1 task.")
    await perform_single_task_stage(def1)
    print(f"{name} completed the 1 task.")

    print(f"{name} moved on to the defense of the 2 task.")
    await perform_single_task_stage(def2)
    print(f"{name} completed the 2 task.")


async def interviews_2(*candidates):
    tasks = [run_candidate_tasks(candidate) for candidate in candidates]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    data = [('Ivan', 5, 2, 7, 2), ('John', 3, 4, 5, 1), ('Sophia', 4, 2, 5, 1)]
    t0 = time.time()
    asyncio.run(interviews_2(*data))
    print(time.time() - t0)
